FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y

COPY /app/requirements.txt .
COPY ./app /app
WORKDIR /app

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "migrate"] 

EXPOSE 8000
