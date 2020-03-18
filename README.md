# bb-admin

**bb-admin** is a commandline tool that bitbucket admins can use to create (and eventually maintain) repositories in bitbucket using yaml configurations to declare default reviewers, branching permissions, and all sorts of neat jazz. It is intended to be a python executable that can be run from anywhere, even _inside_ a repo directory.

## Getting Started

* Clone this repository and copy to a new working directory for your project
* Go through the installation instructions and ensure it works as-is
* Profit! (Draw the rest of the owl)

### Prerequisites

* A working python3 installation
* Internet access to pull libraries.

### Installing locally

#### Setup a virtual environment via `virtualenv`
```
╭─jaygentile at AUS-0498 in ~/repos
╰─○ virtualenv -p /usr/local/bin/python3 .bb-admin
Running virtualenv with interpreter /usr/local/bin/python3
Already using interpreter /usr/local/opt/python/bin/python3.7
Using base prefix '/usr/local/Cellar/python/3.7.4_1/Frameworks/Python.framework/Versions/3.7'
New python executable in /Users/jaygentile/repos/.bb-admin/bin/python3.7
Also creating executable in /Users/jaygentile/repos/.bb-admin/bin/python
Installing setuptools, pip, wheel...
done.

╭─jaygentile at AUS-0498 in ~/repos
╰─○
```
#### Activate virtual environment via `source`
```
╭─jaygentile at AUS-0498 in ~/repos
╰─○ source .bb-admin/bin/activate

╭─jaygentile at AUS-0498 in ~/repos
╰─(.bb-admin) ○
```
#### Install package (from inside repo dir) via `pip`
```
╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─(.bb-admin) ± pip install --editable .
Obtaining file:///Users/jaygentile/repos/cops-bb-admin
Collecting Click==7.0
  Using cached Click-7.0-py2.py3-none-any.whl (81 kB)
Processing /Users/jaygentile/Library/Caches/pip/wheels/8a/55/a4/c0a81d27c33462cfdcb904db018f5550197e88b2b6b85beed2/PyYAML-5.3-cp37-cp37m-macosx_10_14_x86_64.whl
Collecting requests==2.23.0
  Using cached requests-2.23.0-py2.py3-none-any.whl (58 kB)
Collecting deepmerge==0.1.0
  Using cached deepmerge-0.1.0-py2.py3-none-any.whl (9.3 kB)
Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1
  Using cached urllib3-1.25.8-py2.py3-none-any.whl (125 kB)
Collecting chardet<4,>=3.0.2
  Using cached chardet-3.0.4-py2.py3-none-any.whl (133 kB)
Collecting idna<3,>=2.5
  Using cached idna-2.9-py2.py3-none-any.whl (58 kB)
Collecting certifi>=2017.4.17
  Using cached certifi-2019.11.28-py2.py3-none-any.whl (156 kB)
Installing collected packages: Click, PyYAML, urllib3, chardet, idna, certifi, requests, deepmerge, bb-admin
  Running setup.py develop for bb-admin
Successfully installed Click-7.0 PyYAML-5.3 bb-admin certifi-2019.11.28 chardet-3.0.4 deepmerge-0.1.0 idna-2.9 requests-2.23.0 urllib3-1.25.8

╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─(.bb-admin) ±
```

## Execution
### Dockerized

* Login to ecr in the dev aws account

```
╭─jaygentile at AUS-0498 in ~
╰─○ aws ecr get-login --no-include-email --region us-east-1 --profile dev |bash
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
Login Succeeded
╭─jaygentile at AUS-0498 in ~
╰─○
```

* Run via docker commandline

```
╭─jaygentile at AUS-0498 in ~
╰─○ docker run -it 386123533085.dkr.ecr.us-east-1.amazonaws.com/cops/bb-admin:0.1.0 --help
Unable to find image '386123533085.dkr.ecr.us-east-1.amazonaws.com/cops/bb-admin:0.1.0' locally
0.1.0: Pulling from cops/bb-admin
c7b7d16361e0: Pull complete
b7a128769df1: Pull complete
1128949d0793: Pull complete
667692510b70: Pull complete
bed4ecf88e6a: Pull complete
8a8c75f3996a: Pull complete
10b7379e5573: Pull complete
ca1b6fe24628: Pull complete
9a90211ec083: Pull complete
a9acf0e2fe7f: Pull complete
7440b795df4f: Pull complete
ce7978baba17: Pull complete
Digest: sha256:f3a8999a3d09138f3c7b4f1cb5df475f6ddc3157b0f29409829226ab0f051cbf
Status: Downloaded newer image for 386123533085.dkr.ecr.us-east-1.amazonaws.com/cops/bb-admin:0.1.0
Usage: bb-admin [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  Show the version and exit.
  --help         Show this message and exit.

Commands:
  create  Command on cli1
  delete  Delete has not yet been implemented and exists only as an example.
╭─jaygentile at AUS-0498 in ~
╰─○
```
* Run subcommands

```
╭─jaygentile at AUS-0498 in ~
╰─○ docker images
REPOSITORY                                                   TAG                 IMAGE ID            CREATED             SIZE
386123533085.dkr.ecr.us-east-1.amazonaws.com/cops/bb-admin   0.1.0               c5cd67443064        14 minutes ago      930MB

╭─jaygentile at AUS-0498 in ~
╰─○ docker run -it c5cd create --help
Usage: bb-admin create [OPTIONS]

  Command on cli1

Options:
  -l, --login TEXT    Bitbucket cloud login - eg yourname@socialsolutions.com
  -p, --project TEXT  Project string in Bitbucket this repo will belong to (eg
                      DATA for 360 Data Pipeline, DO for devops)  [required]
  -r, --repo TEXT     The name (eg cops-bb-admin) to create  [required]
  -f, --force         Force execution if repo already exists in BitBucket
  --help              Show this message and exit.

╭─jaygentile at AUS-0498 in ~
╰─○
```

### Non-Dockerized
#### Execute via bb-admin cmdline call:
```
╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─(.bb-admin) ± bb-admin --help
Usage: bb-admin [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  Show the version and exit.
  --help         Show this message and exit.

Commands:
  create  Command on cli1
  delete  Delete has not yet been implemented and exists only as an example.

╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─(.bb-admin) ±
```
```
╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─(.bb-admin) ± bb-admin create --help
Usage: bb-admin create [OPTIONS]

  Command on cli1

Options:
  -l, --login TEXT    Bitbucket cloud login - eg yourname@socialsolutions.com
  -p, --project TEXT  Project string in Bitbucket this repo will belong to (eg
                      DATA for 360 Data Pipeline, DO for devops)  [required]
  -r, --repo TEXT     The name (eg cops-bb-admin) to create  [required]
  -f, --force         Force execution if repo already exists in BitBucket
  --help              Show this message and exit.

╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─(.bb-admin) ±
```

#### Deactivate your virtual environment via `deactivate` when finished
```
╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─(.bb-admin) ± deactivate

╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─±
```

## Adding/modifying configs
* The current structure for configurations is `./config/{project}/{project}.yml`

  For example, the "universal-reporting-web" repo lives in a project named "SSG Platform", at https://bitbucket.org/account/user/social-solutions/projects/SP. Therefore its config will live in `./config/sp/sp.yml` (lowercase matters).
* Any value that is _not_ an array in the global config file (`./config/socialsolutions.yml`) can be overridden in the project config.

  For example, if we want universal-reporting-web's `dev` environment to be named `joesenvironment` we can override that in sp.yml with:
```
pipelines-environments:
    dev:
        name: joesenvironment
```
* **ARRAYS** are additive (and eventually deduplicated). For example, default-reviewers in a project get APPENDED to the global default-reviewers in socialsolutions.yml
* All of the configs in this repo have been created using references generated by curling the BitBucket API then converted from json to yaml. Here's an example for GETting the branch-restrictions of apricot:

```
± curl -H "Content-Type: application/json" -u myuser@socialsolutions.com:mypassword 'https://api.bitbucket.org/2.0/repositories/social-solutions/apricot/branch-restrictions' |jq
{
  "pagelen": 10,
  "size": 25,
  "values": [
    {
      "kind": "reset_pullrequest_approvals_on_change",
      "users": [],
      "links": {
        "self": {
          "href": "https://api.bitbucket.org/2.0/repositories/social-solutions/apricot/branch-restrictions/4147433"
        }
      },
      "pattern": "master",
      "value": null,
      "branch_match_kind": "glob",
      "groups": [],
      "type": "branchrestriction",
      "id": 4147433
    },
```

  From here we can convert to yaml and strip out things we don't care about (`values[0].links.self.href & values[0].id`)

## Running the tests

### From the repo root, run python to execute tests via discovery (make sure you're using the virtualenv)

```
╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─(.bb-admin) ± python -m unittest discover tests -v
test_cli_help_execute (test_clirun.TestCliRunOkay)
Test that cli can actually execute ... ok
test_reject_nonadmin (test_create_lib.TestsNotOkay)
Test that non-admins get sys.exit()ed ... User does not appear to be an admin.
ok
test_create_obj (test_create_lib.TestsOkay)
Test that created object is a CreateRepo, a subclass of BitBucketAdmin ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.367s

OK

╭─jaygentile at AUS-0498 in ~/repos/cops-bb-admin on master
╰─(.bb-admin) ±
```

### Test recommendations

* Every method you add, when possible, should have tests
* The cli execution itself should be tested as well

## Deployment

N/A

## Built With

N/A

## Contributing

* See Adding/modifying configs section for config changes
* Play with this, expand upon this, break this, add tests to this, do anything you want. Please just put up a PR.
* **version bumps must happen in setup.py** - this file is everything. It's even where the tag for the docker image comes from.

## Versioning

###### Use [SemVer](https://semver.org/) (Major.Minor.Patch) to version your repository.  

* A bugfix is a patch bump.
* A new feature is a minor bump.
* Broken backwards-compatibility is a major bump.

## Authors

* **Jay Gentile** - *Initial functionality*

## License

N/A

## Acknowledgments

* [Bitbucket API 2.0](https://developer.atlassian.com/bitbucket/api/2/reference/resource/)
* [README.md template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [Click7 Quickstart](https://click.palletsprojects.com/en/7.x/quickstart/)
* [Testing Click Applications](https://click.palletsprojects.com/en/7.x/testing/)
* Coffey is awesome
* Brasewel is also awesome
