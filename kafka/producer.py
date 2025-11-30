from confluent_kafka import Producer
import socket
import json
import time

# 1. Configuration
# Replace 'localhost:9092' with your actual Kafka broker addresses
conf = {
    'bootstrap.servers': 'my-cluster-kafka-bootstrap.kafka:9092',
    # Optional: A client ID helps identify the source of connections in Kafka logs
    'client.id': socket.gethostname(),
    # Other common configs:
    # 'acks': 'all'   # Ensures full durability (default is '1')
    # 'retries': 3    # Number of retries on failed message delivery
}

# Create Producer instance
producer = Producer(conf)
topic = "metrics-raw"

# 2. Define the Delivery Callback Handler
# This function is called asynchronously by librdkafka when a message
# has been successfully delivered or permanently failed.
def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

# 3. Produce messages
try:
    for i in range(5):
        message_data = { "metric": "aiops_api_latency_ms", "value": 123.4, "timestamp": 1732960000 }
        
        # Serialize the message to a JSON string, then encode it to bytes
        value_bytes = json.dumps(message_data).encode('utf-8')
        
        # The produce() method is asynchronous. It queues the message for sending.
        producer.produce(
            topic=topic, 
            value=value_bytes, 
            callback=delivery_report
        )
        
        # Poll for any completed events (delivery reports) that need handling
        producer.poll(0) 
        time.sleep(0.1)

except BufferError:
    print("Local producer queue is full. Wait for messages to be delivered.")

except KeyboardInterrupt:
    pass

finally:
    # 4. Flush any outstanding or queued messages before exiting
    # This blocks until all messages are delivered or the timeout is reached.
    print("\nFlushing remaining messages...")
    remaining_messages = producer.flush(30)
    print(f"{remaining_messages} messages still pending delivery at exit.")