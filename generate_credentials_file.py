


file_contents = {
    "git_credentials":
        {
            "github.com": "",  # Add any other server, token pairs here
        },
    "project_dir": "",  # The directory where you wish to store your new project
    "project_name": ""  # No need to fill this in
}



if __name__ == '__main__':
    import os
    from pathlib import Path

    file_name = os.path.join(Path(os.path.abspath(__file__)).parent, 'CREDENTIALS.json')

    with open(file_name, 'w') as f:
        json.dump(file_contents, f)

