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

## API
### Public
Read only, anonymous access, all endpoints only support `GET` requests.

```
/service (Service)
    - name
    - description
    - components: (ServiceComponent) [
        - name
        - description
    ]
```

```
/policy (PolicyArea)
    - name
    - number
    - scope
    - category (PolicyCategory)
        - name
        - scope
```

```
/policy/{policy_id}/components (PolicyComponent)
    - name
    - description
    - type
    - options (PolicyComponentOption) [
        - value
    ]
```

```
/institution (Institution)
    - name
    - code
    - wikidata_id
```

```
/institution/{institution_id}/policy (InstitutionPolicyArea)
    # TODO: write these fields out 
    - __many__
```

```
/institution/{institution_id}/component/ (InstitutionPolicyComponent)
    - value
    - chosen_options []
    - comment
```


### Authenticated

```
/whoami (InstitutionUser) [GET]
    - user (User)
        - username
        - email
        - first_name
        - last_name
    - institution (Institution)
        - name
        - code
        - wikidata_id
```

```
/{type}/pack [GET]
    list all available question packs statuses
    # TODO: question order
    - name
    - type
    - size (i.e. number of questions)
    - answered (i.e. number of questions with answers)
```

```
/{type}/pack/{pack_id} [GET]
    get the details of a single pack
    - name
    - type
    - questions [
        - text
        - hint
        - type
        - required
        - options
        - answer: null or:
            - value
            - comment
    ]
```

```
/{type}/pack/answer/{question_id} [POST,DELETE]
    - value (could be single or multiple values)
    - comment
```
