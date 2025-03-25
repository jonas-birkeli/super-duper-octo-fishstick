import os
from dotenv import load_dotenv
load_dotenv()

# MySQL configuration for NTNU
MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST', 'stupid_host_url'),
    'user': os.getenv('DB_USER', 'stupid_username'),
    'password': os.getenv('DB_PASSWORD', 'stupid_password'),
    'database': os.getenv('DB_NAME', 'stupid_db_name')
}