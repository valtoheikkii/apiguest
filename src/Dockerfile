FROM sageaxcess/python-base
MAINTAINER Naren J

COPY . /app
WORKDIR /app
CMD ["gunicorn", "--config=gunicorn.py", "--log-config=logging.conf",  "guest_service:app"]
