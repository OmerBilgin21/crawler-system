FROM python:3.10-slim


WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

ARG ENV
ENV ENV $ENV

ARG DB_USER_NAME
ENV DB_USER_NAME $DB_USER_NAME

ARG DB_NAME
ENV DB_NAME $DB_NAME

ARG FILE_NAME
ENV FILE_NAME $FILE_NAME

CMD [ "python3", "explorer.py" ]

