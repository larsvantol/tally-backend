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
