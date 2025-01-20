FROM python:3.12-slim

RUN mkdir -p /home/app

WORKDIR /home/app

COPY ./requirements.txt /home/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/app

EXPOSE 80

ENTRYPOINT ["uvicorn", "app:app", "--host=0.0.0.0", "--port", "80"]