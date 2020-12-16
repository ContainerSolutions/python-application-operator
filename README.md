# python-application-operator

<h1>This is proof of concept</h1>

## Description

This project is using [Canonical Operator Framework](https://github.com/canonical/operator) 

The main idea is to simplify python application deployment by using 
[Gunicorn](https://gunicorn.org/) to serve it to the internet  

## Requirements

- Install and bootstreap k8s with juju (https://juju.is/docs/kubernetes)
- Install charmcraft with `sudo snap install charmcraft`.

## Usage

1. Build charm `charmcraft build`
2. Deploy charm `juju deploy ./python-application-operator.charm --config examples/config_site1.yaml`

## Configuration

- Python: Charm can use any official python image based on ubuntu which can be defied as `image` parameter  
- Repostiory: Currently only publicly available (or without authorization) repositores are supported
- Entrypoint: Application shoul be prepared to work with WSGI servers and application entrypoint shold be provided. 
  - Django example: https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/gunicorn/
  - Flask Example: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
  

## Configuration

Read [config.yaml](config.yaml)

## Examples

Sample application that are were tested:
- https://github.com/kirek007/python-hello-web
  
  To deploy use `juju deploy ./python-application-operator.charm --config examples/config_flask.yaml`
  
- https://github.com/django-ve/django-helloworld

  To deploy use `juju deploy ./python-application-operator.charm --config examples/config_django.yaml`




## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Testing

Tests are not implemented but scaffolding is ready 

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests
