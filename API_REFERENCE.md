# API Reference

## Table of Content
<!-- TOC start -->
- [Products](#products)
  * [Get all products](#get-all-products)
  * [Get specific product](#get-specific-product)
  * [Create a product](#create-a-product)
  * [Edit a product](#edit-a-product)
  * [Delete a product](#delete-a-product)
- [Product Groups](#product-groups)
  * [Get all product groups](#get-all-product-groups)
  * [Get a specific product group](#get-a-specific-product-group)
  * [Create a product group](#create-a-product-group)
  * [Edit a product group](#edit-a-product-group)
  * [Delete a product group](#delete-a-product-group)
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

| Parameter          | Type       | Description                                         | Required             |
| :----------------  | :-------   | :-------------------------------------------------- | :------------------- |
| `api_key`          | `string`   | Your API key                                        | **Required**         |

#### Response

```json
[
    {
        "id": 2,
        "name": "Lays - Paprika",
        "price": 1.53,
        "stock": 66,
        "image_url": "",
        "product_group": {
            "id": 1,
            "name": "Chips"
        }
    },
    {
        "id": 4,
        "name": "Fanta",
        "price": 7.0,
        "stock": 985,
        "image_url": "",
        "product_group": {
            "id": 2,
            "name": "Soda"
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

| Parameter          | Type       | Description                                         | Required             |
| :----------------  | :-------   | :-------------------------------------------------- | :------------------- |
| `api_key`          | `string`   | Your API key                                        | **Required**         |
| `id`               | `integer`  | Id of product to fetch                              | **Required**         |

#### Response

```json
{
    "id": 1,
    "name": "Cola",
    "price": 1.0,
    "stock": 10,
    "image_url": "",
    "product_group": {
        "id": 2,
        "name": "Soda"
    }
}
```

</details>

### Create a product

Use this endpoint to create a product.

<i>Only admin users can create products.</i>

```http
POST /products/products
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter          | Type       | Description                                         | Required             |
| :----------------  | :-------   | :-------------------------------------------------- | :------------------- |
| `api_key`          | `string`   | Your API key                                        | **Required**         |
| `name`             | `string`   | Name of the product                                 | **Required**         |
| `price`            | `string`   | Price of the product                                | **Required**         |
| `stock`            | `string`   | Initial stock of the product (0 if left empty)      | <i>Optional</a>      |
| `image_url`        | `string`   | Url to an image of the product                      | <i>Optional</a>      |
| `product_group_id` | `integer`  | Id of the product group that the product relates to | **Required**         |

#### Response

```json
{
    "id": 2,
    "name": "Lays - Paprika",
    "price": 1.66,
    "stock": 66,
    "image_url": "",
    "product_group": {
        "id": 1,
        "name": "Chips"
    }
}
```

</details>

### Edit a product

There are two API endpoints for editing products. You can use the `PUT` method for updating all the fields of a product or you can use `PATCH` for updating one or more fields of the product.

<i>Only admin users can edit products.</i>

```http
PUT /products/products/${id}
```

```http
PATCH /products/products/${id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter          | Type       | Description                                         | Required             |
| :----------------  | :-------   | :-------------------------------------------------- | :------------------- |
| `api_key`          | `string`   | Your API key                                        | **Required**         |
| `id`               | `integer`  | ID of the product                                   | **Required**         |
| `name`             | `string`   | Name of the product                                 | **Required for PUT** |
| `price`            | `string`   | Price of the product                                | **Required for PUT** |
| `stock`            | `string`   | Initial stock of the product (0 if left empty)      | <i>Optional</a>      |
| `image_url`        | `string`   | Url to an image of the product                      | <i>Optional</a>      |
| `product_group_id` | `integer`  | Id of the product group that the product relates to | **Required for PUT** |

#### Response

```json
{
    "id": 2,
    "name": "Lays - Paprika",
    "price": 1.66,
    "stock": 66,
    "image_url": "",
    "product_group": {
        "id": 1,
        "name": "Chips"
    }
}
```

</details>

### Delete a product

Use this endpoint to delete a product.

<i>Only admin users can delete products.</i>

```http
DELETE /products/products/${id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type      | Description                       | Required     |
| :-------- | :-------  | :-------------------------------- | :-------     |
| `api_key` | `string`  | Your API key                      | **Required** |
| `id`      | `integer` | ID of the product                 | **Required** |

#### Response

```http
HTTP 204 No Content
```

</details>

## Product Groups

### Get all product groups
Returns all product groups ordered by name.

```http
GET /products/product_groups
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type     | Description                       | Required     |
| :-------- | :------- | :-------------------------------- | :-------     |
| `api_key` | `string` | Your API key                      | **Required** |

#### Response

```json
[
    {
        "id": 1,
        "name": "Chips"
    },
    {
        "id": 2,
        "name": "Frisdrank"
    },
    {
        "id": 6,
        "name": "Snoep"
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

| Parameter | Type     | Description                       | Required     |
| :-------- | :------- | :-------------------------------- | :-------     |
| `api_key` | `string` | Your API key                      | **Required** |
| `id`      | `string` | Id of product group to fetch      | **Required** |

#### Response

```json
{
    "id": 1,
    "name": "Chips"
}
```

</details>

### Create a product group

Use this endpoint to create a product group.

<i>Only admin users can create product groups.</i>

```http
POST /products/product_group
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type     | Description                       | Required     |
| :-------- | :------- | :-------------------------------- | :-------     |
| `api_key` | `string` | Your API key                      | **Required** |
| `name`    | `string` | Name of the product group         | **Required** |

#### Response

```json
{
    "id": 7,
    "name": "Koek"
}
```

</details>

### Edit a product group

You can use the `PUT` method for updating the name field of a product group.

<i>Only admin users can edit product groups.</i>

```http
PUT /products/product_groups/${id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type      | Description                       | Required      |
| :-------- | :-------  | :-------------------------------- | :-------      |
| `api_key` | `string`  | Your API key                      | **Required**  |
| `id`      | `integer` | ID of the product group           | **Required**  |
| `name`    | `string`  | Name of the product group         | **Required**  |

#### Response

```json
{
    "id": 7,
    "name": "Koekjes"
}
```

</details>

### Delete a product group

Use this endpoint to delete a product group.

<i>Only admin users can delete product groups.</i>

```http
DELETE /products/product_groups/${id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type      | Description                        | Required      |
| :-------- | :-------  | :--------------------------------  | :-------      |
| `api_key` | `string`  | Your API key                       | **Required**  |
| `id`      | `integer` | ID of the product group            | **Required**  |

#### Response

```http
HTTP 204 No Content
```

</details>

## Transactions

### Get all transactions

Use this endpoint to get an overview of all transactions.

```http
GET /transactions/transactions
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type      | Description                        | Required      |
| :-------- | :-------  | :--------------------------------  | :-------      |
| `api_key` | `string`  | Your API key                       | **Required**  |

#### Response

```json
[
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
    },
    {
        "transaction_id": "175aa13a-aee1-427f-9730-725f7b692f8d",
        "customer": 1,
        "date_created": "2023-03-11T12:12:16.932386Z",
        "subtransactions": [
            {
                "description": "test",
                "amount": "78.00"
            }
        ],
        "subpurchases": [
            {
                "product": 4,
                "quantity": 2,
                "price": "66.00",
                "amount": 132.0
            },
            {
                "product": 1,
                "quantity": 8,
                "price": "5.21",
                "amount": 41.68
            }
        ]
    }
]
```

</details>

### Get a specific transaction

Use this endpoint to get an specific transaction.

```http
GET /transactions/transactions/${transaction_id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter        | Type      | Description                        | Required      |
| :--------------- | :-------  | :--------------------------------  | :-------      |
| `api_key`        | `string`  | Your API key                       | **Required**  |
| `transaction_id` | `string`  | The transaction id (uuid)          | **Required**  |

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

### Create a transaction

Use this endpoint to create a transaction.

```http
POST /transactions/transactions
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter        | Type      | Description                        | Required      |
| :--------------- | :-------  | :--------------------------------  | :-------      |
| `api_key`        | `string`  | Your API key                       | **Required**  |
| `customer_id`    | `integer` | The id of the customer             | **Required**  |

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

### Delete a specific transaction

Use this endpoint to delete an specific transaction.

```http
DELETE /transactions/transactions/${transaction_id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter        | Type      | Description                        | Required      |
| :--------------- | :-------  | :--------------------------------  | :-------      |
| `api_key`        | `string`  | Your API key                       | **Required**  |
| `transaction_id` | `string`  | The transaction id (uuid)          | **Required**  |

#### Response

```http
HTTP 204 No Content
```

</details>

## Customers

### Get all customers

Use this endpoint to get a list of all customers.

```http
GET /transactions/customers
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter | Type      | Description                        | Required      |
| :-------- | :-------  | :--------------------------------  | :-------      |
| `api_key` | `string`  | Your API key                       | **Required**  |

#### Response

```json
[
    {
        "id": 1,
        "first_name": "Lars",
        "prefix": "van",
        "last_name": "Tol"
    },
    {
        "id": 3,
        "first_name": "Christiaan",
        "prefix": "",
        "last_name": "Huygens"
    }
]
```

</details>


### Get a specific customer

Use this endpoint to get an specific customer.

```http
GET /transactions/customers/${customer_id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter        | Type      | Description                        | Required      |
| :--------------- | :-------  | :--------------------------------  | :-------      |
| `api_key`        | `string`  | Your API key                       | **Required**  |
| `customer_id`    | `string`  | The customer id                    | **Required**  |

#### Response

```json
{
    "id": 3,
    "first_name": "Christiaan",
    "prefix": "",
    "last_name": "Huygens"
}
```

</details>


### Create a customer

Use this endpoint to create a customer.

<i>Only admin users can create customers.</i>

```http
POST /transactions/customers
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter       | Type      | Description                                              | Required     |
| :-------------- | :-------- | :------------------------------------------------------- | :----------- |
| `api_key`       | `string`  | Your API key                                             | **Required** |
| `fist_name`     | `string`  | First name of the customer                               | **Required** |
| `prefix`        | `string`  | Prefix of the customer                                   | **Optional** |
| `last_name`     | `string`  | Last name of the customer                                | **Required** |
| `relation_code` | `integer` | Relation code as defined in the financial administration | **Required** |

#### Example request
```json
{
    "first_name": "Christiaan",
    "prefix": "",
    "last_name": "Huygens",
    "relation_code": 1957
}
```

#### Response

```json
{
    "id": 3,
    "first_name": "Christiaan",
    "prefix": "",
    "last_name": "Huygens"
}
```

</details>


### Delete a customer

Use this endpoint to delete a customer.

```http
DELETE /transactions/customers/${customer_id}
```

<details>

<summary>Details</summary>

#### Parameters

| Parameter        | Type      | Description                        | Required      |
| :--------------- | :-------  | :--------------------------------  | :-------      |
| `api_key`        | `string`  | Your API key                       | **Required**  |
| `customer_id`    | `integer` | The customer id                    | **Required**  |

#### Response

```http
HTTP 204 No Content
```

</details>
