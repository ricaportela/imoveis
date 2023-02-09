.SILENT:

SHELL = /bin/bash

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m

## Prints this help
help:
	printf "${COLOR_YELLOW}\nExtranet ESTAVOS\n----------------\n\n${COLOR_RESET}"
	awk '/^[a-zA-Z\-\_0-9\.%]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "${COLOR_GREEN}$$ make %s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort
	printf "\n"

## Install project dependencies
setup:
	pip install -r requirements.txt
	python ./manage.py loaddata start_data.json
	python ./manage.py loaddata ad_example_data.json

## Runs the project
run:
	python ./manage.py runserver

## Runs the project unit tests
test:
	python ./manage.py test

## create automatic migrations
makemigrations:
	python ./manage.py makemigrations

## Runs migrations
migrate:
	python ./manage.py migrate

## Deploy application
deploy:
	fab deploy
