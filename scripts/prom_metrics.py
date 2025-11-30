from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Flask
import time
import requests
import threading

app = Flask(__name__)

TEST_API_URL = "http://example.com" # Target URL

# Prometheus Metrics
API_LATENCY_MS = Histogram( "aiops_api_latency_ms", "Latency of API requests in milliseconds" )
API_ERRORS_TOTAL = Counter( "aiops_api_errors_total", "Total number of API request errors" )

def collect_metrics():
    while true:
        start_time = time.time()
        try:
            response = requests.get(TEST_API_URL, timeout=10)
            response.raise_for_status() # Raise an exception for bad status codes
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Record latency
            API_LATENCY_MS.observe(latency_ms)
        except Exception as e:
            API_ERRORS_TOTAL.inc()
        time.sleep(5)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # Start metric collection thread
    t = threading.Thread(target=collect_metrics)
    t.daemon = True
    t.start()

    # Run Flask app
    app.run(host="0.0.0.0", port=8000)