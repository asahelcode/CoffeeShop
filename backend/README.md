# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Using .env File for Environmental Variables

1. Create an empty file named `.env` in `./backend/src/.env`
2. Edit the .env file and add your Variables:
    - AUTH0_DOMAIN
    - ALGORITHMS
    - API_AUDIENCE
    e.g
    ```bash
        FLASK_APP="flaskr"
        FLASK_ENV="development"
        AUTH0_DOMAIN="<YOUR_AUTH0_DOMAIN>"
        ALGORITHMS="<YOUR_AUTH0_ALGORITHMS> e.g RS256"
        API_AUDIENCE="<AUTH0_AUDIENCE>"
    ```
3. Go to [Flask Auth0 Documentation](https://auth0.com/docs/quickstart/backend/python/01-authorization)


## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`
     - can `get:drinks`
   - Manager
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`


## Endpoint Documentation

### GET `/drinks`
- Request arguments: None.
- Response:  An object with these keys:
  - `drinks`: Contains a object of `id` and `recipe:list of key value pairs`.

```json
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "blue",
          "parts": 1
        }
      ],
      "title": "water"
    },
    {
      "id": 2,
      "recipe": [
        {
          "color": "yellow",
          "parts": 1
        }
      ],
      "title": "Tuwo"
    },
    {
      "id": 3,
      "recipe": [
        {
          "color": "brown",
          "parts": 1
        }
      ],
      "title": "Miya"
    },
    {
      "id": 4,
      "recipe": [
        {
          "color": "ash",
          "parts": 1
        }
      ],
      "title": "Cola"
    }
  ],
  "success": true
}
```


### GET `/drinks-detail`
- Require Authentication.
- Response:  An object with these keys:
  - `drinks`: Contains a object of `id` and `recipe:list of key value pairs`.

```json
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "blue",
          "name": "water",
          "parts": 1
        }
      ],
      "title": "water"
    },
    {
      "id": 2,
      "recipe": [
        {
          "color": "blue",
          "parts": 1
        }
      ],
      "title": "Tuwo"
    }
  ],
  "success": true
}
```

### POST `/drinks`
- Require Authentication.
- Request Body:
  - `title` (char) - The Title
  - `recipe` (list) - list containing objects of recipe
- Request Body SAMPLE:
```json
{
	"title": "Cola",
	"recipe": [
		{
			"color": "ash",
			"parts": 1
		}
	]
}
```
- Response:  An object with these keys:
  - `drinks`: Contains a object of `id` and `recipe:list of key value pairs`.
```json
{
  "drinks": [
    {
      "id": 4,
      "recipe": [
        {
          "color": "ash",
          "parts": 1
        }
      ],
      "title": "Cola"
    }
  ],
  "success": true
}
```

### PATCH `/drinks/<int:id>`
- Require Authentication.
- Request Argument:
   - `id` (int) ID of the Intended drink to update
- Request Body:
  - Object with key value pair of what to update
- Response:
  - Returns the updated instance and success flag

```json
{
  "drinks": [
    {
      "id": 2,
      "recipe": [
        {
          "color": "yellow",
          "parts": 1
        }
      ],
      "title": "Sabon title"
    }
  ],
  "success": true
}
```


### DELETE `/drinks/<int:id>`
- Require Authentication.
- Request Argument:
   - `id` (int) ID of the Intended drink to update
- Response:
  - Returns the delete instance id and success flag
```json
{
  "delete": 4,
  "success": true
}
```
