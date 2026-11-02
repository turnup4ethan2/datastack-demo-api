# DataStack API Reference

DataStack API `v2.1.0` — user management, product catalog, and order processing.

## Authentication

All resource endpoints require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

The `Authorization` header is required on every `/users`, `/products`, and `/orders` endpoint. Requests that omit it are rejected with `422 Unprocessable Entity`. Query-parameter API keys (`?api_key=`) are deprecated and no longer accepted.

## Conventions

- All IDs are strings with a resource prefix (`usr_`, `prod_`, `ord_`).
- All timestamps are ISO 8601 strings in UTC (e.g. `2026-03-20T00:00:00Z`).
- All monetary amounts are integers in USD cents (e.g. `4999` = $49.99).

---

## Health

### GET /health

Returns service liveness status. No authentication required.

**Request**

No parameters.

**Response** — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `ok` when the service is up |

```json
{
  "status": "ok"
}
```

**Curl example**

```bash
curl -X GET "https://api.datastack.io/health"
```

---

## Users

User object fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | User ID |
| `email` | `string` | User email address |
| `name` | `string` | Display name |
| `role` | `string` | One of `admin`, `member`, `viewer` |
| `organization_id` | `string` | ID of the organization the user belongs to |
| `created_at` | `string` | ISO 8601 creation timestamp |

### GET /users

Returns all users in the given organization.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Query parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization_id` | `string` | Yes | Organization whose users to list |

**Response** — `200 OK`

Array of user objects.

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

### POST /users

Creates a new user. Requires the `admin` role on the organization.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | `string` (email) | Yes | User email address; must be a valid email |
| `name` | `string` | Yes | Display name |
| `role` | `string` | No | One of `admin`, `member`, `viewer`. Default: `member` |
| `organization_id` | `string` | Yes | Organization to create the user in |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

The created user object.

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
  -d '{"email": "alice@datastack.io", "name": "Alice", "role": "member", "organization_id": "org_xyz"}'
```

---

### GET /users/{user_id}

Fetches a single user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | ID of the user to fetch |

**Response** — `200 OK`

A user object.

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

### DELETE /users/{user_id}

Permanently deletes a user. You cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | ID of the user to delete |

**Response** — `204 No Content`

Empty response body.

**Curl example**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

Product object fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product ID |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents |
| `sku` | `string` | Stock keeping unit |
| `inventory_count` | `integer` | Units in stock |
| `tags` | `array[string]` | Product tags |
| `created_at` | `string` | ISO 8601 creation timestamp |

### GET /products

Lists all products in the catalog, optionally filtered by tag.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Query parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | `string` | No | Only return products with this tag |

**Response** — `200 OK`

Array of product objects.

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

### POST /products

Creates a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | Product name |
| `description` | `string` | Yes | Product description |
| `price_cents` | `integer` | Yes | Price in USD cents |
| `sku` | `string` | Yes | Stock keeping unit |
| `inventory_count` | `integer` | No | Units in stock. Default: `0` |
| `tags` | `array[string]` | No | Product tags. Default: `[]` |

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

The created product object.

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
  -d '{"name": "Widget Pro", "description": "Our best-selling widget.", "price_cents": 4999, "sku": "WGT-PRO-001", "inventory_count": 142, "tags": ["hardware", "featured"]}'
```

---

### GET /products/{product_id}

Fetches a single product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | `string` | Yes | ID of the product to fetch |

**Response** — `200 OK`

A product object.

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

Order object fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Order ID |
| `user_id` | `string` | ID of the user who placed the order |
| `items` | `array[OrderItem]` | Line items (see below) |
| `shipping_address` | `string` | Shipping address |
| `status` | `string` | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `total_cents` | `integer` | Order total in USD cents (sum of `quantity` × `unit_price_cents`) |
| `promo_code` | `string` \| `null` | Promo code applied, if any |
| `tracking_number` | `string` \| `null` | Carrier tracking number, if shipped |
| `created_at` | `string` | ISO 8601 creation timestamp |
| `updated_at` | `string` | ISO 8601 last-update timestamp |

`OrderItem` fields:

| Field | Type | Description |
|-------|------|-------------|
| `product_id` | `string` | ID of the product ordered |
| `quantity` | `integer` | Number of units |
| `unit_price_cents` | `integer` | Price per unit in USD cents |

### POST /orders

Places a new order. Inventory is reserved immediately and payment is captured asynchronously; the order is returned in `pending` status.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | ID of the user placing the order |
| `items` | `array[OrderItem]` | Yes | Line items; each requires `product_id` (`string`), `quantity` (`integer`), `unit_price_cents` (`integer`, USD cents) |
| `shipping_address` | `string` | Yes | Shipping address |
| `promo_code` | `string` | No | Promo code to apply. Default: `null` |
| `priority_shipping` | `boolean` | No | Request priority shipping. Default: `false` |
| `gift_message` | `string` | No | Gift message to include with the order. Default: `null` |

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

The created order object. `priority_shipping` and `gift_message` are accepted on input but are not included in the response.

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
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usr_abc123", "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}], "shipping_address": "123 Main St, San Francisco, CA 94105", "promo_code": "SPRING10", "priority_shipping": true, "gift_message": "Happy birthday!"}'
```

---

### GET /orders/{order_id}

Fetches a single order by ID. Users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | ID of the order to fetch |

**Response** — `200 OK`

An order object.

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

### PATCH /orders/{order_id}/status

Updates the status of an order. Only admins can transition an order to `confirmed`, `shipped`, or `delivered`; users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | ID of the order to update |

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `string` | Yes | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `tracking_number` | `string` | No | Carrier tracking number. Default: `null` |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

The updated order object.

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
  -d '{"status": "shipped", "tracking_number": "1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| `400` | Bad request |
| `401` | Missing or invalid bearer token |
| `403` | Insufficient permissions (e.g. non-admin creating users or confirming/shipping orders) |
| `404` | Resource not found |
| `422` | Validation error — missing `Authorization` header, missing required field, wrong field type, invalid email, or invalid `status` value |
| `500` | Internal server error |
