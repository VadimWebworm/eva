FROM python:3.8

WORKDIR /app

RUN pip install flask gunicorn
RUN pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install sentence_transformers

COPY . .

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "ts_app:get_app()" ]
