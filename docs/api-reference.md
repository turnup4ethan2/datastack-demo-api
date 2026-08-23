# DataStack API Reference

> **API version: 2.1.0** — This document is kept in sync with `app/routes/` automatically.

## Authentication

All endpoints require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are deprecated and no longer accepted.

---

## Users

### GET /users

Return all users in the given organization.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization_id` | string (query) | Yes | Organization whose users are returned |

**Response** — `200 OK`, array of user objects

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | User ID |
| `email` | string | Email address |
| `name` | string | Display name |
| `role` | string | One of `admin`, `member`, `viewer` |
| `organization_id` | string | Owning organization ID |
| `created_at` | string | ISO 8601 timestamp |

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

### POST /users

Create a new user; requires the `admin` role on the organization.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string (email) | Yes | Must be a valid email address |
| `name` | string | Yes | Display name |
| `role` | string | No | One of `admin`, `member`, `viewer`; defaults to `member` |
| `organization_id` | string | Yes | Organization the user belongs to |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

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
  -d '{"email":"alice@datastack.io","name":"Alice","role":"admin","organization_id":"org_xyz"}'
```

---

### GET /users/{user_id}

Fetch a single user by ID.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string (path) | Yes | User ID |

**Response** — `200 OK`, user object (fields as in `GET /users`)

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

### DELETE /users/{user_id}

Permanently delete a user; you cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string (path) | Yes | User ID |

**Response** — `204 No Content`, empty body

**Curl**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### GET /products

List all products, optionally filtered by tag.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | string (query) | No | Only return products carrying this tag |

**Response** — `200 OK`, array of product objects

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Product ID |
| `name` | string | Product name |
| `description` | string | Product description |
| `price_cents` | integer | Price in USD cents |
| `sku` | string | Stock keeping unit |
| `inventory_count` | integer | Units in stock |
| `tags` | array of string | Product tags |
| `created_at` | string | ISO 8601 timestamp |

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

### POST /products

Create a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Product name |
| `description` | string | Yes | Product description |
| `price_cents` | integer | Yes | Price in USD cents |
| `sku` | string | Yes | Stock keeping unit |
| `inventory_count` | integer | No | Units in stock; defaults to `0` |
| `tags` | array of string | No | Product tags; defaults to `[]` |

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

**Response** — `201 Created`, product object (fields as in `GET /products`)

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
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### GET /products/{product_id}

Fetch a single product by ID.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | string (path) | Yes | Product ID |

**Response** — `200 OK`, product object (fields as in `GET /products`)

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

An order item (`items[]`) has the shape:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | string | Yes | Product ID |
| `quantity` | integer | Yes | Units ordered |
| `unit_price_cents` | integer | Yes | Per-unit price in USD cents |

Order `status` values: `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.

### POST /orders

Place a new order — inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | Yes | User placing the order |
| `items` | array of order item | Yes | Ordered line items |
| `shipping_address` | string | Yes | Destination address |
| `promo_code` | string \| null | No | Promotional code; defaults to `null` |
| `priority_shipping` | boolean | No | Request expedited shipping; defaults to `false` |
| `gift_message` | string \| null | No | Message included with the shipment; defaults to `null` |

```json
{
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": "SPRING10",
  "priority_shipping": true,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Order ID |
| `user_id` | string | User who placed the order |
| `items` | array of order item | Ordered line items |
| `shipping_address` | string | Destination address |
| `status` | string | Order status enum |
| `total_cents` | integer | Order total in USD cents (sum of `quantity * unit_price_cents`) |
| `promo_code` | string \| null | Promotional code applied |
| `tracking_number` | string \| null | Carrier tracking number |
| `created_at` | string | ISO 8601 timestamp |
| `updated_at` | string | ISO 8601 timestamp |

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

Note: `priority_shipping` and `gift_message` are accepted on input but are not returned in the order response.

**Curl**

```bash
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","promo_code":"SPRING10","priority_shipping":true,"gift_message":"Happy birthday!"}'
```

---

### GET /orders/{order_id}

Fetch a single order by ID; users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | string (path) | Yes | Order ID |

**Response** — `200 OK`, order object (fields as in `POST /orders`)

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

### PATCH /orders/{order_id}/status

Update an order's status — only admins may transition to `confirmed`, `shipped`, or `delivered`; users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | string (path) | Yes | Order ID |
| `status` | string (body) | Yes | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `tracking_number` | string \| null (body) | No | Carrier tracking number; defaults to `null` |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`, order object (fields as in `POST /orders`)

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
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Health

### GET /health

Service liveness check.

**Authentication**

None.

**Response** — `200 OK`

```json
{ "status": "ok" }
```

**Curl**

```bash
curl -X GET "https://api.datastack.io/health"
```

---

## Error Codes

| Code | Meaning               |
|------|-----------------------|
| 400  | Bad request           |
| 401  | Missing or invalid bearer token |
| 403  | Insufficient permissions |
| 404  | Resource not found    |
| 422  | Request validation failed |
| 500  | Internal server error |
