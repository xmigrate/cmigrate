
# Overview
Cmigrate is an open-source project for migrating your VM-based application deployments to container. Cmigrate is a CLI based tool wriitten in python which can discover the application runtime on the server and generate a docker file and the application artifacts to containerize.

![demo-tomcat-cmigrate](https://user-images.githubusercontent.com/67468756/203218711-80d74f32-874c-433b-aa35-2675dc97aeaf.gif)


## Current release
---

We have shipped cmigrate with the following features :

- Automatic Environment discovery
- Option to select from multiple environments 
- Automatically collect the application-related environment variable and configurations
- Generates docker file for containerization of the application 
- Support for tomcat and jboss based application


> 💡 *Currently cmigrate only support tomcat and Jboss. We will add support for more application in the forthcoming releases.


## Tech stack
Cmigrate is build on the below tech stack
- Click python framework
- Jinja web template engine


All the code for cmigrate is written in python. Jinja is a web template engine for the Python programming language and it is used to create the template for generating a docker file. Click is a Python package for creating command-line interfaces.

## Future Roadmap
- Support for more applications runtimes

## 🚀How to run? 

Run the cmigrate.py file.

```
python3 cmigrate.py
```

if you have multiple application runtime running you can pass one in --runtime parameter.

Stay tuned for more updates 🎉

