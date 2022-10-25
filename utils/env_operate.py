import os

def get_develop_env():
    develop_env = os.environ["DEVELOP_ENV"]
    return develop_env


if __name__ == "__main__":
    develop_env = get_develop_env()
    print(develop_env)