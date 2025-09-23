from kafka import KafkaConsumer

def consume_message():
    consumer = KafkaConsumer(
        'test-topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000
    )
    messages = []
    for msg in consumer:
        messages.append(msg.value)
    consumer.close()
    return messages
