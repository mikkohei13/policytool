#!/bin/bash

cd dissco
python manage.py migrate
python manage.py loaddata policy/fixtures/elvis/**/*.yaml common/fixtures/**/*.yaml maturity/fixtures/**/*.yaml
