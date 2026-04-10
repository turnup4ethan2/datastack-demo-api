# DataStack API Reference

> **Last updated: April 2026** — This document is kept in sync automatically by Devin whenever route files change.

## Authentication

All API requests require a Bearer token passed in the `Authorization` header:

```
Authorization: Bearer <token>
```

---

## Health

### GET /health

Returns the health status of the API. No authentication required.

**Response** `200 OK`

```json
{
  "status": "ok"
}
```

**Curl Example**

```bash
curl https://api.datastack.io/health
```

---

## Users

### GET /users

Return all users in the given organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization_id` | `string` | Yes | The organization to list users for |

**Response** `200 OK`

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

**Curl Example**

```bash
curl -H "Authorization: Bearer <token>" \
  "https://api.datastack.io/users?organization_id=org_xyz"
```

---

### POST /users

Create a new user. Requires admin role on the organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | `string` (email) | Yes | The user's email address |
| `name` | `string` | Yes | The user's full name |
| `role` | `string` | No | One of `"admin"`, `"member"`, `"viewer"`. Defaults to `"member"` |
| `organization_id` | `string` | Yes | The organization to add the user to |

```json
{
  "email": "bob@datastack.io",
  "name": "Bob",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** `201 Created`

```json
{
  "id": "usr_abc123",
  "email": "bob@datastack.io",
  "name": "Bob",
  "role": "member",
  "organization_id": "org_xyz",
  "created_at": "2026-03-20T00:00:00Z"
}
```

**Curl Example**

```bash
curl -X POST https://api.datastack.io/users \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "bob@datastack.io",
    "name": "Bob",
    "role": "member",
    "organization_id": "org_xyz"
  }'
```

---

### GET /users/{user_id}

Fetch a single user by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | The user's unique ID |

**Response** `200 OK`

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

**Curl Example**

```bash
curl -H "Authorization: Bearer <token>" \
  https://api.datastack.io/users/usr_abc123
```

---

### DELETE /users/{user_id}

Permanently delete a user. Cannot delete your own account.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | The user's unique ID |

**Response** `204 No Content`

No response body.

**Curl Example**

```bash
curl -X DELETE -H "Authorization: Bearer <token>" \
  https://api.datastack.io/users/usr_abc123
```

---

## Products

### GET /products

List all products in the catalog. Optionally filter by tag.

**Authentication**

```
Authorization: Bearer <token>
```

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | `string` | No | Filter products by tag |

**Response** `200 OK`

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product ID |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents |
| `sku` | `string` | Stock-keeping unit identifier |
| `inventory_count` | `integer` | Current inventory quantity |
| `tags` | `string[]` | List of tags |
| `created_at` | `string` | ISO 8601 creation timestamp |

**Curl Example**

```bash
curl -H "Authorization: Bearer <token>" \
  "https://api.datastack.io/products?tag=hardware"
```

---

### POST /products

Create a new product in the catalog.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | Product name |
| `description` | `string` | Yes | Product description |
| `price_cents` | `integer` | Yes | Price in USD cents |
| `sku` | `string` | Yes | Stock-keeping unit identifier |
| `inventory_count` | `integer` | No | Initial inventory quantity. Defaults to `0` |
| `tags` | `string[]` | No | List of tags. Defaults to `[]` |

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

**Response** `201 Created`

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

**Curl Example**

```bash
curl -X POST https://api.datastack.io/products \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Widget Pro",
    "description": "Our best-selling widget.",
    "price_cents": 4999,
    "sku": "WGT-PRO-001",
    "inventory_count": 142,
    "tags": ["hardware", "featured"]
  }'
```

---

### GET /products/{product_id}

Fetch a single product by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | `string` | Yes | The product's unique ID |

**Response** `200 OK`

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

**Curl Example**

```bash
curl -H "Authorization: Bearer <token>" \
  https://api.datastack.io/products/prod_001
```

---

## Orders

### POST /orders

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. Returns the order in `"pending"` status.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | The ID of the user placing the order |
| `items` | `OrderItem[]` | Yes | List of order line items (see below) |
| `shipping_address` | `string` | Yes | Full shipping address |
| `promo_code` | `string` | No | Promotional code to apply |
| `priority_shipping` | `boolean` | No | Enable priority shipping. Defaults to `false` |
| `gift_message` | `string` | No | Optional gift message to include with the order |

Each `OrderItem` object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | `string` | Yes | The product ID |
| `quantity` | `integer` | Yes | Number of units |
| `unit_price_cents` | `integer` | Yes | Price per unit in USD cents |

```json
{
  "user_id": "usr_abc123",
  "items": [
    {
      "product_id": "prod_001",
      "quantity": 2,
      "unit_price_cents": 4999
    }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": "SAVE10",
  "priority_shipping": false,
  "gift_message": "Happy birthday!"
}
```

**Response** `201 Created`

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [
    {
      "product_id": "prod_001",
      "quantity": 2,
      "unit_price_cents": 4999
    }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "status": "pending",
  "total_cents": 9998,
  "promo_code": "SAVE10",
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl Example**

```bash
curl -X POST https://api.datastack.io/orders \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usr_abc123",
    "items": [
      {
        "product_id": "prod_001",
        "quantity": 2,
        "unit_price_cents": 4999
      }
    ],
    "shipping_address": "123 Main St, San Francisco, CA 94105"
  }'
```

---

### GET /orders/{order_id}

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | The order's unique ID |

**Response** `200 OK`

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [
    {
      "product_id": "prod_001",
      "quantity": 2,
      "unit_price_cents": 4999
    }
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

**Curl Example**

```bash
curl -H "Authorization: Bearer <token>" \
  https://api.datastack.io/orders/ord_001
```

---

### PATCH /orders/{order_id}/status

Update the status of an order. Only admins can transition to `"confirmed"`, `"shipped"`, or `"delivered"`. Users may cancel their own `"pending"` orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | The order's unique ID |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `string` | Yes | One of `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, `"cancelled"` |
| `tracking_number` | `string` | No | Shipping carrier tracking number |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** `200 OK`

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [
    {
      "product_id": "prod_001",
      "quantity": 2,
      "unit_price_cents": 4999
    }
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

**Curl Example**

```bash
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped",
    "tracking_number": "1Z999AA10123456784"
  }'
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad request |
| 401 | Unauthorized — missing or invalid Bearer token |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Internal server error |
