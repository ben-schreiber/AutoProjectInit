import sys
import os
from pathlib import Path
import json
from constants import Constants
from github import Github


class ProjectCreator:

    def __init__(self, project_name: str):
        self.project_name: str = project_name
        self.project_dir: str = ''
        self.curr_path = Path(os.path.abspath(__file__))

    def push_local_repo(self, remote_link: str):
        """
        Pushes the local repo to the remote
        """
        os.chdir(self.project_dir)
        os.system(f'git remote add origin {remote_link} >> nul')
        os.system('git branch -M main >> nul')
        os.system('git push -u origin main >> nul')

    def init_remote_git(self) -> str:
        """
        Goes to github, inits a repo with the project name, returns the link
        Throws a ValueError if a repo already exists with that name
        """
        github_token = read_json_attribute(Constants.JSON_GITHUB_TOKEN)
        g = Github(github_token)
        user = g.get_user()
        repo = user.create_repo(self.project_name)
        return f'https://github.com/{user.login}/{self.project_name}.git'

    def init_local_git(self):
        """
        Inits a local git repository, adds all files to it, and commits
        """
        os.chdir(self.project_dir)
        os.system('git init >> nul')
        os.system('git add . >> nul')
        os.system('git commit -m "Initial Commit" >> nul')

    def add_init_files(self):
        """
        Adds the README and .gitignore files
        """
        template_dir = os.path.join(self.curr_path.parent, Constants.TEMPLATE_DIR)

        gitignore_loc = os.path.join(template_dir, Constants.GITIGNORE_FILE)
        gitignore_dest = os.path.join(self.project_dir, Constants.GITIGNORE_FILE)
        os.system(f'cp {gitignore_loc} {gitignore_dest}')

        readme_loc = os.path.join(template_dir, Constants.README_FILE)
        readme_dest = os.path.join(self.project_dir, Constants.README_FILE)
        os.system(f'cp {readme_loc} {readme_dest}')

    def set_project_dir(self, project_dir: str):
        self.project_dir = project_dir
        write_json_attribute(Constants.JSON_PROJECT_DIR, project_dir)

    def create_folder(self) -> bool:
        """
        Given the project name, attempts to create and cd into the folder.
        Returns True iff it successfully creates a folder and cds into it.
        If a folder with the project_name already exists, then return False
        """
        gparent_dir = self.curr_path.parent.parent
        project_dir = os.path.join(gparent_dir, self.project_name)
        if os.path.isdir(project_dir):
            return False
        self.set_project_dir(project_dir)
        os.system(f'mkdir {project_dir}')
        print(project_dir)
        return True


    def first_half(self):
        if not self.create_folder():
            error_handling()
        self.add_init_files()
        self.init_local_git()

    def second_half(self):
        self.project_dir = read_json_attribute(Constants.JSON_PROJECT_DIR)
        remote_link = self.init_remote_git()
        self.push_local_repo(remote_link)


def read_json_attribute(attribute):
    with open(Constants.CREDENTIALS_FILE) as f:
        data = json.load(f)
        return data[attribute]

def write_json_attribute(attribute_name, value):
    with open(Constants.CREDENTIALS_FILE, 'r') as f:
        data = json.load(f)

    data[attribute_name] = value
    with open(Constants.CREDENTIALS_FILE, 'w') as f2:
        json.dump(data, f2)


def error_handling():
    print('error')
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        pc = ProjectCreator(sys.argv[1])
        pc.first_half()
        write_json_attribute(Constants.JSON_PROJECT_NAME, sys.argv[1])

    elif len(sys.argv) == 1:
        pc = ProjectCreator(read_json_attribute(Constants.JSON_PROJECT_NAME))
        pc.second_half()

    else:
        error_handling()
