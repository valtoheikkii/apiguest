FROM ubuntu:latest
MAINTAINER Naren J
RUN  apt-get -yq update && \
     apt-get -yqq install ssh
RUN apt-get install -y git python-pip python-dev build-essential

RUN mkdir /root/.ssh/
ADD id_rsa /root/.ssh/id_rsa
RUN chmod 400 /root/.ssh/id_rsa
RUN chown -R root:root /root/.ssh
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

COPY . /app
WORKDIR /app

RUN git clone git@github.com:SageAxcess/common.git common-repo
RUN rm -rf common
RUN mv common-repo/src common
RUN rm -rf common-repo

RUN pip install -r requirements.txt
RUN pip install -r common/requirements.txt
CMD ["python", "-u", "guest_service.py"]