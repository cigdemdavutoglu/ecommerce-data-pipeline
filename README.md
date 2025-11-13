# Spark-Kafka Streaming Projesi

Bu proje, Apache Spark Streaming ile Apache Kafka’yı entegre ederek gerçek zamanlı veri akışını yönetmeyi amaçlayan bir veri mühendisliği uygulamasıdır. Kafka’dan gelen veriler, Spark tarafından işlenip analiz edilir ve sonuçlar PostgreSQL veritabanına kaydedilir. Projede ayrıca iş akışlarının otomatikleştirilmesi için Apache Airflow kullanılmıştır. Tüm bileşenler Docker ve Docker Compose kullanılarak ayağa kaldırılabilir şekilde yapılandırılmıştır. Ayrıca proje, GitHub Actions ile Docker image’larının otomatik build ve push işlemini (CD) gerçekleştirir.  

---

## Projede Neler Var?

- Kafka üzerinden gerçek zamanlı veri üretimi ve tüketimi  
- Spark Streaming ile veri işleme ve PostgreSQL’e yazma  
- Spark job’unun Airflow DAG ile otomatik tetiklenmesi  
- Docker ve GitHub Actions ile CI/CD süreçlerinin uygulanması  

---

## Kullanılan Teknolojiler

- **Apache Kafka**: Veri akışı için mesaj kuyruğu sistemi  
- **Apache Spark Streaming**: Gerçek zamanlı veri işleme motoru  
- **Apache Airflow**: İş akışı otomasyonu  
- **PostgreSQL**: İşlenmiş verilerin saklandığı veritabanı  
- **Docker & Docker Compose**: Tüm servislerin kolayca kurulumu ve yönetimi  
- **GitHub Actions**: Docker image’larının otomatik build & push’u  
- **Python**: Tüm script ve uygulama geliştirmelerinde kullanılan programlama dili  

---

## Dosya Yapısı

dags/ -> Airflow DAG dosyaları

src/ -> Python scriptleri (producer, consumer, Spark job, Kafka->Postgres)

docker/ -> Her servis için Dockerfile’lar

tests/ -> Unit testler

docker-compose.yml -> Tüm servislerin lokal olarak çalıştırılması

.github/workflows/ -> CI/CD workflow dosyaları (docker-publish.yml)

requirements.txt -> Python bağımlılıkları

---

## Kurulum ve Kullanım

1. Repo’yu klonlayın:

```bash
git clone https://github.com/cigdemdavutoglu/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline

2. Sanal bir Python ortamı oluşturun ve aktive edin:

python3 -m venv venv
source venv/bin/activate

3. Gerekli Python paketlerini yükleyin:

pip install -r requirements.txt

4. Tüm servisleri Docker Compose ile başlatın:

docker-compose up -d

5. Tarayıcı üzerinden Airflow arayüzüne erişin:

http://localhost:1502

6. spark_streaming_dag DAG’ını etkinleştirin ve tetikleyin. Spark uygulaması Kafka’dan verileri okuyup PostgreSQL’e yazacaktır.

---

## CI/CD ve Docker Hub

Bu proje, GitHub Actions kullanarak Docker image’larını otomatik olarak build ve Docker Hub’a push eder.

Workflow dosyası: .github/workflows/docker-publish.yml

Docker Hub kullanıcı adı: cigdemdavutoglu

Public Docker image’lar:

Servis	Docker Hub Image
Producer	cigdemdavutoglu/producer
Consumer	cigdemdavutoglu/consumer
Spark Kafka Streaming	cigdemdavutoglu/spark-kafka-streaming
Kafka to Postgres	cigdemdavutoglu/kafka-to-postgres

Not: “Inactive” durum, image’ın henüz container olarak çalışmadığını gösterir. Image’ları çekip çalıştırabilirsiniz:
docker pull cigdemdavutoglu/producer:latest
docker run -it cigdemdavutoglu/producer:latest

---

## Ne İşe Yarar?

src/producer.py: Kafka’ya örnek veri gönderir

src/consumer.py: Kafka’dan veri okur

src/kafka_to_postgres.py: Spark Streaming uygulaması Kafka’dan gelen verileri PostgreSQL’e yazar

dags/spark_kafka_streaming.py: Spark Streaming uygulamasını tanımlar; Kafka’dan veri alır ve PostgreSQL’e yazar

dags/spark_streaming_dag.py: Spark scriptini çalıştırmak için Airflow DAG’ını tanımlar

---

## Lisans

Bu proje MIT lisansı ile lisanslanmıştır.

