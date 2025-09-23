from unittest.mock import patch, MagicMock
from src import consumer  # consumer.py dosyası src/ klasöründe olmalı

@patch('src.consumer.KafkaConsumer')  # ← KafkaConsumer'ı **doğru modül yolu** ile mock'la
def test_consume_message(mock_consumer_class):
    # KafkaConsumer mock'u
    mock_consumer = MagicMock()
    mock_consumer.__iter__.return_value = [MagicMock(value=b"hello kafka consumer")]
    mock_consumer_class.return_value = mock_consumer

    # Test edilen fonksiyonu çağır
    result = consumer.consume_message()

    # Dönen mesajlar içinde test mesajı var mı kontrol et
    assert b"hello kafka consumer" in result
