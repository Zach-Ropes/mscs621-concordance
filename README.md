# Simple REST Server - Analyze and Locate

## Overview
A simple REST server which returns a specified JSON concordance based on an arbitrary English input
text. The concordance is implemented within Swagger by exporting a generated
server stub using python-flask. Can either analyze to get a simple concordance returned with just the token count or locate to get an indexed concordance returned with the location of each individual word from the inputted plain text.

## Requirements
Python 3.5.2+

## Usage
To run the server, execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m swagger_server 
# or if using the latest version of python (or at least in my case)
python -m swagger_server
```

Once running, there are two endpoints available. For a concordance, open up another command line and execute the following: 

```
-X POST "http://localhost:8080/mscs721/concordance/1.0.0/analyze" -H  "accept: application/json" -H  "Content-Type: text/plain" -d "Insert what you want returned in JSON concordance here."
```

This command targets the 'analyze' endpoint, taking the input string from the request and returning a JSON concordance (each word/token and the number of appearances of that token).

For the location of tokens within the input text, target the 'locate' endpoint with another command. Execute the following from the command line:

```
-X POST "http://localhost:8080/mscs721/concordance/1.0.0/locate" -H  "accept: application/json" -H  "Content-Type: text/plain" -d "Insert what you want returned in JSON concordance here."
```
This command will return a list of each token from the input string, similar to the response from the concordance, but with a 0-indexed location of that token's appearances within the string rather than the number of occurences.


## Deployment on the Cload Service(AWS EC2)

Choose an AMI, we used Microsoft Windows Server 2019 Base. Continue to configure your server, most importantly allowing inbound traffic on port 8080. RDP to the VM, cloning the application to the VM and installing software needed to run the applicataion on the server (Look at requirements above). Open the firewall settings for the VM and make sure to allow port 8080 for inbound and outbound traffic. Lastly, start up the swagger server and test to make sure everything is working as it should.


### Analyze and Locate Once Deployed

Similar to the execution above, just change localhost to the IPv4 public address or the IPv4 public DNS. In our case:

IPv4 public address: ```18.216.56.218```

IPv4 public DNS: ```ec2-18-216-56-218.us-east-2.compute.amazonaws.com```

## DynamoDB

Now communicates with AWS DynamoDB to store the data so the calculation only has to be done once. Also has save and compute flags that can be added to not store the results or to force calculate.

## uWSGI 

Added uWSGI implementation. Execute the following from root directory once uWSGI is installed to launch application:

```
uwsgi --http-socket :8080 --wsgi-file swagger_server/application.py
```