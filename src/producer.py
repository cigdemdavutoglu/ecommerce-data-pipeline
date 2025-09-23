from kafka import KafkaProducer

def send_message(topic, message):
    """
    Kafka'ya mesaj göndermek için kullanılan fonksiyon.
    
    Args:
        topic (str): Kafka topic adı.
        message (bytes): Gönderilecek mesaj (byte formatında olmalı).
    """
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    producer.send(topic, message)
    producer.flush()
    producer.close()
