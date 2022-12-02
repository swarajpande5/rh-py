FROM python:3.6-slim 

RUN mkdir /application
WORKDIR /application 

COPY requirements.txt . 
RUN pip install -r requirements.txt 

COPY . . 

ENV PYTHONBUFFERED 1 

EXPOSE 8081 

ENTRYPOINT ["python"]
CMD ["app.py"]