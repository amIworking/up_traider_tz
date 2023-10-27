#  Тестовое задание для компании АП Трейдер

### Шаги для того, чтобы увидеть результат
1. Склонировать данный репозиторий при помощи команды: git clone https://github.com/amIworking/up_traider_tz.git
2. Установить виртульное окружение: python3 -m venv venv
3. Включить вирт. окр. source venv/bin/activate
4. Установить django: pip install django
5. Установить директорию: menu as root
6. Запустить проект: python3 manage.py runserver
7. Перейти по адресу: http://127.0.0.1:8000/menu/?code=pizza

В конечном итоге должен выйти ответ вида:
 pizza {'name': 'Меню', 'link': '/menu/?code=<built-in function id>', 'child': [{'name': 'Пицца', 'link': '/menu/?code=<built-in function id>', 'child': [{'name': 'Большая', 'link': '/menu/?code=<built-in function id>', 'child': []}, {'name': 'Средняя', 'link': '/menu/?code=<built-in function id>', 'child': []}]}, {'name': 'Бургеры', 'link': '/menu/?code=<built-in function id>', 'child': [{'name': 'Острые', 'link': '/menu/?code=<built-in function id>', 'child': []}, {'name': 'Классические', 'link': '/menu/?code=<built-in function id>', 'child': []}]}]} 
Который будет запрашивать 1 sql запрос
