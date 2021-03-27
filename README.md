Для корректной работы веб-приложения нужно создать группу executor в админке.
executor - может менять статус заявки



Подготовка и запуск:

pip3 install -r requirements.txt

python manage.py makemigrations qr_accounting

python manage.py migrate

python manage.py createsuperuser
#Запуск сервера
python manage.py runserver