# DataStack API Reference

> **Last updated: August 2026** — Generated from `app/routes/` by Devin.

API version: `2.1.0`

## Authentication

All endpoints require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

The header is required on every request; the deprecated `api_key` query parameter is no longer supported.

---

## Users

### List Users

```
GET /users
```

Returns all users in the given organization.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field             | Type   | Required | Description                                |
|-------------------|--------|----------|--------------------------------------------|
| `organization_id` | string | Yes      | Query parameter — organization to list users for |

**Response** — `200 OK`, array of user objects

| Field             | Type   | Description                                  |
|-------------------|--------|----------------------------------------------|
| `id`              | string | User ID                                       |
| `email`           | string | Email address                                 |
| `name`            | string | Display name                                  |
| `role`            | string | One of `admin`, `member`, `viewer`            |
| `organization_id` | string | Organization the user belongs to              |
| `created_at`      | string | ISO 8601 UTC timestamp                        |

```json
[
  {
    "id": "usr_abc123",
    "email": "alice@datastack.io",
    "name": "Alice",
    "role": "admin",
    "organization_id": "org_xyz",
    "created_at": "2026-01-01T00:00:00Z"
  }
]
```

**Curl example**

```bash
curl -X GET "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create User

```
POST /users
```

Creates a new user. Requires admin role on the organization.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request body**

| Field             | Type   | Required | Description                                             |
|-------------------|--------|----------|---------------------------------------------------------|
| `email`           | string | Yes      | Valid email address                                      |
| `name`            | string | Yes      | Display name                                             |
| `role`            | string | No       | One of `admin`, `member`, `viewer`. Defaults to `member` |
| `organization_id` | string | Yes      | Organization the user belongs to                         |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field             | Type   | Description                        |
|-------------------|--------|------------------------------------|
| `id`              | string | User ID                             |
| `email`           | string | Email address                       |
| `name`            | string | Display name                        |
| `role`            | string | `admin`, `member`, or `viewer`      |
| `organization_id` | string | Organization the user belongs to    |
| `created_at`      | string | ISO 8601 UTC timestamp              |

```json
{
  "id": "usr_abc123",
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz",
  "created_at": "2026-03-20T00:00:00Z"
}
```

**Curl example**

```bash
curl -X POST "https://api.datastack.io/users" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"member","organization_id":"org_xyz"}'
```

---

### Get User

```
GET /users/{user_id}
```

Fetches a single user by ID.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field     | Type   | Required | Description             |
|-----------|--------|----------|-------------------------|
| `user_id` | string | Yes      | Path parameter — user ID |

**Response** — `200 OK`, same fields as [Create User](#create-user).

```json
{
  "id": "usr_abc123",
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz",
  "created_at": "2026-01-01T00:00:00Z"
}
```

**Curl example**

```bash
curl -X GET "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently deletes a user. You cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field     | Type   | Required | Description             |
|-----------|--------|----------|-------------------------|
| `user_id` | string | Yes      | Path parameter — user ID |

**Response** — `204 No Content`, empty body.

**Curl example**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### List Products

```
GET /products
```

Lists all products in the catalog, optionally filtered by tag.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field | Type   | Required | Description                            |
|-------|--------|----------|----------------------------------------|
| `tag` | string | No       | Query parameter — filter products by tag |

**Response** — `200 OK`, array of product objects

| Field             | Type            | Description                              |
|-------------------|-----------------|------------------------------------------|
| `id`              | string          | Product ID                                |
| `name`            | string          | Product name                              |
| `description`     | string          | Product description                       |
| `price_cents`     | integer         | Price in USD cents                        |
| `sku`             | string          | Stock keeping unit                        |
| `inventory_count` | integer         | Units currently in stock                  |
| `tags`            | array of string | Tags assigned to the product              |
| `created_at`      | string          | ISO 8601 UTC timestamp                    |

```json
[
  {
    "id": "prod_001",
    "name": "Widget Pro",
    "description": "Our best-selling widget.",
    "price_cents": 4999,
    "sku": "WGT-PRO-001",
    "inventory_count": 142,
    "tags": ["hardware", "featured"],
    "created_at": "2026-01-15T00:00:00Z"
  }
]
```

**Curl example**

```bash
curl -X GET "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create Product

```
POST /products
```

Creates a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request body**

| Field             | Type            | Required | Description                          |
|-------------------|-----------------|----------|--------------------------------------|
| `name`            | string          | Yes      | Product name                          |
| `description`     | string          | Yes      | Product description                   |
| `price_cents`     | integer         | Yes      | Price in USD cents                    |
| `sku`             | string          | Yes      | Stock keeping unit                    |
| `inventory_count` | integer         | No       | Units in stock. Defaults to `0`       |
| `tags`            | array of string | No       | Tags. Defaults to `[]`                |

```json
{
  "name": "Widget Pro",
  "description": "Our best-selling widget.",
  "price_cents": 4999,
  "sku": "WGT-PRO-001",
  "inventory_count": 142,
  "tags": ["hardware", "featured"]
}
```

**Response** — `201 Created`, same fields as [List Products](#list-products).

```json
{
  "id": "prod_001",
  "name": "Widget Pro",
  "description": "Our best-selling widget.",
  "price_cents": 4999,
  "sku": "WGT-PRO-001",
  "inventory_count": 142,
  "tags": ["hardware", "featured"],
  "created_at": "2026-03-20T00:00:00Z"
}
```

**Curl example**

```bash
curl -X POST "https://api.datastack.io/products" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### Get Product

```
GET /products/{product_id}
```

Fetches a single product by ID.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field        | Type   | Required | Description                |
|--------------|--------|----------|----------------------------|
| `product_id` | string | Yes      | Path parameter — product ID |

**Response** — `200 OK`, same fields as [List Products](#list-products).

```json
{
  "id": "prod_001",
  "name": "Widget Pro",
  "description": "Our best-selling widget.",
  "price_cents": 4999,
  "sku": "WGT-PRO-001",
  "inventory_count": 142,
  "tags": ["hardware", "featured"],
  "created_at": "2026-01-15T00:00:00Z"
}
```

**Curl example**

```bash
curl -X GET "https://api.datastack.io/products/prod_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

An order object has the following shape:

| Field              | Type              | Description                                                                 |
|--------------------|-------------------|-----------------------------------------------------------------------------|
| `id`               | string            | Order ID                                                                     |
| `user_id`          | string            | ID of the user who placed the order                                          |
| `items`            | array of object   | Line items — `product_id` (string), `quantity` (integer), `unit_price_cents` (integer) |
| `shipping_address` | string            | Destination address                                                          |
| `status`           | string            | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`           |
| `total_cents`      | integer           | Order total in USD cents (sum of `quantity` × `unit_price_cents`)            |
| `promo_code`       | string or null    | Promo code applied to the order                                              |
| `tracking_number`  | string or null    | Carrier tracking number, once shipped                                        |
| `created_at`       | string            | ISO 8601 UTC timestamp                                                       |
| `updated_at`       | string            | ISO 8601 UTC timestamp                                                       |

### Create Order

```
POST /orders
```

Places a new order. Inventory is reserved immediately and payment is captured asynchronously; the order is returned in `pending` status.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request body**

| Field                       | Type            | Required | Description                                        |
|-----------------------------|-----------------|----------|----------------------------------------------------|
| `user_id`                   | string          | Yes      | User placing the order                              |
| `items`                     | array of object | Yes      | Line items (see below)                              |
| `items[].product_id`        | string          | Yes      | Product being ordered                               |
| `items[].quantity`          | integer         | Yes      | Units ordered                                       |
| `items[].unit_price_cents`  | integer         | Yes      | Per-unit price in USD cents                         |
| `shipping_address`          | string          | Yes      | Destination address                                 |
| `promo_code`                | string          | No       | Promo code to apply. Defaults to `null`             |
| `priority_shipping`         | boolean         | No       | Request expedited shipping. Defaults to `false`     |
| `gift_message`              | string          | No       | Message included with the order. Defaults to `null` |

`priority_shipping` and `gift_message` are accepted on input but are not returned in the order response.

```json
{
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": "WELCOME10",
  "priority_shipping": true,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`, an order object.

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "status": "pending",
  "total_cents": 9998,
  "promo_code": "WELCOME10",
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl example**

```bash
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","priority_shipping":true,"gift_message":"Happy birthday!"}'
```

---

### Get Order

```
GET /orders/{order_id}
```

Fetches a single order by ID. Users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field      | Type   | Required | Description              |
|------------|--------|----------|--------------------------|
| `order_id` | string | Yes      | Path parameter — order ID |

**Response** — `200 OK`, an order object.

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "status": "shipped",
  "total_cents": 9998,
  "promo_code": null,
  "tracking_number": "1Z999AA10123456784",
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-19T08:30:00Z"
}
```

**Curl example**

```bash
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Updates the status of an order. Only admins can transition an order to `confirmed`, `shipped`, or `delivered`; users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field             | Type   | Required | Description                                                                 |
|-------------------|--------|----------|-----------------------------------------------------------------------------|
| `order_id`        | string | Yes      | Path parameter — order ID                                                    |
| `status`          | string | Yes      | Body — one of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`    |
| `tracking_number` | string | No       | Body — carrier tracking number. Defaults to `null`                           |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`, an order object.

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "status": "shipped",
  "total_cents": 9998,
  "promo_code": null,
  "tracking_number": "1Z999AA10123456784",
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl example**

```bash
curl -X PATCH "https://api.datastack.io/orders/ord_001/status" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## System

### Health Check

```
GET /health
```

Returns service health. No authentication required.

**Response** — `200 OK`

```json
{ "status": "ok" }
```

**Curl example**

```bash
curl -X GET "https://api.datastack.io/health"
```

---

## Error Codes

| Code | Meaning                                      |
|------|----------------------------------------------|
| 400  | Bad request                                   |
| 401  | Missing or invalid bearer token               |
| 403  | Authenticated but not permitted               |
| 404  | Resource not found                            |
| 422  | Request validation failed                     |
| 500  | Internal server error                         |
