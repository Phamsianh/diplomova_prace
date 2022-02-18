FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ARG db_host
ARG db_port
ARG db_username
ARG db_password
ARG db_name

ENV DB=postgresql \
    DB_HOST=$db_host \
    DB_PORT=$db_port \
    DB_USERNAME=$db_username \
    DB_PASSWORD=$db_password \
    DB_NAME=$db_name

COPY . .

CMD [ "uvicorn" , "main:app" , "--reload" , "--host", "0.0.0.0" , "--port", "8000" ]