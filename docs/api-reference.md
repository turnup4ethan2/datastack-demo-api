# DataStack API Reference

> **API version 2.1.0** — Generated from `app/routes/` and kept in sync automatically.

## Authentication

All endpoints except `GET /health` require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

A missing header returns `422`; an invalid or expired token returns `401`.

---

## Health

### GET /health

Liveness probe.

**Authentication**: none.

**Response** `200 OK`

| Field    | Type     | Description     |
|----------|----------|-----------------|
| `status` | `string` | Always `"ok"`   |

```json
{ "status": "ok" }
```

```bash
curl https://api.datastack.io/health
```

---

## Users

A `User` object:

| Field             | Type     | Description                          |
|-------------------|----------|--------------------------------------|
| `id`              | `string` | User ID                              |
| `email`           | `string` | Email address                        |
| `name`            | `string` | Display name                         |
| `role`            | `string` | `admin` \| `member` \| `viewer`      |
| `organization_id` | `string` | Organization the user belongs to     |
| `created_at`      | `string` | ISO 8601 timestamp                   |

### GET /users

Return all users in the given organization.

**Authentication**: `Authorization: Bearer <token>`

**Query Parameters**

| Field             | Type     | Required | Description                      |
|-------------------|----------|----------|----------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users to list |

**Response** `200 OK` — array of `User`.

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

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.datastack.io/users?organization_id=org_xyz"
```

---

### POST /users

Create a new user; requires the `admin` role on the organization.

**Authentication**: `Authorization: Bearer <token>`

**Request Body**

| Field             | Type     | Required | Description                                          |
|-------------------|----------|----------|------------------------------------------------------|
| `email`           | `string` | Yes      | Valid email address                                  |
| `name`            | `string` | Yes      | Display name                                         |
| `role`            | `string` | No       | `admin` \| `member` \| `viewer` (default `"member"`) |
| `organization_id` | `string` | Yes      | Organization the user belongs to                     |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** `201 Created` — `User`.

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

```bash
curl -X POST https://api.datastack.io/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"admin","organization_id":"org_xyz"}'
```

---

### GET /users/{user_id}

Fetch a single user by ID.

**Authentication**: `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID     |

**Response** `200 OK` — `User`.

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

```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://api.datastack.io/users/usr_abc123
```

---

### DELETE /users/{user_id}

Permanently delete a user; you cannot delete your own account.

**Authentication**: `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID     |

**Response** `204 No Content` — empty body.

```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  https://api.datastack.io/users/usr_abc123
```

---

## Products

A `Product` object:

| Field             | Type       | Description                        |
|-------------------|------------|------------------------------------|
| `id`              | `string`   | Product ID                         |
| `name`            | `string`   | Product name                       |
| `description`     | `string`   | Product description                |
| `price_cents`     | `integer`  | Price in USD cents                 |
| `sku`             | `string`   | Stock keeping unit                 |
| `inventory_count` | `integer`  | Units in stock                     |
| `tags`            | `string[]` | Tags                               |
| `created_at`      | `string`   | ISO 8601 timestamp                 |

### GET /products

List all products, optionally filtered by tag.

**Authentication**: `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type     | Required | Description                          |
|-------|----------|----------|--------------------------------------|
| `tag` | `string` | No       | Only return products with this tag   |

**Response** `200 OK` — array of `Product`.

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

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.datastack.io/products?tag=featured"
```

---

### POST /products

Create a new product in the catalog.

**Authentication**: `Authorization: Bearer <token>`

**Request Body**

| Field             | Type       | Required | Description                    |
|-------------------|------------|----------|--------------------------------|
| `name`            | `string`   | Yes      | Product name                   |
| `description`     | `string`   | Yes      | Product description            |
| `price_cents`     | `integer`  | Yes      | Price in USD cents             |
| `sku`             | `string`   | Yes      | Stock keeping unit             |
| `inventory_count` | `integer`  | No       | Units in stock (default `0`)   |
| `tags`            | `string[]` | No       | Tags (default `[]`)            |

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

**Response** `201 Created` — `Product`.

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

```bash
curl -X POST https://api.datastack.io/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### GET /products/{product_id}

Fetch a single product by ID.

**Authentication**: `Authorization: Bearer <token>`

**Path Parameters**

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `product_id` | `string` | Yes      | Product ID  |

**Response** `200 OK` — `Product`.

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

```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://api.datastack.io/products/prod_001
```

---

## Orders

An `OrderItem` object:

| Field              | Type      | Required | Description             |
|--------------------|-----------|----------|-------------------------|
| `product_id`       | `string`  | Yes      | Product ID              |
| `quantity`         | `integer` | Yes      | Units ordered           |
| `unit_price_cents` | `integer` | Yes      | Unit price in USD cents |

An `Order` object:

| Field              | Type          | Description                                                         |
|--------------------|---------------|---------------------------------------------------------------------|
| `id`               | `string`      | Order ID                                                            |
| `user_id`          | `string`      | User who placed the order                                           |
| `items`            | `OrderItem[]` | Line items                                                          |
| `shipping_address` | `string`      | Destination address                                                 |
| `status`           | `string`      | `pending` \| `confirmed` \| `shipped` \| `delivered` \| `cancelled` |
| `total_cents`      | `integer`     | Order total in USD cents                                            |
| `promo_code`       | `string`      | Promotional code, or `null`                                         |
| `tracking_number`  | `string`      | Carrier tracking number, or `null`                                  |
| `created_at`       | `string`      | ISO 8601 timestamp                                                  |
| `updated_at`       | `string`      | ISO 8601 timestamp                                                  |

### POST /orders

Place a new order; inventory is reserved immediately and payment is captured asynchronously, so the order is returned in `pending` status with `total_cents` computed as the sum of `quantity * unit_price_cents` across all items.

**Authentication**: `Authorization: Bearer <token>`

**Request Body**

| Field               | Type          | Required | Description                          |
|---------------------|---------------|----------|--------------------------------------|
| `user_id`           | `string`      | Yes      | User placing the order               |
| `items`             | `OrderItem[]` | Yes      | Line items                           |
| `shipping_address`  | `string`      | Yes      | Destination address                  |
| `promo_code`        | `string`      | No       | Promotional code (default `null`)    |
| `priority_shipping` | `boolean`     | No       | Expedited shipping (default `false`) |
| `gift_message`      | `string`      | No       | Gift message (default `null`)        |

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

**Response** `201 Created` — `Order`.

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

```bash
curl -X POST https://api.datastack.io/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","priority_shipping":false}'
```

---

### GET /orders/{order_id}

Fetch a single order by ID; users can only fetch their own orders.

**Authentication**: `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

**Response** `200 OK` — `Order`.

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

```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://api.datastack.io/orders/ord_001
```

---

### PATCH /orders/{order_id}/status

Update the status of an order; only admins can transition an order to `confirmed`, `shipped`, or `delivered`, and users may cancel their own `pending` orders.

**Authentication**: `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

**Request Body**

| Field             | Type     | Required | Description                                                         |
|-------------------|----------|----------|---------------------------------------------------------------------|
| `status`          | `string` | Yes      | `pending` \| `confirmed` \| `shipped` \| `delivered` \| `cancelled` |
| `tracking_number` | `string` | No       | Carrier tracking number (default `null`)                            |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** `200 OK` — `Order`.

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

```bash
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning                               |
|------|---------------------------------------|
| 400  | Bad request                           |
| 401  | Invalid or expired bearer token       |
| 403  | Insufficient permissions for the role |
| 404  | Resource not found                    |
| 422  | Validation error / missing header     |
| 500  | Internal server error                 |
