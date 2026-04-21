# DataStack API Reference

> This document reflects the current state of `app/routes/`. It is kept in sync automatically — see `scripts/trigger_devin.py` and `.github/workflows/doc-sync.yml`.

## Authentication

All API requests require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Requests missing or presenting an invalid token receive `401 Unauthorized`.

---

## Users

### List Users

```
GET /users
```

Returns all users in the given organization.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Query Parameters**

| Parameter        | Type   | Required | Description                      |
|------------------|--------|----------|----------------------------------|
| organization_id  | string | Yes      | Organization to scope the list by |

**Response** — `200 OK`

| Field            | Type   | Description                                  |
|------------------|--------|----------------------------------------------|
| id               | string | User ID                                      |
| email            | string | User email address                           |
| name             | string | User's display name                          |
| role             | string | One of `admin`, `member`, `viewer`           |
| organization_id  | string | Organization the user belongs to             |
| created_at       | string | ISO-8601 timestamp                           |

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

**Curl**

```bash
curl -X GET "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create User

```
POST /users
```

Create a new user. Requires admin role on the organization.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Request Body**

| Field            | Type   | Required | Description                                  |
|------------------|--------|----------|----------------------------------------------|
| email            | string | Yes      | User email address (validated)               |
| name             | string | Yes      | User's display name                          |
| role             | string | No       | One of `admin`, `member`, `viewer`. Defaults to `member` |
| organization_id  | string | Yes      | Organization the user is created in          |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field            | Type   | Description                                  |
|------------------|--------|----------------------------------------------|
| id               | string | User ID                                      |
| email            | string | User email address                           |
| name             | string | User's display name                          |
| role             | string | One of `admin`, `member`, `viewer`           |
| organization_id  | string | Organization the user belongs to             |
| created_at       | string | ISO-8601 timestamp                           |

```json
{
  "id": "usr_abc123",
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz",
  "created_at": "2026-03-20T00:00:00Z"
}
```

**Curl**

```bash
curl -X POST "https://api.datastack.io/users" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@datastack.io",
    "name": "Alice",
    "role": "admin",
    "organization_id": "org_xyz"
  }'
```

---

### Get User

```
GET /users/{user_id}
```

Fetch a single user by ID.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Yes      | User ID     |

**Response** — `200 OK`

| Field            | Type   | Description                                  |
|------------------|--------|----------------------------------------------|
| id               | string | User ID                                      |
| email            | string | User email address                           |
| name             | string | User's display name                          |
| role             | string | One of `admin`, `member`, `viewer`           |
| organization_id  | string | Organization the user belongs to             |
| created_at       | string | ISO-8601 timestamp                           |

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

**Curl**

```bash
curl -X GET "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently delete a user. Cannot delete your own account.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Yes      | User ID     |

**Response** — `204 No Content`

No response body.

**Curl**

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

List all products. Optionally filter by tag.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Query Parameters**

| Parameter | Type   | Required | Description                            |
|-----------|--------|----------|----------------------------------------|
| tag       | string | No       | If provided, only products with this tag are returned |

**Response** — `200 OK`

| Field            | Type     | Description                                  |
|------------------|----------|----------------------------------------------|
| id               | string   | Product ID                                   |
| name             | string   | Product name                                 |
| description      | string   | Product description                          |
| price_cents      | integer  | Price in USD cents                           |
| sku              | string   | Stock keeping unit                           |
| inventory_count  | integer  | Current inventory count                      |
| tags             | string[] | Product tags                                 |
| created_at       | string   | ISO-8601 timestamp                           |

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

**Curl**

```bash
curl -X GET "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create Product

```
POST /products
```

Create a new product in the catalog.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Request Body**

| Field            | Type     | Required | Description                                  |
|------------------|----------|----------|----------------------------------------------|
| name             | string   | Yes      | Product name                                 |
| description      | string   | Yes      | Product description                          |
| price_cents      | integer  | Yes      | Price in USD cents                           |
| sku              | string   | Yes      | Stock keeping unit                           |
| inventory_count  | integer  | No       | Initial inventory count. Defaults to `0`     |
| tags             | string[] | No       | Product tags. Defaults to `[]`               |

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

**Response** — `201 Created`

| Field            | Type     | Description                                  |
|------------------|----------|----------------------------------------------|
| id               | string   | Product ID                                   |
| name             | string   | Product name                                 |
| description      | string   | Product description                          |
| price_cents      | integer  | Price in USD cents                           |
| sku              | string   | Stock keeping unit                           |
| inventory_count  | integer  | Current inventory count                      |
| tags             | string[] | Product tags                                 |
| created_at       | string   | ISO-8601 timestamp                           |

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

**Curl**

```bash
curl -X POST "https://api.datastack.io/products" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Widget Pro",
    "description": "Our best-selling widget.",
    "price_cents": 4999,
    "sku": "WGT-PRO-001",
    "inventory_count": 142,
    "tags": ["hardware", "featured"]
  }'
```

---

### Get Product

```
GET /products/{product_id}
```

Fetch a single product by ID.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Path Parameters**

| Parameter  | Type   | Required | Description |
|------------|--------|----------|-------------|
| product_id | string | Yes      | Product ID  |

**Response** — `200 OK`

| Field            | Type     | Description                                  |
|------------------|----------|----------------------------------------------|
| id               | string   | Product ID                                   |
| name             | string   | Product name                                 |
| description      | string   | Product description                          |
| price_cents      | integer  | Price in USD cents                           |
| sku              | string   | Stock keeping unit                           |
| inventory_count  | integer  | Current inventory count                      |
| tags             | string[] | Product tags                                 |
| created_at       | string   | ISO-8601 timestamp                           |

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

**Curl**

```bash
curl -X GET "https://api.datastack.io/products/prod_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

### Create Order

```
POST /orders
```

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. The order is returned in `pending` status.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Request Body**

| Field              | Type           | Required | Description                                                  |
|--------------------|----------------|----------|--------------------------------------------------------------|
| user_id            | string         | Yes      | ID of the user placing the order                             |
| items              | OrderItem[]    | Yes      | Line items in the order (see below)                          |
| shipping_address   | string         | Yes      | Shipping address as a single line                            |
| promo_code         | string         | No       | Optional promo code                                          |
| priority_shipping  | boolean        | No       | Whether to use priority shipping. Defaults to `false`        |
| gift_message       | string         | No       | Optional gift message to include with the order              |

`OrderItem` fields:

| Field             | Type    | Required | Description                          |
|-------------------|---------|----------|--------------------------------------|
| product_id        | string  | Yes      | Product ID                           |
| quantity          | integer | Yes      | Quantity ordered                     |
| unit_price_cents  | integer | Yes      | Unit price in USD cents              |

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

**Response** — `201 Created`

| Field             | Type         | Description                                                     |
|-------------------|--------------|-----------------------------------------------------------------|
| id                | string       | Order ID                                                        |
| user_id           | string       | ID of the user who placed the order                             |
| items             | OrderItem[]  | Line items                                                      |
| shipping_address  | string       | Shipping address                                                |
| status            | string       | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| total_cents       | integer      | Total order amount in USD cents                                 |
| promo_code        | string\|null | Promo code used, or `null`                                      |
| tracking_number   | string\|null | Carrier tracking number, or `null` until shipped                |
| created_at        | string       | ISO-8601 timestamp                                              |
| updated_at        | string       | ISO-8601 timestamp                                              |

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

**Curl**

```bash
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usr_abc123",
    "items": [
      { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
    ],
    "shipping_address": "123 Main St, San Francisco, CA 94105",
    "promo_code": "WELCOME10",
    "priority_shipping": true,
    "gift_message": "Happy birthday!"
  }'
```

---

### Get Order

```
GET /orders/{order_id}
```

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| order_id  | string | Yes      | Order ID    |

**Response** — `200 OK`

| Field             | Type         | Description                                                     |
|-------------------|--------------|-----------------------------------------------------------------|
| id                | string       | Order ID                                                        |
| user_id           | string       | ID of the user who placed the order                             |
| items             | OrderItem[]  | Line items                                                      |
| shipping_address  | string       | Shipping address                                                |
| status            | string       | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| total_cents       | integer      | Total order amount in USD cents                                 |
| promo_code        | string\|null | Promo code used, or `null`                                      |
| tracking_number   | string\|null | Carrier tracking number, or `null`                              |
| created_at        | string       | ISO-8601 timestamp                                              |
| updated_at        | string       | ISO-8601 timestamp                                              |

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

**Curl**

```bash
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`. Users may cancel their own `pending` orders.

**Authentication**

| Header        | Value                     |
|---------------|---------------------------|
| Authorization | `Bearer <token>` (required) |

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| order_id  | string | Yes      | Order ID    |

**Request Body**

| Field            | Type         | Required | Description                                                     |
|------------------|--------------|----------|-----------------------------------------------------------------|
| status           | string       | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| tracking_number  | string       | No       | Carrier tracking number. Typically set when moving to `shipped` |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Same schema as [Get Order](#get-order).

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

**Curl**

```bash
curl -X PATCH "https://api.datastack.io/orders/ord_001/status" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped",
    "tracking_number": "1Z999AA10123456784"
  }'
```

---

## Error Codes

| Code | Meaning                               |
|------|---------------------------------------|
| 400  | Bad request                           |
| 401  | Missing or invalid bearer token       |
| 403  | Authenticated but not authorized      |
| 404  | Resource not found                    |
| 500  | Internal server error                 |
