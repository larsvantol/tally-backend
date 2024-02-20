# Tally
Tally is the backend for tracking transactions for various products sold at the study association. In addition to products, other expenses that are not linked to a product can also be tracked here. An export can be made of the products sold in a certain time period.

<!-- TOC start -->
- [Features](#features)
- [Run Locally](#run-locally)
  * [Creating an admin user](#creating-an-admin-user)
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

There is also a docker devcontainer for this project. See [devcontainer](#devcontainer).

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

## Devcontainer

This repository has a devcontainer that has been tested in VS Code. The devcontainer will automatically install all dependencies, start a postgres container and an adminer container. On the first build of the container it will also run the migrations.

To be able to run the devcontainer you need to have VS Code installed with the [dev containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). 

First clone the repository and open it with VS Code. Now run the following command in the VS Code command palette: `Dev Containers: Reopen in Container`. (You can open the command palette with `Ctrl+Shift+P`).

Once everything has started succesfully you should be able to access adminer on `localhost:8080`. To be able to run and acces tally itself, you might still need to [create an admin user](#creating-an-admin-user) (first do `cd tally`). Then you can run tally by pressing `Start Debugging (F5)` or by running the command `python manage.py runserver`. You should now be able to access tally on `localhost:8000`. If you want to run the migrations, use the command `python manage.py migrate`.

## Environment Variables (Dummy text)
<i>Dummy text</i>
To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`

## API Reference

See [API_REFERENCE.md](API_REFERENCE.md) for the documentation of the API.

## Contributing

Contributions are always welcome!

See [contributing.md](contributing.md) for ways to get started.
