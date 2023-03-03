import os

print(os.getenv("DB_URL"))


class DbConfig:
    db_url = os.getenv("DB_URL")
    test_db_url = os.getenv("TEST_DB_URL")
    mongo_url = os.getenv("MONGO_URL")


db_config = DbConfig()
