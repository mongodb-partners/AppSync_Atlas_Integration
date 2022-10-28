FROM amazon/aws-lambda-python:3.8

ADD datasource_driver.py ./

RUN pip install 'pymongo[srv]'==3.11
RUN pip install requests
RUN pip install boto3

CMD ["datasource_driver.handler"]