# AWS AppSync Integration with MongoDB Atlas

## Introduction


## MongoDB Atlas

[MongoDB Atlas](https://www.mongodb.com/atlas) is a modern Developer Data Platform with a fully managed cloud database at its core.  Atlas is the best way to run MongoDB, the leading non-relational database. It provides rich features like flexible schema model, native timeseries collections, geo-spatial data, multi level indexing, RBAC, isolated workloads and many more–all built on top of the MongoDB document model.  

MongoDB Atlas App Services help developers build apps, integrate services, and connect to their data without operational overhead utilizing features like hosted Data API and GraphQL API.  Atlas Data API allows developers to easily integrate Atlas data into their cloud apps and services over HTTPS with a flexible API.  Atlas GraphQL API lets developers access Atlas data from any standard GraphQL client with an API that generates based on your data’s schema. 


## AWS AppSync
[AWS AppSync](https://aws.amazon.com/appsync/) is an AWS product that allows developers to build GraphQL and Pub/Sub APIs.  With AppSync developers can create APIs that access data from one or many sources enabling real-time interactions in their applications.  The resulting APIs are serverless making it possible for the client to query only for the data it needs, in the format it needs, and pay only for the requests and the real-time messages delivered. 

## Salient Features

Authentication and Authorization through [Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)
Simple, Secured, Easy GraphQL APIs
Caching to improve performance
End-to-end serverless architecture
AutoScaling based on API request volumes
Subscriptions to support real-time updates


## Pre-requisite

Developer Tool: [VSCode](https://code.visualstudio.com/download), [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), [Docker](https://docs.docker.com/engine/install/), [Postman](https://www.postman.com/downloads/)


## Architecture

![](https://github.com/mongodb-partners/AppSync_Atlas_Integration/blob/main/code/AppSynDataAPI.png)



## Steps for Integration

### 1.Create a MongoDB Atlas cluster

Please follow the [link](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster) to setup a free cluster in MongoDB Atlas

Configure the database for [network security](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) and [access](https://www.mongodb.com/docs/atlas/tutorial/create-mongodb-user-for-cluster/).

create documents for customer and risk . please refer the sample structure for [CounterParty](https://github.com/mongodb-partners/AppSync_Atlas_Integration/blob/main/code/customer.json) and [CounterPartyRisk](https://github.com/mongodb-partners/AppSync_Atlas_Integration/blob/main/code/risk.json) documents.

### 2.Create MongoDB Data API

Create the Data APIs using the [link](https://www.mongodb.com/developer/products/atlas/atlas-data-api-introduction/)


### 3.Store the API Key in AWS Secrets

Copy the API Key and MongoDB Credentials to a local JSON file. Template for the JSON files shown in the link:  [mycreds.json](https://github.com/mongodb-partners/AppSync_Atlas_Integration/blob/main/code/mycreds.json) & [myapikey.json](https://github.com/mongodb-partners/AppSync_Atlas_Integration/blob/main/code/myapikey.json)

      aws secretsmanager create-secret --name <secret_name> \
          --description "MongoDB secrets created for AWS AppSync" \
          --secret-string file://mycreds.json
          
      aws secretsmanager create-secret --name <secret_name> \
          --description "API Keys secret created for AWS AppSync" \
          --secret-string file://myapikey.json



### 4. crerate a AWS Elastic Container Repository


      aws ecr create-repository \
                  --repository-name partner_atlas_appsync_int \
                  --image-scanning-configuration scanOnPush=true \
                  --region <aws_region>


### 5.create the docker image and deploy to lambda

The code base contain 3 repos: data_api_appsync, driver_appsync (datasource_create & datasource_read). Copy the appropriate code to the VSCode.

Note: AWS ECR repositories and Lambda functions are to be created for each of the 3 repos, viz: data_api_appsync /  driver_appsync (read / create)

update the DATA API endpoints and the database credentials appropriate for your requirement.

create the docker image

      aws ecr get-login-password --region <aws region> | docker login --username AWS --password-stdin <accountid>.dkr.ecr.<aws region>.amazonaws.com
      
      docker build -t partner_atlas_appsync_int . --platform=linux/amd64
      
      docker tag partner_test:latest <accountid>.dkr.ecr.<aws region>.amazonaws.com/partner_atlas_appsync_int:latest
      
      docker images
      
      docker push <accountid>.dkr.ecr.<aws region>.amazonaws.com/partner_atlas_appsync_int:latest


### 6.Create the Lambda function



      aws lambda create-function --region <aws region>  --function-name partner_atlas_appsync_int \
          --package-type Image  \
          --code ImageUri= <accountid>.dkr.ecr.<aws region>.amazonaws.com/partner_atlas_appsync_int:latest   \
          --role <Lambda execution role ARN>

pls check the [link](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-images.html#configuration-images-api) for reference code

Note: Ensure the lambda function is having adequate permission to read from the secret manager.

### 7.Create the AWS AppSync API


#### a. Create API
1. Choose Build from scratch and hit Start, for getting a blank API.
<img width="1728" alt="AppSync_Creation_Step1" src="https://user-images.githubusercontent.com/114057324/198644438-17269f86-094f-4113-83f0-4eb1b9d1fc97.png">

2. Add API Name
<img width="1728" alt="Screenshot 2022-10-28 at 5 36 25 PM" src="https://user-images.githubusercontent.com/114057324/198644942-23ffa2f9-dd09-4459-aa84-dcdab680eac4.png">


#### b. Add Schema
1. Click on Schema form the left navigations

<img width="1728" alt="Screenshot 2022-10-28 at 5 36 56 PM" src="https://user-images.githubusercontent.com/114057324/198645875-92ecc6d3-a55e-4986-9a37-71be54207a41.png">

2. GraphQL Schema can be built with Queries and Mutations and click Save Schema
<img width="1728" alt="Screenshot 2022-10-28 at 5 37 45 PM" src="https://user-images.githubusercontent.com/114057324/198646751-842d36c2-47f4-4750-a72d-4fe6a339e019.png">

#### c. Create Data Sources

1. Click on Data Sources from the left navigations and hit Create data source
<img width="1728" alt="Screenshot 2022-10-28 at 5 38 46 PM" src="https://user-images.githubusercontent.com/114057324/198647355-38a85ad1-95f7-47af-bd9d-4cbd082bfdae.png">


2. Attach Lambda function which contains MongoDB driver code for quering the data (Multiple data sources can be added based on requirements)
<img width="1728" alt="Screenshot 2022-10-28 at 5 40 00 PM" src="https://user-images.githubusercontent.com/114057324/198648544-23e46164-dc55-46c7-9693-31967a069400.png">


#### d. Attach Resolvers
1. Go to schema and attach resolvers for Mutations and Queries
<img width="1728" alt="Screenshot 2022-10-28 at 6 43 22 PM" src="https://user-images.githubusercontent.com/114057324/198650042-2e6e61dd-40be-4fc1-ab8b-357d024a00a4.png">

2. Select lambda data source added in previous step, and click save.
<img width="1728" alt="Screenshot 2022-10-28 at 6 44 32 PM" src="https://user-images.githubusercontent.com/114057324/198650403-a8ccb56f-2d07-479b-a46e-ab8d1425bd43.png">

### 8. Test the API
#### a. Using AWS Management Console
Goto Queries and select the query to execute, hit Run button and you should see your query result on the right side.

<img width="1728" alt="Screenshot 2022-10-28 at 6 46 20 PM" src="https://user-images.githubusercontent.com/114057324/198651689-0cd1a646-a54b-4d30-be2b-b80c4bbbb890.png">

##### b. Using Postman
1. Click on settings and create a curl API as below.

            curl --location --request <CRUD OPERATION> <API URL>
            --header 'Content-Type: application/graphql' \
            --header 'x-api-key: <API KEY> \
            --data-raw '{"query": <QUERY>}'
![Screenshot 2022-10-28 at 8 14 14 PM](https://user-images.githubusercontent.com/114057324/198657824-c690a69d-e2d5-4660-8db4-47d526af816e.png)

      
2. Goto Postman and import the curl command and hit send to get the response.

<img width="1728" alt="Screenshot 2022-10-28 at 7 41 33 PM" src="https://user-images.githubusercontent.com/114057324/198658280-c9f54909-2fb7-4090-994b-cc27cf661b99.png">


## Summary

This solution can be extended to [AWS Amplify](https://aws.amazon.com/amplify/) for building mobile applications.

For any further information, please contact partners@mongodb.com

