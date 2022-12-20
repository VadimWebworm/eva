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

```
git clone https://github.com/labintsev/eva.git  
python manage.py makemigrations  
python manage.py migrate  
python manage.py loaddata fixtures/data.json  
python manage.py runserver 
``` 

Откройте браузер по ссылке [localhost:8000](127.0.0.1:8000).

