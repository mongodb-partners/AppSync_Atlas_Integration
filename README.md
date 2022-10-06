# AWS AppSync Integration with MongoDB Atlas

## Introduction


## [MongoDB Atlas](https://www.mongodb.com/atlas)

MongoDB Atlas is an all purpose database having features like Document Model, Geo-spatial , Time-seires, hybrid deployment, multi cloud services. It evolved as "Developer Data Platform", intended to reduce the developers workload on development and management the database environment. It also provide a free tier to test out the application / database features.


## [AWS AppSync](https://aws.amazon.com/appsync/)
AWS AppSync uses GraphQL, a data language that enables client apps to fetch, change and subscribe to data from servers. In a GraphQL query, the client specifies how the data is to be structured when it is returned by the server.

## Salient Features

Better performance and higher concurrency with MongoDB Atlas

Fine Grained data access.

Authentication and Authorization through [Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)


## Pre-requisite

Developer Tool: [VSCode](https://code.visualstudio.com/download), [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), [Docker](https://docs.docker.com/engine/install/), [Postman](https://www.postman.com/downloads/)



## Steps for Integration

### 1.Create a MongoDB Atlas cluster

Please follow the [link](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster) to setup a free cluster in MongoDB Atlas

Configure the database for [network security](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) and [access](https://www.mongodb.com/docs/atlas/tutorial/create-mongodb-user-for-cluster/).


### 2.Create MongoDB Data API

Create the Data APIs using the [link](https://www.mongodb.com/developer/products/atlas/atlas-data-api-introduction/)


### 3.Store the API Key in AWS Secrets

Copy the API Key into a json file, mycreds.json

      aws secretsmanager create-secret --name ATLASAPIKey \
          --description "API Keys secret created for AWS AppSync" \
          --secret-string file://mycreds.json


###3. crerate a AWS Elastic Container Repository

      aws ecr create-repository \
                  --repository-name partner_atlas_appsync_int \
                  --image-scanning-configuration scanOnPush=true \
                  --region us-east-1


### 3.create the docker image and deploy to lambda

Copy the Python code to the VSCode

update the DATA API endpoints

create the docker image

      aws ecr get-login-password --region us-east-1| docker login --username AWS --password-stdin <accountid>.dkr.ecr.us-east-1.amazonaws.com
      
      docker build -t partner_atlas_appsync_int . --platform=linux/amd64
      
      docker tag partner_test:latest <accountid>.dkr.ecr.us-east-1.amazonaws.com/partner_atlas_appsync_int:latest
      
      docker images
      
      docker push <accountid>.dkr.ecr.us-east-1.amazonaws.com/partner_atlas_appsync_int:latest


### 4.Create the Lambda function



      aws lambda create-function --region us-east-1 --function-name ppartner_atlas_appsync_int \
          --package-type Image  \
          --code ImageUri= <accountid>.dkr.ecr.us-east-1.amazonaws.com/partner_atlas_appsync_int:latest   \
          --role <Lambda execution role>

pls check the [link](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-images.html#configuration-images-api) for reference code

### 4.Create the AWS AppSync API


#### a. Define the schema

#### b. Update the data source

#### c. Build the API 

#### d. Query the database


### 5. Test the API

Test the API with Postman




## Summary

Hope this technical guide helped you in integrating AWS AppSync API with MongoDB Atlas

For any assistance please reach out to partners@mongodb.com
