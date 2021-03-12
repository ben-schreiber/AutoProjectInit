import sys
import os
import json
import platform
from pathlib import Path
from github import Github


README_FILE = 'README.md'
TEMPLATE_DIR = 'template_files'
JSON_PROJECT_DIR = 'project_dir'
JSON_PROJECT_NAME = 'project_name'
JSON_GITHUB_TOKEN = 'TOKEN'
GITHUB_CREDENTIALS = 'git_credentials'
GITHUB_SERVER = 'github.com'
GITIGNORE_FILE = '.gitignore'


class ProjectCreator:

    CURRENT_DIR = Path(os.path.abspath(__file__)).parent
    CREDENTIALS_FILE = os.path.join(CURRENT_DIR, 'CREDENTIALS.json')

    def __init__(self, project_name: str):
        self.project_name: str = project_name
        self.project_dir: str = ProjectCreator.read_json_attribute(JSON_PROJECT_DIR)
        self.project_abs_path: str = os.path.join(self.project_dir, project_name)
        self.server: str = ''

    def push_local_repo(self, remote_link: str):
        """
        Pushes the local repo to the remote
        """

        os.chdir(self.project_abs_path)
        os.system(f'git remote add origin {remote_link} >> nul')
        os.system('git branch -M main >> nul')
        os.system('git push -u origin main >> nul')

    def init_remote_git(self) -> str:
        """
        Goes to github, inits a repo with the project name, returns the link
        Throws a ValueError if a repo already exists with that name
        """
        github_token = ProjectCreator.read_json_attribute(GITHUB_CREDENTIALS)[self.server]
        if self.server == GITHUB_SERVER:
            g = Github(github_token)
            user = g.get_user()
            repo = user.create_repo(self.project_name)
        else:
            g = Github(login_or_token=github_token, base_url=f'https://{self.server}/api/v3')
            user = g.get_user()
            repo = user.create_repo(self.project_name, private=True)
        return f'https://{self.server}/{user.login}/{self.project_name}.git'

    def init_local_git(self):
        """
        Inits a local git repository, adds all files to it, and commits
        """
        if platform.system() == 'Windows':
            nul_file = 'nul'
        else:
            nul_file = '/dev/null'

        os.chdir(self.project_abs_path)
        os.system(f'git init >> {nul_file}')
        os.system(f'git add . >> {nul_file}')
        os.system(f'git commit -m "Initial Commit" >> {nul_file}')

    def add_init_files(self):
        """
        Adds the README and .gitignore files
        """
        template_dir = os.path.join(ProjectCreator.CURRENT_DIR, TEMPLATE_DIR)

        gitignore_loc = os.path.join(template_dir, GITIGNORE_FILE)
        gitignore_dest = os.path.join(self.project_abs_path, GITIGNORE_FILE)
        os.system(f'cp {gitignore_loc} {gitignore_dest}')

        readme_loc = os.path.join(template_dir, README_FILE)
        readme_dest = os.path.join(self.project_abs_path, README_FILE)
        os.system(f'cp {readme_loc} {readme_dest}')

    def create_folder(self) -> bool:
        """
        Given the project name, attempts to create and cd into the folder.
        Returns True iff it successfully creates a folder and cds into it.
        If a folder with the project_name already exists, then return False
        """
        if os.path.isdir(self.project_abs_path):
            return False
        os.system(f'mkdir {self.project_abs_path}')
        print(self.project_abs_path)
        return True


    def first_half(self):
        if not self.create_folder():
            error_handling()
        self.add_init_files()
        self.init_local_git()

    def second_half(self):
        print('Which server would you like? (Type the number)\n')
        servers = ProjectCreator.read_json_attribute(GITHUB_CREDENTIALS).keys()
        servers_options = {}
        for i, _server in enumerate(servers):
            print(f' ({i + 1}) {_server}')
            servers_options[str(i + 1)] = _server
        choice = input()
        if choice not in servers_options:
            error_handling()
        self.server = servers_options[choice]
        remote_link = self.init_remote_git()
        self.push_local_repo(remote_link)


    @staticmethod
    def read_json_attribute(attribute):
        with open(ProjectCreator.CREDENTIALS_FILE) as f:
            data = json.load(f)
            return data[attribute]

    @staticmethod
    def write_json_attribute(attribute_name, value):
        with open(ProjectCreator.CREDENTIALS_FILE, 'r') as f:
            data = json.load(f)

        data[attribute_name] = value

        with open(ProjectCreator.CREDENTIALS_FILE, 'w') as f2:
            json.dump(data, f2)


def error_handling():
    print('error')
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        pc = ProjectCreator(sys.argv[1])
        pc.first_half()
        ProjectCreator.write_json_attribute(JSON_PROJECT_NAME, sys.argv[1])

    elif len(sys.argv) == 1:
        pc = ProjectCreator(ProjectCreator.read_json_attribute(JSON_PROJECT_NAME))
        pc.second_half()

    else:
        error_handling()
