# Project Auto Initializer
**Note:** This script can only be run on a `bash` terminal. If you are using a Windows machine, you can run this script from a `bash` emulator such as the Git Bash Terminal.
## Overview
This script accomplishes the following:\
Given a github (server, token) pair and your project directory, it will run a script that
> (1) creates a new local project repository with a `.gitignore` and `README.md` file, 

> (2) inits said repository as a git repo, 

> (3) inits a remote repository with the same name on the given github server,

> (4) pushes the new local repo to the remote repo, and 

> (5) navigates to your new project.

## Setup
In order to get this project up and running, run the following commands:
```bash
git clone "https://github.com/schreiberben/AutoProjectInit.git"
cd AutoProjectInit
```
At this point, you can create/activate a virtual environment if you so please.

```bash
pip install -r requirements.txt
touch .env
```

Now, open the .env file and add in the necessary items (see below for more details).
## Usage
```bash
source create_project <project_name>
```

## `.env` File Format
The `.env` file holds two variables: 
1. `PROJECT_DIRECTORY` ~ The directory in which you want your new projects to be saved.
2. `GITHUB_CREDENTIALS` ~ A list of github servers and tokens to use. In order to generate a token for your account, follow the instructions [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token "Access Token Instructions"). You should save the in server-token pairs in the following format: (server1, token1);(server2, token2);...\
**Note:** The `.env` file is part of your `.gitignore` file, so it won't be saved anywhere other than locally on your computer.

### Example File
```
GITHUB_CREDENTIALS="(github.com, abcdefghijklmnopqrstuvwxyz);(github.cs.huji.ac.il, zyxwvutsrqponmlkjihgfedcba)"
PROJECT_DIRECTORY="C:\\Users\\<Username>\\Projects\\"
```
