import pytest
from pyspark.sql import SparkSession
from src import spark_kafka_streaming  # parse_json fonksiyonu burada olmalı

@pytest.fixture(scope="module")
def spark():
    """Test için SparkSession fixture'ı"""
    return SparkSession.builder \
        .master("local[2]") \
        .appName("KafkaSparkTest") \
        .getOrCreate()

def test_parse_json(spark):
    """
    parse_json fonksiyonunun JSON string'leri doğru şekilde DataFrame'e dönüştürdüğünü test eder.
    """

    # JSON string formatında örnek veri (tek kolon: 'value')
    sample_data = [(
        '{"InvoiceNo": "536365", "StockCode": "85123A", '
        '"Description": "WHITE HANGING HEART T-LIGHT HOLDER", '
        '"Quantity": 6, "InvoiceDate": "12/1/2010 8:26", '
        '"UnitPrice": 2.55, "CustomerID": 17850, "Country": "United Kingdom"}',
    )]

    # Tek kolondan oluşan DataFrame oluştur
    df = spark.createDataFrame(sample_data, ["value"])

    # parse_json fonksiyonunu çağır
    parsed_df = spark_kafka_streaming.parse_json(df)

    # Test çıktısını göster (CI log'larında görebilmek için)
    parsed_df.show(truncate=False)

    # Beklenen kolonların hepsi geldi mi?
    expected_columns = [
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country"
    ]
    
    # Her bir kolonun gerçekten DataFrame'de yer alıp almadığını kontrol et
    for col in expected_columns:
        assert col in parsed_df.columns, f"Kolon eksik: {col}"
