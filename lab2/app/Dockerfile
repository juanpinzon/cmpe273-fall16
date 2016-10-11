FROM python:2.7
MAINTAINER Juan Pinzon "juan.pinzonestupinan@sjsu.edu"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["app.py"]
