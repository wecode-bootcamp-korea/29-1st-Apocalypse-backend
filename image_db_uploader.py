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

CSV_PATH = 'csv/images.csv'	# 3. csv 파일 경로

def insert_images():    
    with open(CSV_PATH, newline='', encoding='utf8') as csvfile:
        data_reader = csv.DictReader(csvfile)
        
        for row in data_reader:
            print(row)
            Image.objects.create(		# 5. class명.objects.create
                image_url     = row['이미지'],
                product_id    = row['상품'],
                )

    print('CATEGORY DATA UPLOADED SUCCESSFULY!')    

insert_images()
