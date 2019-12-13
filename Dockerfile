FROM python:3.8.0
RUN apt-get update
RUN apt-get install whois
RUN pip install --upgrade pip
RUN pip install flask dnspython3
RUN mkdir -p /usr/src/app
COPY ./app/ /usr/src/app/
WORKDIR /usr/src/app/
CMD ["python","/usr/src/app/app.py"]
EXPOSE 80