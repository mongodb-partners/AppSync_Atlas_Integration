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

### 6. Test the API
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

Hope this technical guide helped you in integrating AWS AppSync API with MongoDB Atlas

For any assistance please reach out to partners@mongodb.com
