# SmahtZillow

SmahtZillow is a rental searh engine template application.

## Getting Started

### Prerequisites
- Node.JS
- Node dependency:
  ```
  "dependencies": {
    "body-parser": "~1.15.2",
    "client-sessions": "^0.7.0",
    "cookie-parser": "~1.4.3",
    "debug": "~2.2.0",
    "express": "~4.14.0",
    "jade": "~1.11.0",
    "jayson": "^2.0.2",
    "mongoose": "^4.7.5",
    "morgan": "~1.7.0",
    "password-hash": "^1.2.2",
    "serve-favicon": "~2.3.0"
  ```
  - password hash (optional)
  
- MongoDB
  - Mongoose
  
- CloudAMQP

- Python
  - Pyjsonrpc
  - Pika
  - Zillow-API (optional)
  - Xmljson
  - lxml
  
- Tor (optional)

### Download and Use

Download from SZ_Project/Week3 the source code.

- Run the local mongodb.

- Run the node server, go to the directory under SZ_Project/Week3, use ```./bin/www``` to start the web server.

  Front-end server will take request from clients and call data fetchers, which are back-end crawlers, to collect info corresponding to the search criterions. These data will be stored on the local MongoDB. Data fetchers are cooporated with zillow-api in case when data is not available throught crawlers.

- CloudAMQP provides an asynchronized approach for data fetchers to produce and consume rental info.

## Author

**Eason - @2017**
