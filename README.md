# Project Auto Initializer
## Overview
This script accomplishes the following:\
Given a github (server, token) pair and your project directory, it will run a script that
> (1) creates a new local project repository with a .gitignore and README.md file, 

>(2) inits said
repository as a git repo, 

> (3) inits a remote repository with the same name on the given github server,

> (4) pushes the new local repo to the remote repo, and 

>(5) navigates to your new project.

## Setup
Before running the script, you need to setup a few things. 
### Virtual Environment
First, create and activate a virtual environment.
Navigate to this project's directory, and run the following commands:
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
or, if you are on a Windows machine:
```bash
source venv/Scripts/activate
```
### Credentials File
In order for the script to run, it needs two pieces of information: the path of the directory in which you store all of your projects, and the (github server, account token) pair for the desired github account you wish to push your project to.\
First, open `generate_credentials_file.py` and add in the path to your projects directory and the github server and token. In order to generate a token, 
