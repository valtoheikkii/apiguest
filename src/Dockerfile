FROM ubuntu:latest
MAINTAINER Shubhadeep Roychowdhury
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install -r common/requirements.txt
CMD ["python", "-u", "guest_service.py"]