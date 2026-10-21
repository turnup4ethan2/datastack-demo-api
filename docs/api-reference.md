# DataStack API Reference

> Generated from the route definitions in `app/routes/` and `app/main.py` (API version `2.1.0`). Examples use the local dev server (`uvicorn app.main:app`) at `http://localhost:8000`; substitute your deployment host.

## Authentication

All resource endpoints (`/users`, `/products`, `/orders`) require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are deprecated and no longer accepted. A request without the `Authorization` header fails validation with `422 Unprocessable Entity`.

---

## Users

### GET /users

Return all users in the given organization.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization_id` | `string` | Yes | Organization whose users are returned |

**Response** — `200 OK`

Array of user objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | User ID |
| `email` | `string` | User email address |
| `name` | `string` | Display name |
| `role` | `string` | One of `admin`, `member`, `viewer` |
| `organization_id` | `string` | Organization the user belongs to |
| `created_at` | `string` | ISO 8601 creation timestamp |

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

**Example**

```bash
curl -X GET "http://localhost:8000/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### POST /users

Create a new user; requires the `admin` role on the organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | `string` (email) | Yes | Must be a valid email address |
| `name` | `string` | Yes | Display name |
| `organization_id` | `string` | Yes | Organization to create the user in |
| `role` | `string` | No | One of `admin`, `member`, `viewer`. Default: `member` |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

Returns the created user object (same fields as `GET /users/{user_id}`).

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

**Example**

```bash
curl -X POST "http://localhost:8000/users" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@datastack.io", "name": "Alice", "role": "member", "organization_id": "org_xyz"}'
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
| `email` | `string` | User email address |
| `name` | `string` | Display name |
| `role` | `string` | One of `admin`, `member`, `viewer` |
| `organization_id` | `string` | Organization the user belongs to |
| `created_at` | `string` | ISO 8601 creation timestamp |

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

**Example**

```bash
curl -X GET "http://localhost:8000/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### DELETE /users/{user_id}

Permanently delete a user; you cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | ID of the user to delete |

**Response** — `204 No Content`

No response body.

**Example**

```bash
curl -X DELETE "http://localhost:8000/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### GET /products

List all products, optionally filtered by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | `string` | No | Only return products with this tag |

**Response** — `200 OK`

Array of product objects:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product ID |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents (e.g. `4999` = $49.99) |
| `sku` | `string` | Stock-keeping unit |
| `inventory_count` | `integer` | Units in stock |
| `tags` | `array[string]` | Product tags |
| `created_at` | `string` | ISO 8601 creation timestamp |

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

**Example**

```bash
curl -X GET "http://localhost:8000/products?tag=featured" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
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
| `sku` | `string` | Yes | Stock-keeping unit |
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

Returns the created product object (same fields as `GET /products/{product_id}`).

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

**Example**

```bash
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget Pro", "description": "Our best-selling widget.", "price_cents": 4999, "sku": "WGT-PRO-001", "inventory_count": 142, "tags": ["hardware", "featured"]}'
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
| `sku` | `string` | Stock-keeping unit |
| `inventory_count` | `integer` | Units in stock |
| `tags` | `array[string]` | Product tags |
| `created_at` | `string` | ISO 8601 creation timestamp |

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

**Example**

```bash
curl -X GET "http://localhost:8000/products/prod_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

**Order object**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Order ID |
| `user_id` | `string` | ID of the user who placed the order |
| `items` | `array[OrderItem]` | Line items (see below) |
| `shipping_address` | `string` | Shipping address |
| `status` | `string` | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `total_cents` | `integer` | Order total in USD cents (sum of `quantity * unit_price_cents`) |
| `promo_code` | `string` \| `null` | Promo code applied to the order |
| `tracking_number` | `string` \| `null` | Carrier tracking number, once shipped |
| `created_at` | `string` | ISO 8601 creation timestamp |
| `updated_at` | `string` | ISO 8601 last-update timestamp |

**OrderItem**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | `string` | Yes | Product ID |
| `quantity` | `integer` | Yes | Number of units |
| `unit_price_cents` | `integer` | Yes | Unit price in USD cents |

---

### POST /orders

Place a new order; inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | ID of the user placing the order |
| `items` | `array[OrderItem]` | Yes | Line items (`product_id`, `quantity`, `unit_price_cents`) |
| `shipping_address` | `string` | Yes | Shipping address |
| `promo_code` | `string` \| `null` | No | Promo code to apply. Default: `null` |
| `priority_shipping` | `boolean` | No | Request priority shipping. Default: `false` |
| `gift_message` | `string` \| `null` | No | Gift message to include with the order. Default: `null` |

Note: `priority_shipping` and `gift_message` are accepted on create but are not returned in the order object.

```json
{
  "user_id": "usr_abc123",
  "items": [
    {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": null,
  "priority_shipping": true,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

Returns the order object.

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

**Example**

```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usr_abc123", "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}], "shipping_address": "123 Main St, San Francisco, CA 94105", "priority_shipping": true, "gift_message": "Happy birthday!"}'
```

---

### GET /orders/{order_id}

Fetch a single order by ID; users can only fetch their own orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | Order ID |

**Response** — `200 OK`

Returns the order object.

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

**Example**

```bash
curl -X GET "http://localhost:8000/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### PATCH /orders/{order_id}/status

Update the status of an order; only admins can transition to `confirmed`, `shipped`, or `delivered`, and users may cancel their own `pending` orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | Order ID |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `string` | Yes | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `tracking_number` | `string` \| `null` | No | Carrier tracking number. Default: `null` |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Returns the updated order object.

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

**Example**

```bash
curl -X PATCH "http://localhost:8000/orders/ord_001/status" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped", "tracking_number": "1Z999AA10123456784"}'
```

---

## Health

### GET /health

Liveness check; does not require authentication.

**Authentication:** None

**Response** — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `ok` |

```json
{"status": "ok"}
```

**Example**

```bash
curl -X GET "http://localhost:8000/health"
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400  | Bad request |
| 401  | Invalid bearer token |
| 403  | Insufficient permissions (e.g. non-admin creating users or confirming/shipping orders) |
| 404  | Resource not found |
| 422  | Request validation failed (missing `Authorization` header, missing required field, wrong type, or invalid enum value). Body: `{"detail": [{"loc": [...], "msg": "...", "type": "..."}]}` |
| 500  | Internal server error |
