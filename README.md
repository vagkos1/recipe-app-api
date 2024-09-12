# recipe-app-api
Recipe API project

### Linting

- Use flake8
- Run linting through Docker Compose
- Exclude some files app/.flake8 to only lint our code

```text
docker-compose run --rm app sh -c "flake8"
```

## Testing
- Django test suite
- Setup tests per Django app
- Run tests through Docker Compose

### Run tests

```text
docker-compose run --rm app sh -c "python manage.py test"
```

### Create Django project

```text
docker-compose run --rm app sh -c "django-admin startproject app ."
```

### Run the project

```text
docker-compose up"
```

### Github Actions
configured in `.github/workflows/checks.yml`
We'll set triggers
We'll also add steps for running tests and linting

### Dockerhub
- pull base images
- We shoud be fine with regards to rate limits
    - Anonymous (some IP): 100/6h
    - Authenticated: 200/6h
- GitHub Actions uses shared IP addresses
    - Limit applied to all users
- So we'll authenticate with DockerHub to get 200 pulls per 6h all to ourselves!

so, the steps are:
1. register acount in https://hub.docker.com/
2. use `docker login` during our job
3. add secrets to GitHub project (DOCKERHUB_TOKEN and DOCKERHUB_USER)  
(secrets are encrypted and they are decrypted when needd in actions)