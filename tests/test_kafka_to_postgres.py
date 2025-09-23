import pytest
from unittest.mock import patch, MagicMock

# Doğrudan psycopg2.connect'i mock'la
@patch('psycopg2.connect')
def test_db_insert(mock_connect):
    # Mock connection ve cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Fonksiyon içe aktarılıyor
    from src.kafka_to_postgres import save_to_postgres

    # Test verisi
    test_data = {
        "InvoiceNo": "536365",
        "StockCode": "85123A",
        "Description": "WHITE HANGING HEART T-LIGHT HOLDER",
        "Quantity": 6,
        "InvoiceDate": "12/1/2010 8:26",
        "UnitPrice": 2.55,
        "CustomerID": 17850,
        "Country": "United Kingdom"
    }

    # Fonksiyonu çağır
    save_to_postgres(test_data)

    # execute çağrıldı mı?
    assert mock_cursor.execute.called, "Cursor.execute() hiç çağrılmadı."

    # INSERT içeriyor mu?
    called_args = mock_cursor.execute.call_args[0]
    assert any("INSERT" in str(arg).upper() for arg in called_args), "INSERT sorgusu gönderilmedi."

    # commit çağrıldı mı?
    mock_conn.commit.assert_called_once()

    # kaynaklar kapatıldı mı?
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
