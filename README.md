# Sagemaker examples and projects

This is a personal project to practice Object Detection techniques using AWS SageMaker.
## Installation

There are several dependen
Dependencies

```
apt-get update 
apt-get install -y curl git vim wget \ 
    python-setuptools python-dev build-essential && \
    easy_install pip 
pip install sagemaker awscli
```

then, run:
```
aws configure 
```
or alternatively if you want to execute it using different AWS profile:
```
aws configure --profile sagemaker
```

Your configuration should look like that (with the real keys of course):
```
$ aws configure --profile sagemaker
AWS Access Key ID [None]: <accesskey>
AWS Secret Access Key [None]: <secretkey>
Default region name [None]: us-east-1
Default output format [None]:
```

# Overview
scripts/inferences.py - Inference the image agains an endpoint. Can be used stand alone and also as a library.
 
scripts/plot_result.py - A utility that helps to plot the results. 

# Usage 
To inference an image from command line, use the following syntax:
```
inferences.py [-h] [-d DATA_TYPE] filename endpoint
```
Example for that can look like that:
```
python inferences.py ../images/4.0-13.6.10.png myendpoint
```

