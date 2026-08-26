# DataStack API Reference

> **Last updated: August 2026** — Generated from `app/routes/` by Devin.

API version: `2.1.0`

## Authentication

All endpoints require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

The previous `api_key` query-parameter pattern is deprecated and is no longer accepted.

---

## Health

### GET /health

Liveness probe. No authentication required.

**Request**

No parameters.

**Response** — `200 OK`

| Field    | Type     | Description                |
|----------|----------|----------------------------|
| `status` | `string` | Always `"ok"` when healthy |

```json
{
  "status": "ok"
}
```

**Curl**

```bash
curl https://api.datastack.io/health
```

---

## Users

The user object is returned by every `/users` endpoint that has a response body.

| Field             | Type     | Description                                        |
|-------------------|----------|----------------------------------------------------|
| `id`              | `string` | User ID (e.g. `usr_abc123`)                        |
| `email`           | `string` | Email address                                      |
| `name`            | `string` | Display name                                       |
| `role`            | `string` | One of `admin`, `member`, `viewer`                  |
| `organization_id` | `string` | Organization the user belongs to                   |
| `created_at`      | `string` | ISO 8601 UTC timestamp                             |

### GET /users

Return all users in the given organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Field             | Type     | Required | Description                              |
|-------------------|----------|----------|------------------------------------------|
| `organization_id` | `string` | Yes      | Query parameter — organization to list   |

**Response** — `200 OK`

Array of user objects (see table above).

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
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### POST /users

Create a new user; requires the `admin` role on the organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field             | Type     | Required | Description                                             |
|-------------------|----------|----------|---------------------------------------------------------|
| `email`           | `string` | Yes      | Valid email address                                     |
| `name`            | `string` | Yes      | Display name                                            |
| `role`            | `string` | No       | `admin`, `member`, or `viewer` (defaults to `member`)    |
| `organization_id` | `string` | Yes      | Organization to create the user in                      |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

User object (see table above).

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
curl -X POST https://api.datastack.io/users \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"member","organization_id":"org_xyz"}'
```

---

### GET /users/{user_id}

Fetch a single user by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Field     | Type     | Required | Description             |
|-----------|----------|----------|-------------------------|
| `user_id` | `string` | Yes      | Path parameter — user ID |

**Response** — `200 OK`

User object (see table above).

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
curl https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### DELETE /users/{user_id}

Permanently delete a user; you cannot delete your own account.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Field     | Type     | Required | Description             |
|-----------|----------|----------|-------------------------|
| `user_id` | `string` | Yes      | Path parameter — user ID |

**Response** — `204 No Content`

Empty body.

**Curl**

```bash
curl -X DELETE https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

The product object is returned by every `/products` endpoint.

| Field             | Type           | Description                              |
|-------------------|----------------|------------------------------------------|
| `id`              | `string`       | Product ID (e.g. `prod_001`)             |
| `name`            | `string`       | Product name                             |
| `description`     | `string`       | Product description                      |
| `price_cents`     | `integer`      | Price in USD cents (e.g. `4999` = $49.99)|
| `sku`             | `string`       | Stock keeping unit                       |
| `inventory_count` | `integer`      | Units currently in stock                 |
| `tags`            | `list[string]` | Tags applied to the product              |
| `created_at`      | `string`       | ISO 8601 UTC timestamp                   |

### GET /products

List all products, optionally filtered by tag.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Field | Type     | Required | Description                          |
|-------|----------|----------|--------------------------------------|
| `tag` | `string` | No       | Query parameter — filter by one tag  |

**Response** — `200 OK`

Array of product objects (see table above).

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
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### POST /products

Create a new product in the catalog.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field             | Type           | Required | Description                                   |
|-------------------|----------------|----------|-----------------------------------------------|
| `name`            | `string`       | Yes      | Product name                                  |
| `description`     | `string`       | Yes      | Product description                           |
| `price_cents`     | `integer`      | Yes      | Price in USD cents                            |
| `sku`             | `string`       | Yes      | Stock keeping unit                            |
| `inventory_count` | `integer`      | No       | Units in stock (defaults to `0`)              |
| `tags`            | `list[string]` | No       | Tags (defaults to `[]`)                       |

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

Product object (see table above).

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
curl -X POST https://api.datastack.io/products \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### GET /products/{product_id}

Fetch a single product by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Field        | Type     | Required | Description                 |
|--------------|----------|----------|-----------------------------|
| `product_id` | `string` | Yes      | Path parameter — product ID |

**Response** — `200 OK`

Product object (see table above).

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
curl https://api.datastack.io/products/prod_001 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

The order object is returned by every `/orders` endpoint.

| Field              | Type                  | Description                                                                       |
|--------------------|-----------------------|-----------------------------------------------------------------------------------|
| `id`               | `string`              | Order ID (e.g. `ord_001`)                                                         |
| `user_id`          | `string`              | User who placed the order                                                         |
| `items`            | `list[object]`        | Line items — `product_id` (`string`), `quantity` (`integer`), `unit_price_cents` (`integer`) |
| `shipping_address` | `string`              | Destination address                                                               |
| `status`           | `string`              | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`                 |
| `total_cents`      | `integer`             | Order total in USD cents (sum of `quantity * unit_price_cents`)                    |
| `promo_code`       | `string` \| `null`    | Promo code applied, if any                                                        |
| `tracking_number`  | `string` \| `null`    | Carrier tracking number once shipped                                              |
| `created_at`       | `string`              | ISO 8601 UTC timestamp                                                            |
| `updated_at`       | `string`              | ISO 8601 UTC timestamp                                                            |

Note: `priority_shipping` and `gift_message` are accepted on order creation but are not returned in the order response.

### POST /orders

Place a new order — inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field                     | Type               | Required | Description                                       |
|---------------------------|--------------------|----------|---------------------------------------------------|
| `user_id`                 | `string`           | Yes      | User placing the order                            |
| `items`                   | `list[object]`     | Yes      | Line items (see below)                            |
| `items[].product_id`      | `string`           | Yes      | Product being ordered                             |
| `items[].quantity`        | `integer`          | Yes      | Units ordered                                     |
| `items[].unit_price_cents`| `integer`          | Yes      | Per-unit price in USD cents                       |
| `shipping_address`        | `string`           | Yes      | Destination address                               |
| `promo_code`              | `string` \| `null` | No       | Promo code to apply (defaults to `null`)          |
| `priority_shipping`       | `boolean`          | No       | Request expedited shipping (defaults to `false`)  |
| `gift_message`            | `string` \| `null` | No       | Message to include with the order (defaults to `null`) |

```json
{
  "user_id": "usr_abc123",
  "items": [
    {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": null,
  "priority_shipping": false,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

Order object (see table above).

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [
    {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
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
curl -X POST https://api.datastack.io/orders \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","priority_shipping":false,"gift_message":"Happy birthday!"}'
```

---

### GET /orders/{order_id}

Fetch a single order by ID; users can only fetch their own orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Field      | Type     | Required | Description               |
|------------|----------|----------|---------------------------|
| `order_id` | `string` | Yes      | Path parameter — order ID |

**Response** — `200 OK`

Order object (see table above).

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [
    {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
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
curl https://api.datastack.io/orders/ord_001 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### PATCH /orders/{order_id}/status

Update the status of an order — only admins can transition to `confirmed`, `shipped`, or `delivered`; users may cancel their own `pending` orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

| Field      | Type     | Required | Description               |
|------------|----------|----------|---------------------------|
| `order_id` | `string` | Yes      | Path parameter — order ID |

**Request Body**

| Field             | Type               | Required | Description                                                        |
|-------------------|--------------------|----------|--------------------------------------------------------------------|
| `status`          | `string`           | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`  |
| `tracking_number` | `string` \| `null` | No       | Carrier tracking number (defaults to `null`)                       |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Order object (see table above).

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [
    {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
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
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning               |
|------|-----------------------|
| 400  | Bad request           |
| 401  | Missing or invalid bearer token |
| 403  | Insufficient role for this operation |
| 404  | Resource not found    |
| 422  | Request validation failed |
| 500  | Internal server error |
