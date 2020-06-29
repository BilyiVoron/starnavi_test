# starnavi_test
 
 # INSTRUCTIONS

# Setup

#### Create local env file

Just run `make test_env`


#### Build containers

`docker-compose -f docker-compose-dev.yml build` or `make build_compose`

#### Remove containers

`docker-compose -f docker-compose-dev.yml down --remove-orphans` or `make stop_compose`

#### Before running project

- Create local env file
- Build containers
- Run project

#### Run project

`docker-compose -f docker-compose-dev.yml up` or `make start_compose`


#### When project is running

- Apply db migrations `make migrations`
- Create superuser `make test_user`. After that you'll be able to login into Admin
- Be happy :)

#### Create new app

`make app name=<app_name>`

# Testing

- Import JSON-file 'Insomnia_2020-06-29.json' to Insomnia to test API endpoints 
- Run tests `make pytest`


### Project description

This is simple project just to demonstrate basic concept of Django.
Social network for Starnavi's test task includes such features as:
 - user signup/login/logout via simple UI
 - user signup via Facebook or other the most popular social networks
 - post create, update, delete
 - comment create, update, delete
 - possibility to comment post
 - possibility add or remove likes to posts and comments
 - possibility to see who has liked user's posts or comments (only for object's owner)
 - Swagger Docs
 - Docker
 * Also wrote unit test using Django Tests and pytest for every API endpoint

- You are able to see Django Admin and create some posts and comments in DB.


#### All commands you can find in `Makefile`
