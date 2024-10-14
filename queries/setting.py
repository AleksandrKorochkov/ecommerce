from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseConfig:
    database: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных
    db_port: str

@dataclass
class Config:
    db: DatabaseConfig


def load_config(path: str | None = None) -> str:
    env: Env = Env()
    env.read_env(path)
    path_db = Config(db = DatabaseConfig(
        database=env('DATABASE'),
        db_host=env('DB_HOST'),
        db_user=env('DB_USER'),
        db_password=env('DB_PASSWORD'),
        db_port=env('DB_PORT')
    ))
    return "postgresql+asyncpg://postgres:1212@localhost:5432/ecommerce"
    # return f'postgresql+asyncpg://{path_db.db.db_user}:{path_db.db.db_password}@{path_db.db.db_host}:{path_db.db.db_port}/{path_db.db.database}'

    
def key_config(path: str | None = None) -> dict:
    env: Env = Env()
    env.read_env('/Users/alexkor/Desktop/VS/queries/.env')
    return {"key": env('secret_key'), "algo": env('ALGORITHM')}

