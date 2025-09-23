from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StringType


def get_spark_session():
    return SparkSession.builder \
        .appName("KafkaToConsole_Cleaned") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0") \
        .getOrCreate()


def get_schema():
    return StructType() \
        .add("InvoiceNo", StringType()) \
        .add("StockCode", StringType()) \
        .add("Description", StringType()) \
        .add("Quantity", StringType()) \
        .add("InvoiceDate", StringType()) \
        .add("UnitPrice", StringType()) \
        .add("CustomerID", StringType()) \
        .add("Country", StringType())


def parse_json(df):
    schema = get_schema()
    return df.selectExpr("CAST(value AS STRING) as json_str") \
             .select(from_json(col("json_str"), schema).alias("data")) \
             .select("data.*")


def clean_data(df):
    return df \
        .withColumn("Quantity", col("Quantity").cast("int")) \
        .withColumn("UnitPrice", col("UnitPrice").cast("double")) \
        .withColumn("InvoiceDate", to_timestamp(col("InvoiceDate"), "M/d/yyyy H:mm"))


def start_streaming():
    spark = get_spark_session()
    raw_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "orders") \
        .load()

    parsed_df = parse_json(raw_df)
    cleaned_df = clean_data(parsed_df)

    query = cleaned_df.writeStream \
        .format("console") \
        .outputMode("append") \
        .start()

    query.awaitTermination()


# Doğrudan çalıştırıldığında stream başlat
if __name__ == "__main__":
    start_streaming()
