FROM python:3.7.2-stretch

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install apt-utils && \
    apt-get -y install apt-transport-https curl nano

RUN export DEBIAN_FRONTEND=noninteractive && \
    curl -s https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl -s https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get -y install msodbcsql17 && \
    odbcinst -q -d -n "ODBC Driver 17 for SQL Server"

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install g++ && \
    apt-get -y install unixodbc-dev

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
