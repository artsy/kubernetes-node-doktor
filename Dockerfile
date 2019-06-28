FROM python:3.6

RUN pip install pipenv

RUN mkdir /app

WORKDIR /app

ADD . /app

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python", "main.py"]
