
# Overview
cmigrate is an opensource project for migrating your VM to container.cmigrate is a commandline based tool wriitten in python which automatically discover the application runtime on the server and generate a docker file.

## Current release
---

We have shipped cmigrate with the below features :

- Automatic Environment discovery
- Option to select from multiple environment 
- Automatically collect the application related environment variable and configurations
- Generates docker file for containerization of the application 
- Support for multiple applications *


> 💡 *Currently cmigrate only support tomcat and Jboss.We will add support for more application in the forthcoming releases.


## Tech stack
cmigrate is build on below techstack
- Click python framework
- Jinja web template engine

xmigrate is a web application which run as a container in your local machine. 

All the code for cmigrate is written in python. Jinja is a web template engine for the Python programming language and it is used to create the template for generating docker file.Click is a Python package for creating beautiful command line interfaces.

## Future Roadmap
- Support for more applications.

## 🚀How to run? 

Run the xmigrate.py file.

if you have multiple application runtime running you can pass one in --runtime parameter.

Stay tuned for more updates. Join our [community](https://xmigrate.slack.com/) and start collaborating 🎉

