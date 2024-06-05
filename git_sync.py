import argparse
import json
import git
import os


def read_json(path):
    data = None
    if os.path.exists(path):
        with open(path, 'r') as fh:
            data = json.load(fh)
    return data


def expand(path):
    path = os.path.expanduser(path)
    path = os.path.realpath(path)
    path = os.path.abspath(path)
    return path


def mkdir(path):
    return os.makedirs(path, exist_ok=True)


class GitSync:
    def __init__(self, repos_conf):
        self.repos = read_json(repos_conf)

    def clone(self, remote, local):
        git.Repo.clone_from(f"git@github.com:{remote}.git", local)

    def local_repo_exists(self, local):
        return os.path.exists(os.path.join(local, ".git"))

    def local_repo_config(self, local):
        repo = git.Repo(local)
        return repo.config_reader()

    def get_primary_branch(self, config):
        contains_main = False
        contains_master = False
        for section in config.sections():
            if "branch" in section:
                if "\"main\"" in section:
                    contains_main = True
                if "\"master\"" in section:
                    contains_master = True
                if contains_master and contains_main:
                    break
        branch = "main"
        # default to 'main' unless it 'master' is the only branch
        if contains_master:
            if not contains_main:
                branch = "master"
        return branch

    def pull(self, local):
        repo = git.Repo(local)
        config = self.local_repo_config(local)
        branch = self.get_primary_branch(config)
        repo.git.checkout(branch)
        origin = repo.remotes.origin
        origin.pull(branch)

    def sync(self):
        for repo in self.repos:
            local = expand(repo["local_repo"])
            print(local)
            remote = repo["remote_repo"]
            if self.local_repo_exists(local):
                print(f"[*] refreshing {remote}")
                self.pull(local)
            else:
                print(f"[*] cloning {remote}")
                self.clone(remote, local)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repos", help="/path/to/repos.json")
    args = parser.parse_args()

    gs = GitSync(args.repos)
    gs.sync()


if __name__ == "__main__":
    main()
