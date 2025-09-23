### Spark-Kafka Streaming Projesi

Bu proje, Apache Spark Streaming ile Apache Kafka’yı entegre ederek gerçek zamanlı veri akışını yönetmeyi amaçlayan bir veri mühendisliği uygulamasıdır. Kafka’dan gelen veriler, Spark tarafından işlenip analiz edilir ve sonuçlar PostgreSQL veritabanına kaydedilir. Projede ayrıca iş akışlarının otomatikleştirilmesi için Apache Airflow kullanılmıştır. Tüm bileşenler Docker ve Docker Compose kullanılarak ayağa kaldırılabilir şekilde yapılandırılmıştır.

### Projede Neler Var?

Projede Kafka üzerinden gerçek zamanlı veri üretimi ve tüketimi sağlanmaktadır. Üretilen veriler Spark Streaming uygulaması tarafından okunur, işlenir ve PostgreSQL’e yazılır. Spark job’u, Airflow DAG aracılığıyla otomatik olarak tetiklenir. Böylece veri akışı uçtan uca otomatik bir sistemle yönetilmiş olur.

### Kullanılan Teknolojiler

Apache Kafka: Veri akışı için mesaj kuyruğu sistemi

Apache Spark Streaming: Gerçek zamanlı veri işleme motoru

Apache Airflow: İş akışı otomasyonu

PostgreSQL: İşlenmiş verilerin saklandığı veritabanı

Docker & Docker Compose: Tüm servislerin kolayca kurulumu ve yönetimi

Python: Tüm script ve uygulama geliştirmelerinde kullanılan programlama dili

### Dosya Yapısı

dags/ klasörü, Airflow tarafından çalıştırılacak DAG dosyalarını içerir.

src/ klasörü, Kafka’ya veri gönderen producer.py ve Kafka’dan veri okuyan consumer.py scriptlerini barındırır.

src/kafka_to_postgres.py: PostgreSQL veritabanına yazmak için kullanılan scripti içerir.

docker-compose.yml dosyası, Spark, Kafka, PostgreSQL ve Airflow gibi servislerin tek komutla ayağa kalkmasını sağlar.

requirements.txt dosyası, Python ortamı için gerekli bağımlılıkları listeler.

README.md, projenin açıklamasını ve kurulum adımlarını içerir.

### Kurulum ve Kullanım

Projeyi kullanmaya başlamak için önce GitHub üzerinden klonlamanız yeterlidir. Aşağıdaki adımlar size kurulum sürecini anlatır:

Projeyi GitHub üzerinden klonlayın:

git clone https://github.com/cigdemdavutoglu/ecommerce-data-pipeline.git

cd ecommerce-data-pipeline


Sanal bir Python ortamı oluşturun ve aktive edin:

python3 -m venv venv
source venv/bin/activate


Gerekli Python paketlerini yükleyin:

pip install -r requirements.txt


Tüm servisleri başlatmak için Docker Compose komutunu çalıştırın:

docker-compose up -d


Tarayıcı üzerinden Airflow arayüzüne erişin: http://localhost:1502

spark_streaming_dag adlı DAG’ı etkinleştirin ve tetikleyin. Spark uygulaması, Kafka’dan verileri okuyarak PostgreSQL’e kaydetmeye başlayacaktır.

### Ne İşe Yarar?

src/producer.py: Kafka’ya örnek veri gönderir.

src/consumer.py: Kafka’dan veri okur.

src/kafka_to_postgres.py: Spark Streaming uygulaması Kafka’dan gelen verileri PostgreSQL veritabanına yazmak için kullanılır.

dags/spark_kafka_streaming.py: Spark Streaming uygulamasını tanımlar; Kafka’dan veri alır ve PostgreSQL’e yazar.

dags/spark_streaming_dag.py: Yukarıdaki Spark scriptini çalıştırmak için Airflow DAG’ını tanımlar.

### Lisans

Bu proje MIT lisansı ile lisanslanmıştır. 
