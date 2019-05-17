# Mozio_v0 project

## Contents

* [Requirements](#requirements)
* [Local development](#local-development)

## Requirements

* Ubuntu 16.04 (for deployment)
* Python 3.6 (make sure python header `python3.6-dev` files are installed)
* PostgreSQL >= 9.4 (9.6 is recommended)

## Local development

### Database setup

You can use whatever db user and db name you want, but we will use `mozio_v0` everywhere here.
```bash
sudo su - postgres
createuser mozio_v0 -DRSP  # Set mozio_v0 as a password
createdb mozio_v0 -O mozio_v0
```

### Git repo setup
```bash
git clone git@github.com:CrazyChief/mozio_v0.git
cd mozio_v0
```

> All the following commands are considered to be executed from the dir `mozio_v0` we've changed into in the step above, unless otherwise is specified.

### Local settings configuration
```bash
make environment
```

You have to edit `mozio_v0/.env` now, especially `DJANGO_SETTINGS_MODULE` you what to use, `DATABASES` settings, etc.

### Virtual environment activation

If you ever need to use some direct commands (not Makefile targets) you can simply activate virtual environment by the following:
```bash
source .env/bin/activate
```

### Install requirements
```bash
make requirements
```

### Create migrations
```bash
make migrations
```

### Apply migrations
```bash
make migrate
```

### Run tests
```bash
make test
```

### Create superuser
```bash
make superuser
```

### Run Django server
```bash
make run
```

## API endpoints description

#### Provider
* ```GET|POST /api/v0/providers/``` for listing and creating new Providers;

> For POST request you need to provide appropriate values in JSON format (ex. values):
```json
{
    "name": "some_name",
    "email": "some1email@gmail.com",
    "phone_number": "+345624568347",
    "language": "en",
    "currency": "USD"
}
``` 
* ```GET|PUT|PATCH|DELETE /api/v0/providers/<id>/``` for getting detail view, or editing and deleting Providers;

#### ServiceArea
* ```GET|POST /api/v0/service-areas/``` for listing and creating new ServiceAreas;

> For POST request you need to provide appropriate values in JSON format (ex. values):
```json
{
    "provider": 1,
    "polygon_name": "qwerty",
    "price": 20,
    "polygon": [
        [51.01564224011381, 29.76750033024507],
        [50.403427717842696, 29.59171908024507],
        [50.13658746370076, 30.84416048649507]
    ]
}
```
> Note: for polygon param you need to provide at least 3 pairs of values like provided above [longitude, latitude] pairs.

* ```GET|PUT|PATCH|DELETE /api/v0/service-areas/<id>/``` for getting detail view, or editing and deleting ServiceArea;

Also you can filter ServiceAreas provided ```pos``` param with appropriate [longitude, latitude] pair or pairs and get list of ServiceAreas with Provider name
* ```GET /api/v0/service-areas/?pos=[51.01564224011381,2029.76750033024507]```

>OR
* ```GET /api/v0/service-areas/?pos=[51.01564224011381,2029.76750033024507],[50.403427717842696,2029.59171908024507]```

As a result you will get a JSON with fields "polygon_name", "provider_name" and "price" like this:
```json
[
    {
        "polygon_name": "ajscnadfjsd",
        "provider_name": "qvkwencf",
        "price": "30.0000"
    }
]
```
