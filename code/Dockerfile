FROM amazon/aws-lambda-python:3.8

ADD datasource.py ./

RUN pip install 'pymongo[srv]'==3.11
RUN pip install requests

CMD ["datasource.handler"]
