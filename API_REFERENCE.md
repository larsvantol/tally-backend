# API Reference

## Table of Content

<!-- TOC start -->

- [Products](#products)
  - [Get all products](#get-all-products)
    - [Parameters](#parameters)
    - [Response](#response)
  - [Get specific product](#get-specific-product)
    - [Parameters](#parameters-1)
    - [Response](#response-1)
- [Product Groups](#product-groups)
  - [Get all product groups](#get-all-product-groups)
    - [Parameters](#parameters-2)
    - [Response](#response-2)
  - [Get a specific product group](#get-a-specific-product-group)
    - [Parameters](#parameters-3)
    - [Response](#response-3)
- [Transactions](#transactions)
  - [Get all transactions](#get-all-transactions)
    - [Parameters](#parameters-4)
    - [Response](#response-4)
  - [Create a transaction](#create-a-transaction)
    - [Parameters](#parameters-5)
    - [Response](#response-5)
- [Customers](#customers)

  - [Get the current customer](#get-the-current-customer)
    - [Parameters](#parameters-6)
    - [Response](#response-6)

  <!-- TOC end -->

## Authentication

Some endpoints are secured. To use this endpoints a user must be authenticated. To authenticate, the application using the endpoints must be whitelisted in the settings (see `CORS_ORIGIN_WHITELIST` and `CSRF_TRUSTED_ORIGINS`) and with each request the credentials (`sessionid` and `csrftoken`) must be sent.

## Products

### Get all products

Returns all products ordered by product group name.

```http
GET /products/products
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type | Description | Required |
| :-------- | :--- | :---------- | :------- |

<i>None</i>

#### Authentication

<i>Authentication not required</i>

#### Response

```json
[
  {
    "id": 3,
    "name": "Lays - Paprika",
    "price": 1.66,
    "stock": 60,
    "image_url": "",
    "product_group": {
      "id": 2,
      "name": "Chips",
      "created": "2023-05-19T10:51:59.472081Z",
      "last_modified": "2023-05-19T10:51:59.472081Z"
    }
  },
  {
    "id": 4,
    "name": "Lays - Naturel",
    "price": 1.66,
    "stock": 66,
    "image_url": "",
    "product_group": {
      "id": 2,
      "name": "Chips",
      "created": "2023-05-19T10:51:59.472081Z",
      "last_modified": "2023-05-19T10:51:59.472081Z"
    }
  },
  {
    "id": 1,
    "name": "Fanta",
    "price": 1.66,
    "stock": 14,
    "image_url": "",
    "product_group": {
      "id": 1,
      "name": "Frisdrank",
      "created": "2023-05-09T19:00:11.947134Z",
      "last_modified": "2023-05-09T19:00:11.947134Z"
    }
  },
  {
    "id": 2,
    "name": "Cola",
    "price": 1.23,
    "stock": 13,
    "image_url": "",
    "product_group": {
      "id": 1,
      "name": "Frisdrank",
      "created": "2023-05-09T19:00:11.947134Z",
      "last_modified": "2023-05-09T19:00:11.947134Z"
    }
  }
]
```

</details>

### Get specific product

Returns the specific product that was requested.

```http
GET /products/products/${id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type      | Description            | Required     |
| :-------- | :-------- | :--------------------- | :----------- |
| `id`      | `integer` | Id of product to fetch | **Required** |

#### Authentication

<i>Authentication not required</i>

#### Response

```json
{
  "id": 1,
  "name": "Fanta",
  "price": 1.66,
  "stock": 14,
  "image_url": "",
  "product_group": {
    "id": 1,
    "name": "Frisdrank",
    "created": "2023-05-09T19:00:11.947134Z",
    "last_modified": "2023-05-09T19:00:11.947134Z"
  }
}
```

</details>

## Product Groups

### Get all product groups

Returns all product groups ordered by name including the products that belong to them.

```http
GET /products/product_groups
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type | Description | Required |
| :-------- | :--- | :---------- | :------- |

<i>None</i>

#### Authentication

<i>Authentication not required</i>

#### Response

```json
[
  {
    "id": 1,
    "name": "Frisdrank",
    "products": [
      {
        "id": 1,
        "name": "Fanta",
        "price": 1.66,
        "stock": 14,
        "image_url": "",
        "product_group": {
          "id": 1,
          "name": "Frisdrank",
          "created": "2023-05-09T19:00:11.947134Z",
          "last_modified": "2023-05-09T19:00:11.947134Z"
        }
      },
      {
        "id": 2,
        "name": "Cola",
        "price": 1.23,
        "stock": 13,
        "image_url": "",
        "product_group": {
          "id": 1,
          "name": "Frisdrank",
          "created": "2023-05-09T19:00:11.947134Z",
          "last_modified": "2023-05-09T19:00:11.947134Z"
        }
      }
    ]
  },
  {
    "id": 2,
    "name": "Chips",
    "products": [
      {
        "id": 3,
        "name": "Lays - Paprika",
        "price": 1.66,
        "stock": 60,
        "image_url": "",
        "product_group": {
          "id": 2,
          "name": "Chips",
          "created": "2023-05-19T10:51:59.472081Z",
          "last_modified": "2023-05-19T10:51:59.472081Z"
        }
      },
      {
        "id": 4,
        "name": "Lays - Naturel",
        "price": 1.66,
        "stock": 66,
        "image_url": "",
        "product_group": {
          "id": 2,
          "name": "Chips",
          "created": "2023-05-19T10:51:59.472081Z",
          "last_modified": "2023-05-19T10:51:59.472081Z"
        }
      }
    ]
  }
]
```

</details>

### Get a specific product group

Returns the specific product group that was requested.

```http
GET /products/product_groups/${id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type     | Description                  | Required     |
| :-------- | :------- | :--------------------------- | :----------- |
| `id`      | `string` | Id of product group to fetch | **Required** |

#### Authentication

<i>Authentication not required</i>

#### Response

```json
{
  "id": 1,
  "name": "Frisdrank",
  "products": [
    {
      "id": 1,
      "name": "Fanta",
      "price": 1.66,
      "stock": 14,
      "image_url": "",
      "product_group": {
        "id": 1,
        "name": "Frisdrank",
        "created": "2023-05-09T19:00:11.947134Z",
        "last_modified": "2023-05-09T19:00:11.947134Z"
      }
    },
    {
      "id": 2,
      "name": "Cola",
      "price": 1.23,
      "stock": 13,
      "image_url": "",
      "product_group": {
        "id": 1,
        "name": "Frisdrank",
        "created": "2023-05-09T19:00:11.947134Z",
        "last_modified": "2023-05-09T19:00:11.947134Z"
      }
    }
  ]
}
```

</details>

## Transactions

### Get all transactions

Use this endpoint to get an overview of all transactions of the customer that is logged in.

```http
GET /transactions/transactions
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type   | Description                                | Required     |
| :-------- | :----- | :----------------------------------------- | :----------- |
| `flat`    | `bool` | Lists all subtransactions in one list      | **Optional** |
| `month`   | `int`  | Filter transactions for this month (1=Jan) | **Optional** |
| `year`    | `int`  | Filter transactions for this year          | **Optional** |

Exampe:

```http
GET /transactions/transactions/?flat=true&month=5&year=2023
```

#### Authentication

Authentication is required. Only the transactions of the authenticated user are returned.

#### Response

```json
[
  {
    "transaction_id": "c3bb7b19-bcfb-413d-a88a-ee0d50aefdb7",
    "customer": 3,
    "date": "2023-04-21T09:33:57Z",
    "subtransactions": [
      {
        "description": "Cosmo kosten (5km)",
        "amount": "1.66"
      }
    ],
    "subpurchases": []
  },
  {
    "transaction_id": "e7a5f3e5-3f1d-4a66-a50b-b1cb8e148897",
    "customer": 3,
    "date": "2023-05-13T17:51:58Z",
    "subtransactions": [
      {
        "description": "AV eten 13/05",
        "amount": "12.78"
      }
    ],
    "subpurchases": [
      {
        "product": 1,
        "quantity": 2,
        "price": "3.45",
        "amount": 6.9
      }
    ]
  },
  {
    "transaction_id": "c90a24a4-4d00-4b29-aae6-454eb15469a8",
    "customer": 3,
    "date": "2023-05-20T11:00:29Z",
    "subtransactions": [
      {
        "description": "AV eten 20/05",
        "amount": "10.66"
      }
    ],
    "subpurchases": []
  }
]
```

Example response for `flat = True`

```json
[
  {
    "name": "Cosmo kosten (5km)",
    "quantity": 1,
    "amount": 1.66,
    "date": "2023-04-21T09:33:57Z"
  },
  {
    "name": "AV eten 13/05",
    "quantity": 1,
    "amount": 12.78,
    "date": "2023-05-13T17:51:58Z"
  },
  {
    "name": "Fanta",
    "quantity": 2,
    "amount": 6.9,
    "date": "2023-05-13T17:51:58Z"
  },
  {
    "name": "AV eten 20/05",
    "quantity": 1,
    "amount": 10.66,
    "date": "2023-05-20T11:00:29Z"
  }
]
```

</details>

### Create a transaction

Use this endpoint to create a transaction.

```http
POST /transactions/transactions/
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type | Description | Required |
| :-------- | :--- | :---------- | :------- |

One or more of the following is <b>required</b>: `SubTransaction` or `SubPurchase`. These can be provided in the post request as a list with the name `subtransactions` and/or `subpurchases`.

A `SubTransaction` has the following form:

```json
{
  "description": "AV Eten",
  "amount": 10.66
}
```

A `SubPurchase` has the following form: (it uses the product id)

```json
{
  "product": 1,
  "quantity": 8
}
```

An example request can look like this:

<i>`subpurchases` or `subtransactions` can be left out of the request below.</i>

```json
{
  "subpurchases": [
    {
      "product": 4,
      "quantity": 2
    },
    {
      "product": 1,
      "quantity": 8
    }
  ],
  "subtransactions": [
    {
      "description": "test",
      "amount": 78.21
    }
  ]
}
```

#### Authentication

Authentication is required. Only transactions for the authenticated user can be created.

#### Response

```json
{
  "transaction_id": "054b83c2-8380-4c49-8ebb-b317b337c8a0",
  "customer": 1,
  "date": "2024-02-22T19:59:23.559999Z",
  "subtransactions": [
    {
      "description": "Test",
      "amount": "5.00"
    }
  ],
  "subpurchases": [
    {
      "product": 4,
      "quantity": 2,
      "price": "1.00",
      "amount": 2.0
    }
  ]
}
```

</details>

## Customers

### Get the current customer

Use this endpoint to get information about the logged in customer.

```http
GET /transactions/customer
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type | Description | Required |
| :-------- | :--- | :---------- | :------- |

<i>None</i>

#### Authentication

Authentication is required. Only information about the current user is returned.

#### Response

```json
{
  "id": 4,
  "netid": "dewijzeuil",
  "sub": "WISVCH.660001",
  "relation_code": 6601,
  "user": {
    "id": 5,
    "username": "WISVCH.660001",
    "last_login": "2024-02-22T19:19:00Z",
    "first_name": "De",
    "last_name": "Wijze Uil",
    "email": "dewijzeuil@ch.tudelft.nl",
    "is_staff": true,
    "is_superuser": true,
    "days_since_joined": 0
  }
}
```

</details>
