# DataStack API Reference

> **Last updated: August 2026** — Generated from `app/routes/` by Devin's documentation sync.

API version: `2.1.0`

## Base URL

All examples below use `$DATASTACK_BASE_URL` for the API host (locally: `http://localhost:8000`).

## Authentication

All endpoints except `GET /health` require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are deprecated and no longer accepted.

---

## Users

### GET /users

Returns all users in the given organization.

**Authentication**

`Authorization: Bearer <token>` (required)

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization_id` | string | Yes | Organization whose users are returned |

**Response** — `200 OK`, array of user objects.

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
curl "$DATASTACK_BASE_URL/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### POST /users

Creates a new user; requires the `admin` role on the organization.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email address |
| `name` | string | Yes | Display name |
| `role` | string | No | One of `admin`, `member`, `viewer`. Defaults to `member` |
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

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | User ID |
| `email` | string | Email address |
| `name` | string | Display name |
| `role` | string | One of `admin`, `member`, `viewer` |
| `organization_id` | string | Owning organization ID |
| `created_at` | string | ISO 8601 timestamp |

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
curl -X POST "$DATASTACK_BASE_URL/users" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"admin","organization_id":"org_xyz"}'
```

---

### GET /users/{user_id}

Fetches a single user by ID.

**Authentication**

`Authorization: Bearer <token>` (required)

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | Yes | ID of the user to fetch |

**Response** — `200 OK`, a user object (same fields as `POST /users`).

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
curl "$DATASTACK_BASE_URL/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### DELETE /users/{user_id}

Permanently deletes a user; you cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>` (required)

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | Yes | ID of the user to delete |

**Response** — `204 No Content`, empty body.

**Curl**

```bash
curl -X DELETE "$DATASTACK_BASE_URL/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### GET /products

Lists all products in the catalog, optionally filtered by tag.

**Authentication**

`Authorization: Bearer <token>` (required)

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | string | No | Return only products carrying this tag |

**Response** — `200 OK`, array of product objects.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Product ID |
| `name` | string | Product name |
| `description` | string | Product description |
| `price_cents` | integer | Price in USD cents |
| `sku` | string | Stock-keeping unit |
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
curl "$DATASTACK_BASE_URL/products?tag=featured" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### POST /products

Creates a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Product name |
| `description` | string | Yes | Product description |
| `price_cents` | integer | Yes | Price in USD cents |
| `sku` | string | Yes | Stock-keeping unit |
| `inventory_count` | integer | No | Units in stock. Defaults to `0` |
| `tags` | array of string | No | Product tags. Defaults to `[]` |

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

**Response** — `201 Created`, a product object (same fields as `GET /products`).

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
curl -X POST "$DATASTACK_BASE_URL/products" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### GET /products/{product_id}

Fetches a single product by ID.

**Authentication**

`Authorization: Bearer <token>` (required)

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | string | Yes | ID of the product to fetch |

**Response** — `200 OK`, a product object (same fields as `GET /products`).

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
curl "$DATASTACK_BASE_URL/products/prod_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

### POST /orders

Places a new order: inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication**

`Authorization: Bearer <token>` (required)

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | Yes | User placing the order |
| `items` | array of item objects | Yes | Ordered line items |
| `shipping_address` | string | Yes | Destination address |
| `promo_code` | string \| null | No | Promotional code. Defaults to `null` |
| `priority_shipping` | boolean | No | Request expedited shipping. Defaults to `false` |
| `gift_message` | string \| null | No | Message included with the shipment. Defaults to `null` |

Item object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | string | Yes | Product being ordered |
| `quantity` | integer | Yes | Units ordered |
| `unit_price_cents` | integer | Yes | Price per unit in USD cents |

```json
{
  "user_id": "usr_abc123",
  "items": [
    {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
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
| `items` | array of item objects | Line items (`product_id`, `quantity`, `unit_price_cents`) |
| `shipping_address` | string | Destination address |
| `status` | string | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `total_cents` | integer | Order total in USD cents (sum of `quantity` × `unit_price_cents`) |
| `promo_code` | string \| null | Promotional code applied |
| `tracking_number` | string \| null | Carrier tracking number, `null` until shipped |
| `created_at` | string | ISO 8601 timestamp |
| `updated_at` | string | ISO 8601 timestamp |

`priority_shipping` and `gift_message` are accepted on create but are not returned in the order response.

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
  "promo_code": "SPRING10",
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl**

```bash
curl -X POST "$DATASTACK_BASE_URL/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","priority_shipping":true}'
```

---

### GET /orders/{order_id}

Fetches a single order by ID; users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>` (required)

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | string | Yes | ID of the order to fetch |

**Response** — `200 OK`, an order object (same fields as `POST /orders`).

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
curl "$DATASTACK_BASE_URL/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### PATCH /orders/{order_id}/status

Updates the status of an order; only admins may transition to `confirmed`, `shipped`, or `delivered`, while users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>` (required)

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | string | Yes | ID of the order to update |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `tracking_number` | string \| null | No | Carrier tracking number. Defaults to `null` |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`, the updated order object (same fields as `POST /orders`).

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
curl -X PATCH "$DATASTACK_BASE_URL/orders/ord_001/status" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Health

### GET /health

Returns service liveness.

**Authentication**

None.

**Response** — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Always `ok` |

```json
{"status": "ok"}
```

**Curl**

```bash
curl "$DATASTACK_BASE_URL/health"
```

---

## Error Codes

| Code | Meaning                              |
|------|--------------------------------------|
| 400  | Bad request                          |
| 401  | Missing or invalid Bearer token      |
| 403  | Insufficient role for this operation |
| 404  | Resource not found                   |
| 422  | Request validation failed            |
| 500  | Internal server error                |
