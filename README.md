# Hospital
## MySql 8
Дамп базы данных находится в папке Hospital/database_dump

## Python 3.6 
## Зависимости

Для реализации RESTful сервиса используется фреймворк bottle(0.12.16)  
Если нет, то можно установить:
```
# для Linux
pip3 install bottle
# для Windows
pip install bottle
```

Для работы с БД MySql8 используется mysql connector  
Если нет, то можно установить:
```
# для Linux
pip3 install mysql-connector-python
# для Windows
pip install mysql-connector-python
```
Для работы с аргументами используется модуль argparse  
Если нет, то можно установить:
```
# для Linux
pip3 install argparse
# для Windows
pip install argparse
```

# Настройка приложения
## Аргументы запуска
### Настройка домена приложения  
Запуск происходит на протоколе HTTP.    
_--host_ - параметр, который отвечает за хост на котором будет размещено приложение, например IP-адресс 192.168.0.1, или доменное имя localhost  
Значение по умолчанию = **localhost**    
_--port_ - параметр, который отвечает за порт на котором будет размещено приложение, например 38080  
Значение по умолчанию = **5555**  
  
### Настройка доступа к БД MySql8  
_--dbhost_ - параметр, который указывает на каком хосте размещена база данных, например IP-адресс 192.168.0.1, или доменное имя localhost  
Значение по умолчанию = **localhost**  
_--dbport_ - параметр, который указывает на каком порту размещена база данных, например 3306  
Значение по умолчанию = **3306**  
_--dbuser_ - параметр, который указывает имя пользователя для работы с БД  
Значение по умолчанию = **root**  
_--dbpass_ - параметр, который указывает пароль пользователя для работы с БД  
Значение по умолчанию = Без пароля  
_--dbname_ - параметр, который указывает имя базы данных для подключения   
Значение по умолчанию = **hospital**  

## Запуск приложения
```
# для Linux
python3 app.py --host=localhost --port=5555 --dbhost=localhost --dbport=3306 --dbuser=root --dbpass=password1 --dbname=hospital
# для Windows
python app.py --host=localhost --port=5555 --dbhost=localhost --dbport=3306 --dbuser=root --dbpass=password1 --dbname=hospital
```


