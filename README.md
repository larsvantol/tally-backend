# Tally
Tally is the backend for tracking transactions for various products sold at the study association. In addition to products, other expenses that are not linked to a product can also be tracked here. An export can be made of the products sold in a certain time period.

<!-- TOC start -->
- [Features](#features)
- [Run Locally](#run-locally)
  * [Creating a admin user](#creating-a-admin-user)
- [Environment Variables (Dummy text)](#environment-variables-dummy-text)
- [API Reference (Dummy text)](#api-reference-dummy-text)
    + [Get all items](#get-all-items)
    + [Get item](#get-item)
    + [add(num1, num2)](#addnum1-num2)
- [Contributing (Dummy text)](#contributing-dummy-text)
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
git clone https://github.com/larsvantol/turf.git
```

Go to the root of the project directory and setup a virtual environment.

```bash
python venv venv
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
python manage.py runserver
```

Start the server

```bash
python manage.py runserver
```

The backend should work now and is accesible via [localhost:8000/admin](https://localhost:8000/admin)

### Creating a admin user

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

## Environment Variables (Dummy text)

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`

## API Reference

See [API_REFERENCE.md](API_REFERENCE.md) for the documentation of the API.

## Contributing (Dummy text)

Contributions are always welcome!

See [contributing.md](contributing.md) for ways to get started.
