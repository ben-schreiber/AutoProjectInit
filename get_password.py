if __name__ == '__main__':
    import json

    with open('CREDENTIALS.json') as f:
        print(json.load(f)['PASSWORD'])
