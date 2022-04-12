# DiSSCo Self-Assessment Tool

## Installation
From the root of this repo (so one up from here):

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -e .
```

To install the test dependencies:

```bash
pip install -e .[test]
```

## Useful commands
Each of these should be run from within this directory. 

```bash
# load policy model
./manage.py loaddata policy_v1.yaml

# load institutions - codes should be a list of institution codes, for example NHMUK WAG MfN
./manage.py populate <codes>
```
