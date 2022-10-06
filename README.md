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



## Steps for Integration

### 1.Create a MongoDB Atlas cluster

Please follow the [link](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster) to setup a free cluster in MongoDB Atlas

Configure the database for [network security](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) and [access](https://www.mongodb.com/docs/atlas/tutorial/create-mongodb-user-for-cluster/).


### 2.Create MongoDB Data API

Create the Data APIs using the [link](https://www.mongodb.com/developer/products/atlas/atlas-data-api-introduction/)


### 3.Create the lamdba resolver


### 3.Create the AWS AppSync API


### 4. Test the API

## Summary

Hope this technical guide helped you in integrating AWS AppSync API with MongoDB Atlas

For any assistance please reach out to partners@mongodb.com
