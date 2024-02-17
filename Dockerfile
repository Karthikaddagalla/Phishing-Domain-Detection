FROM python:3.9

COPY . /app

WORKDIR /app

ENV PYTHONUNBUFFERED=1


RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
