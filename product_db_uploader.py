import csv 
import os
import sys
import django

os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apocalypse.settings")	# 1. 여기서 프로젝트명.settings입력
django.setup()

# 위의 과정까지가 python manage.py shell을 키는 것과 비슷한 효과

from products.models import *	# 2. App이름.models

CSV_PATH = 'csv/products.csv'	# 3. csv 파일 경로

def insert_products():    
    with open(CSV_PATH, newline='', encoding='utf8') as csvfile:
        data_reader = csv.DictReader(csvfile)
        
        for row in data_reader:
            print(row)
            Product.objects.create(		# 5. class명.objects.create
                korean_name     = row['한국이름'],
                english_name    = row['영어이름'],
                price           = row['가격'],
                description     = row['설명'],
                how_to_use      = row['사용방법'],
                subcategory_id  = row['서브카테고리']
        )

    print('CATEGORY DATA UPLOADED SUCCESSFULY!')    

insert_products()
