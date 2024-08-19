import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def iniciar_conexion():
    HOST = os.getenv('DB_HOST')
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    DB = os.getenv('DB_DB')

    config = {
            'host': HOST,
            'user': USER,
            'password': PASSWORD,
            'database': DB,
            'charset': 'utf8mb4'
            }

    connections = pymysql.connect(**config)
    return connections
