# DiSSCo Self-Assessment Tool

## Installation
From the root of this repo (so one up from here):

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .
```

To install the test dependencies:

```bash
pip install -e .[test]
```

## Useful commands
Each of these should be run from within this directory. 

```bash
# load base data
./manage.py loaddata policy/fixtures/elvis/**/*.yaml common/fixtures/**/*.yaml
```
