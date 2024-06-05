# git-sync
This script will clone and/or pull aribtrary remote repos in arbitrary local directories.  You only need to maintain a `repos.json` configuration file that is an array of JSON objects that map the remote repo name to a local directory.  Take a look at `repos.json` in this repo for an example configuration.

## Usage
To use, simply run the script and pass in the path to your `repos.json`:

```
python3 git_sync.py repos.json
```

## Requirements
This script uses GitPython, which can be installed with `pip`.
