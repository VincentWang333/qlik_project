FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app/qlik_assessment
COPY requirements.txt /app/qlik_assessment/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app/qlik_assessment
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
EXPOSE 8000
CMD python3 manage.py runserver 0.0.0.0:8000