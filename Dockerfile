# this is an official Python runtime, used as the parent image
FROM python:2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install  -r requirements.txt

COPY . .

EXPOSE 9000
CMD [ "python", "./src/controller/index.py" ]
