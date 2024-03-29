# Tally

Tally is the backend for tracking transactions for various products sold at the study association. In addition to products, other expenses that are not linked to a product can also be tracked here. An export can be made of the products sold in a certain time period.

<!-- TOC start -->

- [Features](#features)
- [Run Locally](#run-locally)
  - [Creating an admin user](#creating-an-admin-user)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Contributing](#contributing)
<!-- TOC end -->

## Features

If the backend is finished, these are the features that the server has.

- Products database and stock
- Login page for customers in which they can view their transactions
- Export of transactions per customer
- Sending customers a mail with an overview of their transactions

## Run Locally

Clone the project

```bash
git clone https://github.com/larsvantol/tally-backend.git
```

Go to the root of the project directory and setup a virtual environment.

```bash
python -m venv venv
```

Activate the virtual environment.

```bash
python venv\Scripts\activate
```

Install the dependencies using the package manager [pip](https://pip.pypa.io/en/stable/). This should be done inside the virtual environment.

```bash
pip install -r requirements.txt
```

Run the migrations.

```bash
python manage.py migrate
```

Start the server

```bash
python manage.py runserver
```

The backend should work now and is accesible via [localhost:8000/admin](https://localhost:8000/admin)

### Creating an admin user

To log in into the backend you should have a user account with admin privileges. If you don't have an account yet you should create one by following the steps below:

```bash
python manage.py createsuperuser
```

You should now fill in the following fields:

```bash
Username (leave blank to use 'computername'):
Email:
Password:
Password (again):
Superuser created successfully.
```

You can now log in into the admin panel.

## Environment Variables

To run this project, you will need to create a file called `.env` in the main directory add the following environment variables to your `.env` file

#### `OIDC_RP_CLIENT_ID`

Here you have to specify the client id of the provider you are trying to connect to.

#### `OIDC_RP_CLIENT_SECRET`

Here you have to specify the client secret of the provider you are trying to connect to.

#### `OIDC_TALLY_ADMIN_GROUP`

Here you have to specify which group is allowed in the administration backend of the application.

#### `DJANGO_SECRET_KEY`

The secret key used in django. See the [Django documentation](https://docs.djangoproject.com/en/5.0/ref/settings/#secret-key).

## API Reference

See [API_REFERENCE.md](API_REFERENCE.md) for the documentation of the API.

## Contributing

Contributions are always welcome!

See [contributing.md](contributing.md) for ways to get started.
