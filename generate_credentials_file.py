FILE_CONTENTS = {
    "git_credentials":
        {
            "github.com": "",  # Add any other server, token pairs here
        },
    "project_dir": "",  # The directory where you wish to store your new project
}



if __name__ == '__main__':
    import os
    import json
    from pathlib import Path

    file_name = os.path.join(Path(os.path.abspath(__file__)).parent, 'CREDENTIALS.json')

    with open(file_name, 'w') as f:
        json.dump(FILE_CONTENTS, f)

