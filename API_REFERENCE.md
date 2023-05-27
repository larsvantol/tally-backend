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

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

  <!-- TOC end -->

## Products

### Get all products

Returns all products ordered by product group name.

```http
GET /products/products
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type     | Description  | Required     |
| :-------- | :------- | :----------- | :----------- |
| `api_key` | `string` | Your API key | **Required** |

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
| `api_key` | `string`  | Your API key           | **Required** |
| `id`      | `integer` | Id of product to fetch | **Required** |

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

| Parameter | Type     | Description  | Required     |
| :-------- | :------- | :----------- | :----------- |
| `api_key` | `string` | Your API key | **Required** |

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
| `api_key` | `string` | Your API key                 | **Required** |
| `id`      | `string` | Id of product group to fetch | **Required** |

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

| Parameter | Type     | Description                                | Required     |
| :-------- | :------- | :----------------------------------------- | :----------- |
| `api_key` | `string` | Your API key                               | **Required** |
| `flat`    | `bool`   | Lists all subtransactions in one list      | **Optional** |
| `month`   | `int`    | Filter transactions for this month (1=Jan) | **Optional** |
| `year`    | `int`    | Filter transactions for this year          | **Optional** |

```http
GET /transactions/transactions?flat=true&month=5&year=2023
```

#### Response

```json
[
  {
    "transaction_id": "c3bb7b19-bcfb-413d-a88a-ee0d50aefdb7",
    "customer": 3,
    "date": "2023-04-21T09:33:57Z",
    "subtransactions": [
      {
        "description": "Test April",
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
        "description": "Test",
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
        "description": "Test",
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
    "name": "Test April",
    "quantity": 1,
    "amount": 1.66,
    "date": "2023-04-21T09:33:57Z"
  },
  {
    "name": "Test",
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
    "name": "Test",
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
POST /transactions/transactions
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter     | Type      | Description            | Required     |
| :------------ | :-------- | :--------------------- | :----------- |
| `api_key`     | `string`  | Your API key           | **Required** |
| `customer_id` | `integer` | The id of the customer | **Required** |

Furthermore one or more of the following is required: `SubTransaction` or `SubPurchase`. These can be provided in the post request as a list with the name `subtransactions` and/or `subpurchases`.

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
  "customer": 1,
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

#### Response

```json
{
  "transaction_id": "054b83c2-8380-4c49-8ebb-b317b337c8a0",
  "customer": 1,
  "date_created": "2023-03-10T17:43:11.138850Z",
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

Use this endpoint to get the logged in customer.

```http
GET /transactions/customer
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type     | Description  | Required     |
| :-------- | :------- | :----------- | :----------- |
| `api_key` | `string` | Your API key | **Required** |

#### Response

```json
{
  "id": 3,
  "relation_code": 6601,
  "sub": "WISVCH.10443",
  "user": {
    "id": 6,
    "username": "WISVCH.10443",
    "last_login": "2023-05-26T20:35:00.682717Z",
    "first_name": "Lars",
    "last_name": "van Tol",
    "email": "lmjvantol@gmail.com",
    "is_staff": true,
    "is_superuser": true,
    "days_since_joined": 6
  }
}
```

</details>
