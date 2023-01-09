# EVA - Educator's voice assistant

## Голосовой ассистент преподавателя для оценки знаний учеников и студентов.
Ученику задается вопрос, на который он должен ответить голосом. 
Система распознает ответ ученика и сравнивает его с правильным ответом. 
Результат выводится на экран и сохраняется в базе данных.   

В проекте используются технологии:  
* django web server - базовый UI, аутентификация пользователей, работа с базой данных.  
* ASR (automatic speech recognition) для перевода голоса в текст - [vosk+pykaldi](https://alphacephei.com/vosk/server)
* NLP для сравнения близости двух текстов (ответа ученика и правильного ответа) - [DeepPavlov](https://deeppavlov.ai/).


## Запуск приложения

1) Скачайте репозиторий  
```
git clone https://github.com/labintsev/eva.git
```

2.1) Запуск в режиме разработки UI  
```
cd app  
pip install -r requirements.txt  
python manage.py runserver 
``` 

2.2) Запуск в docker контейнерах вместе с сервисами распознавания голоса и текста  
```
docker-compose build  
docker-compose up
``` 

Откройте браузер по ссылке [localhost:8000](127.0.0.1:8000).

