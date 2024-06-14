import os

BASE_DIR = os.path.dirname(__file__)

## MySQL DBMS URI
DB_MYSQL_URI = "mysql+pymysql://root:1234@localhost:3306/computer_mate"

## 사용할 DBMS 설정/ SQLALCHEMY_시작 변수명 고정
SQLALCHEMY_DATABASE_URI = DB_MYSQL_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
