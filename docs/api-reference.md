# DataStack API Reference

API version `2.1.0`. Examples use `http://localhost:8000` (the local `uvicorn app.main:app` default) as the base URL; replace it with your deployment's host.

## Authentication

All endpoints under `/users`, `/products`, and `/orders` require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are deprecated and no longer accepted. Requests missing the `Authorization` header are rejected with `422 Unprocessable Entity`.

---

## Health

### GET /health

Returns service liveness status. Does not require authentication.

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
curl http://localhost:8000/health
```

---

## Users

User object fields (returned by all user endpoints except `DELETE`):

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | User ID, e.g. `usr_abc123` |
| `email` | `string` | User email address |
| `name` | `string` | Display name |
| `role` | `string` | One of `admin`, `member`, `viewer` |
| `organization_id` | `string` | ID of the organization the user belongs to |
| `created_at` | `string` | ISO 8601 timestamp (UTC) |

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
curl "http://localhost:8000/users?organization_id=org_xyz" \
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
| `email` | `string` (email) | Yes | Must be a valid email address |
| `name` | `string` | Yes | Display name |
| `organization_id` | `string` | Yes | Organization to add the user to |
| `role` | `string` | No | One of `admin`, `member`, `viewer`. Defaults to `member` |

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
curl -X POST http://localhost:8000/users \
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
| `user_id` | `string` | Yes | User ID |

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
curl http://localhost:8000/users/usr_abc123 \
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

Empty body.

**Curl example**

```bash
curl -X DELETE http://localhost:8000/users/usr_abc123 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

Product object fields (returned by all product endpoints):

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product ID, e.g. `prod_001` |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents (e.g. `4999` = $49.99) |
| `sku` | `string` | Stock keeping unit |
| `inventory_count` | `integer` | Units in stock |
| `tags` | `array<string>` | Tags attached to the product |
| `created_at` | `string` | ISO 8601 timestamp (UTC) |

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
curl "http://localhost:8000/products?tag=featured" \
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
curl -X POST http://localhost:8000/products \
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
| `product_id` | `string` | Yes | Product ID |

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
curl http://localhost:8000/products/prod_001 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

Order object fields (returned by all order endpoints):

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Order ID, e.g. `ord_001` |
| `user_id` | `string` | ID of the user who placed the order |
| `items` | `array<object>` | Line items (see below) |
| `items[].product_id` | `string` | Product ID |
| `items[].quantity` | `integer` | Units ordered |
| `items[].unit_price_cents` | `integer` | Unit price in USD cents |
| `shipping_address` | `string` | Shipping address |
| `status` | `string` | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `total_cents` | `integer` | Order total in USD cents (sum of `quantity * unit_price_cents`) |
| `promo_code` | `string \| null` | Promo code applied, if any |
| `tracking_number` | `string \| null` | Carrier tracking number, if shipped |
| `created_at` | `string` | ISO 8601 timestamp (UTC) |
| `updated_at` | `string` | ISO 8601 timestamp (UTC) |

### POST /orders

Places a new order; inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | ID of the user placing the order |
| `items` | `array<object>` | Yes | Line items |
| `items[].product_id` | `string` | Yes | Product ID |
| `items[].quantity` | `integer` | Yes | Units to order |
| `items[].unit_price_cents` | `integer` | Yes | Unit price in USD cents |
| `shipping_address` | `string` | Yes | Shipping address |
| `promo_code` | `string` | No | Promo code to apply. Defaults to `null` |
| `priority_shipping` | `boolean` | No | Request priority shipping. Defaults to `false`. Not echoed in the response |
| `gift_message` | `string` | No | Gift message to include with the order. Defaults to `null`. Not echoed in the response |

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

The created order object.

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
curl -X POST http://localhost:8000/orders \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usr_abc123", "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}], "shipping_address": "123 Main St, San Francisco, CA 94105", "promo_code": "SPRING10", "priority_shipping": true, "gift_message": "Happy birthday!"}'
```

---

### GET /orders/{order_id}

Fetches a single order by ID; users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | Order ID |

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
curl http://localhost:8000/orders/ord_001 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### PATCH /orders/{order_id}/status

Updates an order's status; only admins can set `confirmed`, `shipped`, or `delivered`, while users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | Order ID |

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `string` | Yes | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. Other values return `422` |
| `tracking_number` | `string` | No | Carrier tracking number. Defaults to `null` |

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
curl -X PATCH http://localhost:8000/orders/ord_001/status \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped", "tracking_number": "1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400  | Bad request |
| 401  | Invalid or missing Bearer token |
| 404  | Resource not found |
| 422  | Request validation failed (missing/invalid field, header, or query parameter) |
| 500  | Internal server error |
