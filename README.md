# small django scrapy scraping project

first install =>

pip install django scrapy scrapyd python-scrapyd-api

python manage.py makemigrations
python manage.py migrate

launch django server and scrapy server by =>

on scraping folder level 
python managae.py runserver
then go open new bash tab and in scraper_engine folder and run scrapy simultaneuoulsly
scrapyd

http://127.0.0.1:8000/launch/

Enter a website adress in the input and submit

You will get the src of all the images in the page saved in db
