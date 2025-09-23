from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp, when
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType

# PostgreSQL bağlantı bilgileri
DB_USER = 'train'
DB_PASS = 'Ankara06'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'traindb'
DB_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Kafka veri şeması
schema = StructType() \
    .add("InvoiceNo", StringType()) \
    .add("StockCode", StringType()) \
    .add("Description", StringType()) \
    .add("Quantity", StringType()) \
    .add("InvoiceDate", StringType()) \
    .add("UnitPrice", StringType()) \
    .add("CustomerID", StringType()) \
    .add("Country", StringType())

def create_spark_session():
    return SparkSession.builder \
        .appName("KafkaToPostgres") \
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,"
                "org.postgresql:postgresql:42.7.3") \
        .getOrCreate()

def transform_data(df):
    return df \
        .withColumn("Quantity", when(col("Quantity") != "", col("Quantity").cast(IntegerType())).otherwise(None)) \
        .withColumn("UnitPrice", when(col("UnitPrice") != "", col("UnitPrice").cast(DoubleType())).otherwise(None)) \
        .withColumn("InvoiceDate", to_timestamp(col("InvoiceDate"), "M/d/yyyy H:mm")) \
        .filter(col("Quantity").isNotNull())

def save_to_postgres(row_dict):
    """
    Test edilebilir PostgreSQL veri kaydetme fonksiyonu.
    Bu unittest mock ile test edilir.
    """
    import psycopg2

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO orders (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (
        row_dict.get("InvoiceNo"),
        row_dict.get("StockCode"),
        row_dict.get("Description"),
        row_dict.get("Quantity"),
        row_dict.get("InvoiceDate"),
        row_dict.get("UnitPrice"),
        row_dict.get("CustomerID"),
        row_dict.get("Country")
    ))

    conn.commit()
    cursor.close()
    conn.close()

def foreach_batch_function(df, epoch_id):
    df.write \
      .format("jdbc") \
      .option("url", DB_URL) \
      .option("dbtable", "orders") \
      .option("user", DB_USER) \
      .option("password", DB_PASS) \
      .option("driver", "org.postgresql.Driver") \
      .mode("append") \
      .save()

def start_streaming():
    spark = create_spark_session()

    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "orders") \
        .load()

    json_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
        .select(from_json(col("json_str"), schema).alias("data")) \
        .select("data.*")

    cleaned_df = transform_data(json_df)

    query = cleaned_df.writeStream \
        .foreachBatch(foreach_batch_function) \
        .outputMode("append") \
        .start()

    query.awaitTermination()

# Bu if bloğu sadece script olarak çalıştırıldığında geçerli olur,
# import edildiğinde çalışmaz (CI/test için kritik!)
if __name__ == "__main__":
    start_streaming()
