import sys
import os

from shutil import copy2
from pathlib import Path
from github import Github
from dotenv import load_dotenv


README_FILE = 'README.md'
TEMPLATE_DIR = 'template_files'
GITHUB_SERVER = 'github.com'
GITIGNORE_FILE = '.gitignore'


class ProjectCreator:

    def __init__(self, project_name: str):
        self.current_dir: str = Path(os.path.abspath(__file__)).parent
        self.project_name: str = project_name
        self.project_dir: str = os.getenv('PROJECT_DIRECTORY')
        self.project_abs_path: str = os.path.join(self.project_dir, self.project_name)
        self.server: str = ''
        self.servers: dict = {}

    def push_local_repo(self, remote_link: str):
        os.chdir(self.project_abs_path)
        os.system(f'git remote add origin {remote_link}')
        os.system('git branch -M main')
        os.system('git push -u origin main')

    def init_remote_git(self) -> str:
        github_token = self.servers[self.server]
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
        os.chdir(self.project_abs_path)
        os.system(f'git init')
        os.system(f'git add .')
        os.system(f'git commit -m "Initial Commit"')

    def add_init_files(self):
        template_dir = os.path.join(self.current_dir, TEMPLATE_DIR)

        gitignore_src = os.path.join(template_dir, GITIGNORE_FILE)
        gitignore_dest = os.path.join(self.project_abs_path, GITIGNORE_FILE)
        copy2(gitignore_src, gitignore_dest)

        readme_src = os.path.join(template_dir, README_FILE)
        readme_dest = os.path.join(self.project_abs_path, README_FILE)
        copy2(readme_src, readme_dest)

    def create_folder(self) -> bool:
        if os.path.isdir(self.project_abs_path):
            return False
        os.makedirs(self.project_abs_path)
        return True

    def get_server_choice(self):
        msg: str = 'Which server would you like? (Type the number)'
        print('\n' + '=' * len(msg))
        print(msg + '\n')
        self.process_servers()
        servers_list = list(self.servers.keys())
        for i, _server in enumerate(servers_list):
            print(f' ({i + 1}) {_server}')
        print('=' * len(msg))
        choice = eval(input())
        if choice > len(servers_list) or choice < 1:
            error_handling('Invalid Server Choice.')
        self.server = servers_list[choice - 1]

    def run(self):
        if not self.create_folder():
            error_handling(f'Project with the name `{self.project_name}` already exists')
        self.add_init_files()
        self.init_local_git()
        self.get_server_choice()
        self.push_local_repo(self.init_remote_git())

    def process_servers(self):
        env_info = os.environ.get('GITHUB_CREDENTIALS')  # Come in the form: [(server, token), ...]
        server_token_pairs = env_info.split(';')
        for pair in server_token_pairs:
            server, token = pair.strip()[1:-1].split(',')
            self.servers[server.strip()] = token.strip()


def error_handling(msg: str = ''):
    if len(msg) > 6:
        print('=' * len(msg))
    else:
        print('=' * 6)

    print('Error!')
    if msg:
        print(msg)

    if len(msg) > 6:
        print('=' * len(msg))
    else:
        print('=' * 6)
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        load_dotenv()
        pc = ProjectCreator(sys.argv[1])
        pc.run()
    else:
        error_handling('USAGE: source create_project <project_name>')
