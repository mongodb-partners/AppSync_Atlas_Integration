FROM amazon/aws-lambda-python:3.8

ADD driver_input.py ./

RUN pip install 'pymongo[srv]'==3.11
RUN pip install requests
RUN pip install boto3

CMD ["driver_input.handler"]