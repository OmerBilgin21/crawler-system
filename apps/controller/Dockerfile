FROM python:3.10-slim


WORKDIR /app
#COPY /apps/controller/ /apps/models /apps/__init__.py /apps/crawler /apps/scheduler /app/apps/

COPY . /app/

#COPY /controller.py /requirements.txt /app/

RUN pip3 install -r requirements.txt

ARG ENV
ENV ENV $ENV

ARG DB_USER_NAME
ENV DB_USER_NAME $DB_USER_NAME

ARG DB_NAME
ENV DB_NAME $DB_NAME

CMD [ "python3", "controller.py" ]

