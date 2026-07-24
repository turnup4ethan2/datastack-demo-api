# DataStack API Reference

> **Last updated: July 2026** — Auto-generated from `app/routes/` by Devin.

## Authentication

All API requests require a Bearer token passed in the `Authorization` header:

```
Authorization: Bearer <token>
```

---

## Users

### List Users — `GET /users`

Returns all users in the given organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Parameter         | Type   | Required | Description                    |
|-------------------|--------|----------|--------------------------------|
| `organization_id` | string | Yes      | Query param. Organization to list users for. |

**Response** — `200 OK`

| Field             | Type   | Description                          |
|-------------------|--------|--------------------------------------|
| `id`              | string | User ID                              |
| `email`           | string | User email                           |
| `name`            | string | User full name                       |
| `role`            | string | One of `admin`, `member`, `viewer`   |
| `organization_id` | string | Organization the user belongs to     |
| `created_at`      | string | ISO 8601 timestamp                   |

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
curl "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer <token>"
```

---

### Create User — `POST /users`

Create a new user. Requires admin role on the organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field             | Type   | Required | Description                          |
|-------------------|--------|----------|--------------------------------------|
| `email`           | string | Yes      | Valid email address                  |
| `name`            | string | Yes      | User full name                       |
| `role`            | string | No       | One of `admin`, `member`, `viewer`. Defaults to `member`. |
| `organization_id` | string | Yes      | Organization the user belongs to     |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field             | Type   | Description                          |
|-------------------|--------|--------------------------------------|
| `id`              | string | User ID                              |
| `email`           | string | User email                           |
| `name`            | string | User full name                       |
| `role`            | string | One of `admin`, `member`, `viewer`   |
| `organization_id` | string | Organization the user belongs to     |
| `created_at`      | string | ISO 8601 timestamp                   |

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

**Curl**

```bash
curl -X POST "https://api.datastack.io/users" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"member","organization_id":"org_xyz"}'
```

---

### Get User — `GET /users/{user_id}`

Fetch a single user by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Parameter   | Type   | Required | Description   |
|-------------|--------|----------|---------------|
| `user_id`   | string | Yes      | Path param. User ID. |

**Response** — `200 OK`

| Field             | Type   | Description                          |
|-------------------|--------|--------------------------------------|
| `id`              | string | User ID                              |
| `email`           | string | User email                           |
| `name`            | string | User full name                       |
| `role`            | string | One of `admin`, `member`, `viewer`   |
| `organization_id` | string | Organization the user belongs to     |
| `created_at`      | string | ISO 8601 timestamp                   |

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
curl "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

### Delete User — `DELETE /users/{user_id}`

Permanently delete a user. You cannot delete your own account.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Parameter   | Type   | Required | Description   |
|-------------|--------|----------|---------------|
| `user_id`   | string | Yes      | Path param. User ID. |

**Response** — `204 No Content`

No response body.

**Curl**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

## Products

### List Products — `GET /products`

List all products. Optionally filter by tag.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Parameter | Type   | Required | Description                        |
|-----------|--------|----------|------------------------------------|
| `tag`     | string | No       | Query param. Filter products by tag. |

**Response** — `200 OK`

| Field             | Type          | Description                       |
|-------------------|---------------|-----------------------------------|
| `id`              | string        | Product ID                        |
| `name`            | string        | Product name                      |
| `description`     | string        | Product description               |
| `price_cents`     | integer       | Price in USD cents                |
| `sku`             | string        | Stock keeping unit                |
| `inventory_count` | integer       | Units in stock                    |
| `tags`            | array[string] | Product tags                      |
| `created_at`      | string        | ISO 8601 timestamp                |

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
curl "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer <token>"
```

---

### Create Product — `POST /products`

Create a new product in the catalog.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field             | Type          | Required | Description                       |
|-------------------|---------------|----------|-----------------------------------|
| `name`            | string        | Yes      | Product name                      |
| `description`     | string        | Yes      | Product description               |
| `price_cents`     | integer       | Yes      | Price in USD cents                |
| `sku`             | string        | Yes      | Stock keeping unit                |
| `inventory_count` | integer       | No       | Units in stock. Defaults to `0`.  |
| `tags`            | array[string] | No       | Product tags. Defaults to `[]`.   |

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

| Field             | Type          | Description                       |
|-------------------|---------------|-----------------------------------|
| `id`              | string        | Product ID                        |
| `name`            | string        | Product name                      |
| `description`     | string        | Product description               |
| `price_cents`     | integer       | Price in USD cents                |
| `sku`             | string        | Stock keeping unit                |
| `inventory_count` | integer       | Units in stock                    |
| `tags`            | array[string] | Product tags                      |
| `created_at`      | string        | ISO 8601 timestamp                |

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
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### Get Product — `GET /products/{product_id}`

Fetch a single product by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Parameter    | Type   | Required | Description       |
|--------------|--------|----------|-------------------|
| `product_id` | string | Yes      | Path param. Product ID. |

**Response** — `200 OK`

| Field             | Type          | Description                       |
|-------------------|---------------|-----------------------------------|
| `id`              | string        | Product ID                        |
| `name`            | string        | Product name                      |
| `description`     | string        | Product description               |
| `price_cents`     | integer       | Price in USD cents                |
| `sku`             | string        | Stock keeping unit                |
| `inventory_count` | integer       | Units in stock                    |
| `tags`            | array[string] | Product tags                      |
| `created_at`      | string        | ISO 8601 timestamp                |

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
curl "https://api.datastack.io/products/prod_001" \
  -H "Authorization: Bearer <token>"
```

---

## Orders

### Create Order — `POST /orders`

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. Returns the order in `pending` status.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field               | Type              | Required | Description                              |
|---------------------|-------------------|----------|------------------------------------------|
| `user_id`           | string            | Yes      | User placing the order                   |
| `items`             | array[OrderItem]  | Yes      | Line items (see below)                   |
| `shipping_address`  | string            | Yes      | Destination address                      |
| `promo_code`        | string            | No       | Promotional code. Defaults to `null`.    |
| `priority_shipping` | boolean           | No       | Request priority shipping. Defaults to `false`. |
| `gift_message`      | string            | No       | Gift message. Defaults to `null`.        |

`OrderItem` fields:

| Field              | Type    | Required | Description                    |
|--------------------|---------|----------|--------------------------------|
| `product_id`       | string  | Yes      | Product ID                     |
| `quantity`         | integer | Yes      | Number of units                |
| `unit_price_cents` | integer | Yes      | Unit price in USD cents        |

```json
{
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": null,
  "priority_shipping": false,
  "gift_message": null
}
```

**Response** — `201 Created`

| Field              | Type             | Description                              |
|--------------------|------------------|------------------------------------------|
| `id`               | string           | Order ID                                 |
| `user_id`          | string           | User who placed the order                |
| `items`            | array[OrderItem] | Line items                               |
| `shipping_address` | string           | Destination address                      |
| `status`           | string           | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `total_cents`      | integer          | Order total in USD cents                 |
| `promo_code`       | string \| null   | Promotional code applied                 |
| `tracking_number`  | string \| null   | Carrier tracking number                  |
| `created_at`       | string           | ISO 8601 timestamp                       |
| `updated_at`       | string           | ISO 8601 timestamp                       |

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
  "promo_code": null,
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl**

```bash
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105"}'
```

---

### Get Order — `GET /orders/{order_id}`

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Parameter  | Type   | Required | Description     |
|------------|--------|----------|-----------------|
| `order_id` | string | Yes      | Path param. Order ID. |

**Response** — `200 OK`

| Field              | Type             | Description                              |
|--------------------|------------------|------------------------------------------|
| `id`               | string           | Order ID                                 |
| `user_id`          | string           | User who placed the order                |
| `items`            | array[OrderItem] | Line items                               |
| `shipping_address` | string           | Destination address                      |
| `status`           | string           | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `total_cents`      | integer          | Order total in USD cents                 |
| `promo_code`       | string \| null   | Promotional code applied                 |
| `tracking_number`  | string \| null   | Carrier tracking number                  |
| `created_at`       | string           | ISO 8601 timestamp                       |
| `updated_at`       | string           | ISO 8601 timestamp                       |

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
curl "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer <token>"
```

---

### Update Order Status — `PATCH /orders/{order_id}/status`

Update the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`. Users may cancel their own `pending` orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Parameter  | Type   | Required | Description     |
|------------|--------|----------|-----------------|
| `order_id` | string | Yes      | Path param. Order ID. |

**Request Body**

| Field             | Type           | Required | Description                              |
|-------------------|----------------|----------|------------------------------------------|
| `status`          | string         | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `tracking_number` | string         | No       | Carrier tracking number. Defaults to `null`. |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

| Field              | Type             | Description                              |
|--------------------|------------------|------------------------------------------|
| `id`               | string           | Order ID                                 |
| `user_id`          | string           | User who placed the order                |
| `items`            | array[OrderItem] | Line items                               |
| `shipping_address` | string           | Destination address                      |
| `status`           | string           | Updated status                           |
| `total_cents`      | integer          | Order total in USD cents                 |
| `promo_code`       | string \| null   | Promotional code applied                 |
| `tracking_number`  | string \| null   | Carrier tracking number                  |
| `created_at`       | string           | ISO 8601 timestamp                       |
| `updated_at`       | string           | ISO 8601 timestamp                       |

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
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning               |
|------|-----------------------|
| 400  | Bad request           |
| 401  | Invalid or missing token |
| 404  | Resource not found    |
| 500  | Internal server error |
