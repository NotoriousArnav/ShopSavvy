# ShopSavvy: Store management software (Backend)
ShopSavvy is a store management software made using FastAPI and MongoDB to manage your store data, privately and securely.

## Features
The Features of ShopSavvy are as follows:
- **Privacy Focused**
We are focused on privacy, because we know that your data is important.
- **Secure**
We use Several Security Measures to protect your data, including User Roles and Short-lived JWT Tokens
- **Fast**
We use FastAPI for the backend, and MongoDB for the database, which is fast and reliable.
- **Scalable**
Our Choice of using FastAPI and MongoDB, makes it possible to operate severlessly for scalable applications.
- **Open Source**
This is open source and free to use.

## Prerequisites
- git
- Python 3.11
- pipenv
- MongoDB URI in .env
- Randomly generated SECRET_KEY in .env

## Setting up .env
1. Make a File Called .env
2. Add: `MONGO_URI="mongodb://yourdbhost:port"`
3. Generate a Randomly generated SECRET_KEY using `openssl rand -hex 32` and copy it
4. Add: `SECRET_KEY="that randomly generated secret key you copied"`

## Installation
```bash
pip install pipenv
```
```bash
pipenv install
```

## Usage
```bash
pipenv run start # start_all for starting on all interfaces
```

## Documentation
Documentation is available at [docs.md](docs.md) and at `/docs` and `/redoc` routes.

## [License](LICENSE)
This project is licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
