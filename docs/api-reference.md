# DataStack API Reference

DataStack core API (`v2.1.0`) — user management, product catalog, and order processing.

## Authentication

All endpoints (except `GET /health`) require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are no longer supported.

---

## System

### GET /health

Returns the service health status. No authentication required.

**Authentication**

None.

**Request**

No parameters.

**Response** — `200 OK`

| Field    | Type     | Description            |
|----------|----------|------------------------|
| `status` | `string` | Always `"ok"` when healthy |

```json
{
  "status": "ok"
}
```

**Curl example**

```bash
curl https://api.datastack.io/health
```

---

## Users

### GET /users

Returns all users in the given organization.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Query parameters:

| Field             | Type     | Required | Description                          |
|-------------------|----------|----------|--------------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users to return   |

**Response** — `200 OK`

Returns an array of user objects.

| Field             | Type     | Description                                  |
|-------------------|----------|----------------------------------------------|
| `id`              | `string` | User ID                                      |
| `email`           | `string` | User email address                           |
| `name`            | `string` | Display name                                 |
| `role`            | `string` | One of `"admin"`, `"member"`, `"viewer"`     |
| `organization_id` | `string` | Organization the user belongs to             |
| `created_at`      | `string` | ISO 8601 creation timestamp                  |

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
curl "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /users

Creates a new user. Requires the `admin` role on the organization.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field             | Type     | Required | Description                                                  |
|-------------------|----------|----------|--------------------------------------------------------------|
| `email`           | `string` | Yes      | Valid email address                                          |
| `name`            | `string` | Yes      | Display name                                                 |
| `role`            | `string` | No       | `"admin"`, `"member"`, or `"viewer"`. Defaults to `"member"` |
| `organization_id` | `string` | Yes      | Organization to add the user to                              |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field             | Type     | Description                              |
|-------------------|----------|------------------------------------------|
| `id`              | `string` | User ID                                  |
| `email`           | `string` | User email address                       |
| `name`            | `string` | Display name                             |
| `role`            | `string` | One of `"admin"`, `"member"`, `"viewer"` |
| `organization_id` | `string` | Organization the user belongs to         |
| `created_at`      | `string` | ISO 8601 creation timestamp              |

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
curl -X POST https://api.datastack.io/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"member","organization_id":"org_xyz"}'
```

---

### GET /users/{user_id}

Fetches a single user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID     |

**Response** — `200 OK`

| Field             | Type     | Description                              |
|-------------------|----------|------------------------------------------|
| `id`              | `string` | User ID                                  |
| `email`           | `string` | User email address                       |
| `name`            | `string` | Display name                             |
| `role`            | `string` | One of `"admin"`, `"member"`, `"viewer"` |
| `organization_id` | `string` | Organization the user belongs to         |
| `created_at`      | `string` | ISO 8601 creation timestamp              |

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
curl https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $TOKEN"
```

---

### DELETE /users/{user_id}

Permanently deletes a user. You cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID     |

**Response** — `204 No Content`

Empty body.

**Curl example**

```bash
curl -X DELETE https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Products

### GET /products

Lists all products in the catalog, optionally filtered by tag.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Query parameters:

| Field | Type     | Required | Description                              |
|-------|----------|----------|------------------------------------------|
| `tag` | `string` | No       | Return only products with this tag       |

**Response** — `200 OK`

Returns an array of product objects.

| Field             | Type       | Description                          |
|-------------------|------------|--------------------------------------|
| `id`              | `string`   | Product ID                           |
| `name`            | `string`   | Product name                         |
| `description`     | `string`   | Product description                  |
| `price_cents`     | `integer`  | Price in USD cents                   |
| `sku`             | `string`   | Stock keeping unit                   |
| `inventory_count` | `integer`  | Units currently in stock             |
| `tags`            | `string[]` | Tags associated with the product     |
| `created_at`      | `string`   | ISO 8601 creation timestamp          |

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
curl "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /products

Creates a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field             | Type       | Required | Description                                   |
|-------------------|------------|----------|-----------------------------------------------|
| `name`            | `string`   | Yes      | Product name                                  |
| `description`     | `string`   | Yes      | Product description                           |
| `price_cents`     | `integer`  | Yes      | Price in USD cents                            |
| `sku`             | `string`   | Yes      | Stock keeping unit                            |
| `inventory_count` | `integer`  | No       | Initial units in stock. Defaults to `0`       |
| `tags`            | `string[]` | No       | Tags for the product. Defaults to `[]`        |

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

| Field             | Type       | Description                      |
|-------------------|------------|----------------------------------|
| `id`              | `string`   | Product ID                       |
| `name`            | `string`   | Product name                     |
| `description`     | `string`   | Product description              |
| `price_cents`     | `integer`  | Price in USD cents               |
| `sku`             | `string`   | Stock keeping unit               |
| `inventory_count` | `integer`  | Units currently in stock         |
| `tags`            | `string[]` | Tags associated with the product |
| `created_at`      | `string`   | ISO 8601 creation timestamp      |

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
curl -X POST https://api.datastack.io/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### GET /products/{product_id}

Fetches a single product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `product_id` | `string` | Yes      | Product ID  |

**Response** — `200 OK`

| Field             | Type       | Description                      |
|-------------------|------------|----------------------------------|
| `id`              | `string`   | Product ID                       |
| `name`            | `string`   | Product name                     |
| `description`     | `string`   | Product description              |
| `price_cents`     | `integer`  | Price in USD cents               |
| `sku`             | `string`   | Stock keeping unit               |
| `inventory_count` | `integer`  | Units currently in stock         |
| `tags`            | `string[]` | Tags associated with the product |
| `created_at`      | `string`   | ISO 8601 creation timestamp      |

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
curl https://api.datastack.io/products/prod_001 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Orders

### Order object

| Field              | Type             | Description                                                                       |
|--------------------|------------------|-----------------------------------------------------------------------------------|
| `id`               | `string`         | Order ID                                                                          |
| `user_id`          | `string`         | ID of the user who placed the order                                               |
| `items`            | `OrderItem[]`    | Line items (see below)                                                            |
| `shipping_address` | `string`         | Shipping address                                                                  |
| `status`           | `string`         | One of `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, `"cancelled"`      |
| `total_cents`      | `integer`        | Order total in USD cents (sum of `quantity * unit_price_cents` across all items)  |
| `promo_code`       | `string \| null` | Promo code applied, if any                                                        |
| `tracking_number`  | `string \| null` | Carrier tracking number, if assigned                                              |
| `created_at`       | `string`         | ISO 8601 creation timestamp                                                       |
| `updated_at`       | `string`         | ISO 8601 last-update timestamp                                                    |

`OrderItem`:

| Field              | Type      | Description                    |
|--------------------|-----------|--------------------------------|
| `product_id`       | `string`  | Product ID                     |
| `quantity`         | `integer` | Units ordered                  |
| `unit_price_cents` | `integer` | Price per unit in USD cents    |

---

### POST /orders

Places a new order. Inventory is reserved immediately; payment is captured asynchronously. The order is returned in `"pending"` status.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field               | Type          | Required | Description                                                  |
|---------------------|---------------|----------|--------------------------------------------------------------|
| `user_id`           | `string`      | Yes      | ID of the user placing the order                             |
| `items`             | `OrderItem[]` | Yes      | Line items; each has `product_id`, `quantity`, `unit_price_cents` |
| `shipping_address`  | `string`      | Yes      | Shipping address                                             |
| `promo_code`        | `string`      | No       | Promo code to apply. Defaults to `null`                      |
| `priority_shipping` | `boolean`     | No       | Request priority shipping. Defaults to `false`               |
| `gift_message`      | `string`      | No       | Gift message to include with the order. Defaults to `null`   |

```json
{
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": "SPRING10",
  "priority_shipping": false,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

Returns an [Order object](#order-object). `priority_shipping` and `gift_message` are accepted on input but are not included in the response.

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
  "promo_code": "SPRING10",
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl example**

```bash
curl -X POST https://api.datastack.io/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","promo_code":"SPRING10","priority_shipping":false,"gift_message":"Happy birthday!"}'
```

---

### GET /orders/{order_id}

Fetches a single order by ID. Users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

**Response** — `200 OK`

Returns an [Order object](#order-object).

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
curl https://api.datastack.io/orders/ord_001 \
  -H "Authorization: Bearer $TOKEN"
```

---

### PATCH /orders/{order_id}/status

Updates the status of an order. Only admins can transition to `"confirmed"`, `"shipped"`, or `"delivered"`; users may cancel their own `"pending"` orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

Request body:

| Field             | Type     | Required | Description                                                                  |
|-------------------|----------|----------|------------------------------------------------------------------------------|
| `status`          | `string` | Yes      | One of `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, `"cancelled"` |
| `tracking_number` | `string` | No       | Carrier tracking number. Defaults to `null`                                  |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Returns the updated [Order object](#order-object).

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
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning                                   |
|------|-------------------------------------------|
| 400  | Bad request                               |
| 401  | Missing or invalid Bearer token           |
| 404  | Resource not found                        |
| 422  | Request validation failed                 |
| 500  | Internal server error                     |
