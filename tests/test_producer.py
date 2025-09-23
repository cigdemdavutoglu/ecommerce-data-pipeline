from unittest.mock import patch, MagicMock
from src import producer  # src/producer.py içindeki send_message fonksiyonu test ediliyor

@patch('src.producer.KafkaProducer')  # KafkaProducer'ı mockla
def test_send_message(mock_kafka_producer):
    # KafkaProducer mock instance'ını oluştur
    mock_instance = MagicMock()
    mock_kafka_producer.return_value = mock_instance

    # Fonksiyonu çağır
    producer.send_message('test-topic', b'hello')

    # KafkaProducer doğru şekilde kullanılmış mı kontrol et
    mock_kafka_producer.assert_called_once_with(bootstrap_servers='localhost:9092')
    mock_instance.send.assert_called_once_with('test-topic', b'hello')
    mock_instance.flush.assert_called_once()
    mock_instance.close.assert_called_once()
