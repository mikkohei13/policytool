# DiSSCo Policy Tool
[![DOI](https://zenodo.org/badge/409189014.svg)](https://zenodo.org/badge/latestdoi/409189014)

A tool allowing DiSSCo partners to self-assess their alignment with the DiSSCo policies that govern the various DiSSCo services.

## Setup (preliminary)

- `docker compose up; docker compose down;`
- Create superuser with `docker compose exec -e DJANGO_SETTINGS_MODULE=dissco.settings.docker backend python dissco/manage.py createsuperuser`
- Login to http://localhost:5000/admin to setup user and institution
- Clear cookies if yoh have logged in, and login again

## Key Documents

User Stories and Requirements Document: https://docs.google.com/spreadsheets/d/1EG8DRhbr5_bT_P2c19DXozxd1s1f4wIcErIgvTxeY0w/edit?usp=sharing

Meeting Notes: https://docs.google.com/document/d/13UtDedI7uyYYL2sDtE903iTHRILvGq0kcNUhqfBkY50/edit

## DiSSCo Milestones
MS7.5 DiSSCo Policy Tool Design Blueprint: https://drive.google.com/file/d/1r6dXM9ec9gHXlzlbp1pdeGh3SP9kjHaY/view?usp=sharing

MS3.2 DiSSCo Digital Maturity Tool Design Blueprint: https://drive.google.com/file/d/1WlBwiheB0GgxB45AoFIgWi8LL4QpbGWi/view?usp=sharing

## Prior Work

ICEDIG Policy Dashboard and findings (a framework for comparing relevant institutional policies) - https://icedig.eu/content/policy-analysis.

SYNTHESYS+ Task 2.1 Policy Metadata schema (still in development): https://drive.google.com/file/d/1oOEG1a3zalm-5mjVGOGJYlUOc4o6zMgt/view?usp=sharing.
