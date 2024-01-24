# SATD GIT Extractor

A Python project for extracting additional data from GIT repositories of a selection Apache OSS projects in the SATD dataset.

- [SATD Dataset Project](https://github.com/yikun-li/satd-different-sources-data)
- [Dataset](https://github.com/yikun-li/satd-different-sources-data/blob/c3c13955ce6c3e68f98fa08829adf41f37281b9a/satd-dataset-commit_messages.csv)

A dataset containing listings of Apache repositories is provided under [resources](./resources).

> [!NOTE]
> [PyDriller](https://github.com/ishepard/pydriller) library is used for extracting data from GIT repositories.
> It does not handle well commits that are merged from a fork of a repository.

## Usage

Data extraction will output a CSV file per extracted directory.

```shell
python -m satd_git_extractor extract --repositories repos.csv --commits satd-dataset-commit_messages.csv --exports-dir export --clone-dir repos
```

Merge the extracted data into the SATD CSV file.

```shell
python -m satd_git_extractor merge --commits satd-dataset-commit_messages.csv --exports-dir export --output satd-commits-merged-dataset.csv
```

## Initialize Project

> [!NOTE]
> The following instructions are for Windows using [virtual environment](https://docs.python.org/3/library/venv.html).
> The [Python version](./.python-version) is specified for [PyEnv](https://github.com/pyenv/pyenv).

Initialize Python virtual environment.

```shell
python -m venv env
```

Activate the environment.

```powershell
.\env\Scripts\Activate.ps1
```

Install dependencies.

```shell
pip install -r requirements.txt
```

Install the project (in editable mode).

```shell
pip install --editable .
```
