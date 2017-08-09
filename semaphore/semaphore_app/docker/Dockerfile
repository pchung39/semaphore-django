# base image
FROM ubuntu:16.04

# update build
RUN apt-get update

# just in case, install python in Ubuntu build
RUN apt-get install -y python python-pip wget git

RUN apt-get -y install openssh-client
CMD ssh-keygen -q -t rsa -N '' -f /keys/id_rsa

# pull git repo for semaphore
RUN git clone https://github.com/pchung39/semaphore-django.git
WORKDIR /home/semaphore-django

# run pip install -r requirements.txt
RUN pip install -r requirements.txt
