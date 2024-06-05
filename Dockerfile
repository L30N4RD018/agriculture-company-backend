FROM python:3.12-slim

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

ENTRYPOINT uvicorn app:app --host=0.0.0.0 --port=${PORT:-8000}