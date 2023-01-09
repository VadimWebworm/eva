FROM python:3.8

WORKDIR /app

ADD models ./models
ADD asr_app.py asr_app.py

RUN pip install flask gunicorn
RUN pip install vosk

EXPOSE 5005

CMD [ "gunicorn", "--bind", "0.0.0.0:5005", "asr_app:get_app()" ]
