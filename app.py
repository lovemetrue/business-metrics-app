from flask import Flask
from prometheus_client import Counter, Gauge, Histogram, generate_latest
import random
import time

app = Flask(__name__)

# Бизнес-метрики
orders_total = Counter('app_orders_total', 'Total number of orders')
revenue_total = Counter('app_revenue_total', 'Total revenue', ['currency'])
active_users = Gauge('app_active_users', 'Number of active users')

# Технические метрики
request_duration = Histogram('app_request_duration_seconds', 'Request duration')
error_count = Counter('app_errors_total', 'Total errors')

@app.route('/')
def hello():
    start_time = time.time()
    
    # Имитация бизнес-логики
    if random.random() > 0.1:  # 90% успешных запросов
        orders_total.inc()
        revenue_total.labels(currency='USD').inc(random.uniform(10, 100))
        active_users.set(random.randint(100, 1000))
    else:
        error_count.inc()
    
    duration = time.time() - start_time
    request_duration.observe(duration)
    
    return 'Hello World!'

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
