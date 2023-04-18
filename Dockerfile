FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y python3 pip mysql-server python-dev default-libmysqlclient-dev libssl-dev net-tools vim mc wget lynx curl less && apt-get clean
RUN pip install mysql-connector-python

ENV PROJECT_DIR /var/hackergram

RUN mkdir -p $PROJECT_DIR

COPY utils/requirements.txt $PROJECT_DIR
RUN pip install -r /var/hackergram/requirements.txt

COPY utils/container_start.sh $PROJECT_DIR
COPY utils/start.sql $PROJECT_DIR
COPY ./app/ $PROJECT_DIR

RUN chmod +x /var/hackergram/container_start.sh

EXPOSE 5000

CMD ["/var/hackergram/container_start.sh"]
