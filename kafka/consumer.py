from confluent_kafka import Consumer, KafkaException, KafkaError
import sys
import json
import time

# 1. Configuration
conf = {
    'bootstrap.servers': 'my-cluster-kafka-bootstrap.kafka:9092',
    # 'group.id' is required for consumers. Consumers in the same group
    # share the partitions of a topic, enabling parallel consumption.
    'group.id': 'aiops-project',
    # 'auto.offset.reset': 'earliest' ensures we read from the beginning
    # of the topic if we don't have a committed offset for this group.
    'auto.offset.reset': 'earliest',
    # Automatically commit offsets periodically
    'enable.auto.commit': True,
    'auto.commit.interval.ms': 1000  # Commit every second
}

# Create Consumer instance
consumer = Consumer(conf)
topic = "metrics-raw" # Must match the topic used by the producer example

# 2. Subscribe to the topic(s)
try:
    consumer.subscribe([topic])
    print(f"Subscribed to topic: {topic}. Waiting for messages...")

    # 3. Start the consumption loop
    while True:
        # Poll for messages. 'timeout' dictates how long to wait for a message.
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event - no more messages for now
                print(f"Reached end of partition for {msg.topic()} [{msg.partition()}]")
                continue
            elif msg.error():
                # Other error
                raise KafkaException(msg.error())
        else:
            # Successful message receipt
            # Messages are returned as bytes, so decode them
            try:
                # Assuming the producer sent JSON
                message_value = json.loads(msg.value().decode('utf-8'))
                print(f"Consumed message: key={msg.key()}, value={message_value}")
                # print(f"Partition: {msg.partition()}, Offset: {msg.offset()}")
            except json.JSONDecodeError:
                print(f"Received non-JSON message: {msg.value()}")

except KeyboardInterrupt:
    print("Consumer interrupted by user.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 4. Close the consumer to gracefully exit and commit final offsets
    print("Closing consumer.")
    consumer.close()