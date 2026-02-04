import pytest
from unittest.mock import MagicMock, AsyncMock
from database.database import Database
from helper.utils import humanbytes, TimeFormatter

def test_humanbytes():
    assert humanbytes(1024) == "1.0 KB"
    assert humanbytes(1024*1024) == "1.0 MB"
    assert humanbytes(0) == "0 B"

def test_time_formatter():
    assert "1s" in TimeFormatter(1000)
    assert "1m" in TimeFormatter(60000)

@pytest.mark.asyncio
async def test_database_new_user():
    # Mocking motor client
    mock_client = MagicMock()
    db_instance = Database("mongodb://localhost:27017", "test_db")

    user_data = db_instance.new_user(12345)
    assert user_data['id'] == 12345
    assert user_data['credits'] == 10
    assert user_data['is_premium'] is False
