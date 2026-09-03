# DataStack API Reference

> API version `2.1.0`. This document is kept in sync with `app/routes/` automatically.

## Authentication

All endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Requests without a valid `Authorization` header are rejected. API keys passed as a query parameter (`?api_key=...`) are **not** supported.

---

## Users

Base path: `/users`

### GET /users

Return all users in the given organization.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization_id` | `string` | Yes | Organization whose users to list |

**Response** — `200 OK`

Array of user objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | User ID (e.g. `usr_abc123`) |
| `email` | `string` | Email address |
| `name` | `string` | Display name |
| `role` | `string` | One of `admin`, `member`, `viewer` |
| `organization_id` | `string` | Owning organization ID |
| `created_at` | `string` | ISO 8601 timestamp |

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
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /users

Create a new user. Requires `admin` role on the organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | `string` (email) | Yes | Must be a valid email address |
| `name` | `string` | Yes | Display name |
| `role` | `string` | No | One of `admin`, `member`, `viewer`. Defaults to `member` |
| `organization_id` | `string` | Yes | Organization to add the user to |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | User ID |
| `email` | `string` | Email address |
| `name` | `string` | Display name |
| `role` | `string` | One of `admin`, `member`, `viewer` |
| `organization_id` | `string` | Owning organization ID |
| `created_at` | `string` | ISO 8601 timestamp |

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
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"member","organization_id":"org_xyz"}'
```

---

### GET /users/{user_id}

Fetch a single user by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | User ID |

**Response** — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | User ID |
| `email` | `string` | Email address |
| `name` | `string` | Display name |
| `role` | `string` | One of `admin`, `member`, `viewer` |
| `organization_id` | `string` | Owning organization ID |
| `created_at` | `string` | ISO 8601 timestamp |

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
  -H "Authorization: Bearer $TOKEN"
```

---

### DELETE /users/{user_id}

Permanently delete a user. You cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | User ID |

**Response** — `204 No Content`

Empty body.

**Curl**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Products

Base path: `/products`

### GET /products

List all products, optionally filtered by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | `string` | No | Return only products with this tag |

**Response** — `200 OK`

Array of product objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product ID (e.g. `prod_001`) |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents |
| `sku` | `string` | Stock keeping unit |
| `inventory_count` | `integer` | Units in stock |
| `tags` | `array<string>` | Tags |
| `created_at` | `string` | ISO 8601 timestamp |

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
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /products

Create a new product in the catalog.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | Product name |
| `description` | `string` | Yes | Product description |
| `price_cents` | `integer` | Yes | Price in USD cents |
| `sku` | `string` | Yes | Stock keeping unit |
| `inventory_count` | `integer` | No | Units in stock. Defaults to `0` |
| `tags` | `array<string>` | No | Tags. Defaults to `[]` |

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product ID |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents |
| `sku` | `string` | Stock keeping unit |
| `inventory_count` | `integer` | Units in stock |
| `tags` | `array<string>` | Tags |
| `created_at` | `string` | ISO 8601 timestamp |

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
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### GET /products/{product_id}

Fetch a single product by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | `string` | Yes | Product ID |

**Response** — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product ID |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents |
| `sku` | `string` | Stock keeping unit |
| `inventory_count` | `integer` | Units in stock |
| `tags` | `array<string>` | Tags |
| `created_at` | `string` | ISO 8601 timestamp |

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
  -H "Authorization: Bearer $TOKEN"
```

---

## Orders

Base path: `/orders`

Order `status` is one of: `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.

**Order item object**

| Field | Type | Description |
|-------|------|-------------|
| `product_id` | `string` | Product ID |
| `quantity` | `integer` | Units ordered |
| `unit_price_cents` | `integer` | Price per unit in USD cents |

### POST /orders

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. The order is returned in `pending` status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | User placing the order |
| `items` | `array<OrderItem>` | Yes | Line items (see order item object above) |
| `shipping_address` | `string` | Yes | Shipping address |
| `promo_code` | `string` | No | Promotional code. Defaults to `null` |
| `priority_shipping` | `boolean` | No | Request priority shipping. Defaults to `false` |
| `gift_message` | `string` | No | Gift message to include with the order. Defaults to `null` |

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Order ID (e.g. `ord_001`) |
| `user_id` | `string` | User who placed the order |
| `items` | `array<OrderItem>` | Line items |
| `shipping_address` | `string` | Shipping address |
| `status` | `string` | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `total_cents` | `integer` | Order total in USD cents (sum of `quantity * unit_price_cents`) |
| `promo_code` | `string \| null` | Promotional code applied |
| `tracking_number` | `string \| null` | Carrier tracking number, `null` until shipped |
| `created_at` | `string` | ISO 8601 timestamp |
| `updated_at` | `string` | ISO 8601 timestamp |

Note: `priority_shipping` and `gift_message` are accepted on create but are not returned in the order object.

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
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","priority_shipping":false}'
```

---

### GET /orders/{order_id}

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | Order ID |

**Response** — `200 OK`

Same schema as the `POST /orders` response.

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
  -H "Authorization: Bearer $TOKEN"
```

---

### PATCH /orders/{order_id}/status

Update the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`. Users may cancel their own `pending` orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | Order ID |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `string` | Yes | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `tracking_number` | `string` | No | Carrier tracking number. Defaults to `null` |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Same schema as the `POST /orders` response, with the updated `status` and `tracking_number`.

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
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Health

### GET /health

Liveness check. No authentication required.

**Response** — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `ok` |

```json
{ "status": "ok" }
```

**Curl**

```bash
curl -X GET "https://api.datastack.io/health"
```

---

## Error Codes

| Code | Meaning                                   |
|------|-------------------------------------------|
| 400  | Bad request                               |
| 401  | Missing or invalid `Authorization` header |
| 404  | Resource not found                        |
| 422  | Request validation failed                 |
| 500  | Internal server error                     |
