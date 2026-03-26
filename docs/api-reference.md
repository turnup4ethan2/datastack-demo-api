# DataStack API Reference

> **Last updated: March 2026** — This document is auto-generated from the source code.

## Authentication

All API requests require a Bearer token passed via the `Authorization` header:

```
Authorization: Bearer <token>
```

---

## Users

### GET /users

Return all users in the given organization.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization_id` | string | Yes | The organization to list users for |

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique user identifier |
| `email` | string | User email address |
| `name` | string | User display name |
| `role` | string | User role: `"admin"`, `"member"`, or `"viewer"` |
| `organization_id` | string | Organization the user belongs to |
| `created_at` | string | ISO 8601 timestamp of when the user was created |

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer <token>"
```

---

### POST /users

Create a new user. Requires admin role on the organization.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email address |
| `name` | string | Yes | User display name |
| `role` | string | No | User role: `"admin"`, `"member"`, or `"viewer"` (default: `"member"`) |
| `organization_id` | string | Yes | Organization to add the user to |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** `201 Created`

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique user identifier |
| `email` | string | User email address |
| `name` | string | User display name |
| `role` | string | User role: `"admin"`, `"member"`, or `"viewer"` |
| `organization_id` | string | Organization the user belongs to |
| `created_at` | string | ISO 8601 timestamp of when the user was created |

**Curl Example**

```bash
curl -X POST "https://api.datastack.io/users" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@datastack.io",
    "name": "Alice",
    "role": "member",
    "organization_id": "org_xyz"
  }'
```

---

### GET /users/{user_id}

Fetch a single user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | Yes | The user's unique identifier |

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique user identifier |
| `email` | string | User email address |
| `name` | string | User display name |
| `role` | string | User role: `"admin"`, `"member"`, or `"viewer"` |
| `organization_id` | string | Organization the user belongs to |
| `created_at` | string | ISO 8601 timestamp of when the user was created |

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

### DELETE /users/{user_id}

Permanently delete a user. Cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | Yes | The user's unique identifier |

**Response** `204 No Content`

No response body.

**Curl Example**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

## Products

### GET /products

List all products in the catalog. Optionally filter by tag.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | string | No | Filter products by tag |

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
| `id` | string | Unique product identifier |
| `name` | string | Product name |
| `description` | string | Product description |
| `price_cents` | integer | Price in USD cents |
| `sku` | string | Stock-keeping unit code |
| `inventory_count` | integer | Current inventory count |
| `tags` | array of strings | Product tags |
| `created_at` | string | ISO 8601 timestamp of when the product was created |

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer <token>"
```

---

### POST /products

Create a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Product name |
| `description` | string | Yes | Product description |
| `price_cents` | integer | Yes | Price in USD cents |
| `sku` | string | Yes | Stock-keeping unit code |
| `inventory_count` | integer | No | Initial inventory count (default: `0`) |
| `tags` | array of strings | No | Product tags (default: `[]`) |

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique product identifier |
| `name` | string | Product name |
| `description` | string | Product description |
| `price_cents` | integer | Price in USD cents |
| `sku` | string | Stock-keeping unit code |
| `inventory_count` | integer | Current inventory count |
| `tags` | array of strings | Product tags |
| `created_at` | string | ISO 8601 timestamp of when the product was created |

**Curl Example**

```bash
curl -X POST "https://api.datastack.io/products" \
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

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | string | Yes | The product's unique identifier |

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique product identifier |
| `name` | string | Product name |
| `description` | string | Product description |
| `price_cents` | integer | Price in USD cents |
| `sku` | string | Stock-keeping unit code |
| `inventory_count` | integer | Current inventory count |
| `tags` | array of strings | Product tags |
| `created_at` | string | ISO 8601 timestamp of when the product was created |

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/products/prod_001" \
  -H "Authorization: Bearer <token>"
```

---

## Orders

### POST /orders

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. Returns the order in `"pending"` status.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | Yes | The ID of the user placing the order |
| `items` | array of `OrderItem` | Yes | Line items for the order |
| `items[].product_id` | string | Yes | Product identifier |
| `items[].quantity` | integer | Yes | Quantity ordered |
| `items[].unit_price_cents` | integer | Yes | Unit price in USD cents |
| `shipping_address` | string | Yes | Full shipping address |
| `promo_code` | string | No | Optional promotional code |

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
  "promo_code": "SAVE10"
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

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique order identifier |
| `user_id` | string | The user who placed the order |
| `items` | array of `OrderItem` | Line items in the order |
| `items[].product_id` | string | Product identifier |
| `items[].quantity` | integer | Quantity ordered |
| `items[].unit_price_cents` | integer | Unit price in USD cents |
| `shipping_address` | string | Full shipping address |
| `status` | string | Order status: `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, or `"cancelled"` |
| `total_cents` | integer | Order total in USD cents |
| `promo_code` | string or null | Promotional code applied to the order |
| `tracking_number` | string or null | Shipment tracking number |
| `created_at` | string | ISO 8601 timestamp of when the order was created |
| `updated_at` | string | ISO 8601 timestamp of when the order was last updated |

**Curl Example**

```bash
curl -X POST "https://api.datastack.io/orders" \
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
    "shipping_address": "123 Main St, San Francisco, CA 94105",
    "promo_code": "SAVE10"
  }'
```

---

### GET /orders/{order_id}

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | string | Yes | The order's unique identifier |

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique order identifier |
| `user_id` | string | The user who placed the order |
| `items` | array of `OrderItem` | Line items in the order |
| `items[].product_id` | string | Product identifier |
| `items[].quantity` | integer | Quantity ordered |
| `items[].unit_price_cents` | integer | Unit price in USD cents |
| `shipping_address` | string | Full shipping address |
| `status` | string | Order status: `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, or `"cancelled"` |
| `total_cents` | integer | Order total in USD cents |
| `promo_code` | string or null | Promotional code applied to the order |
| `tracking_number` | string or null | Shipment tracking number |
| `created_at` | string | ISO 8601 timestamp of when the order was created |
| `updated_at` | string | ISO 8601 timestamp of when the order was last updated |

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer <token>"
```

---

### PATCH /orders/{order_id}/status

Update the status of an order. Only admins can transition to `"confirmed"`, `"shipped"`, or `"delivered"`. Users may cancel their own `"pending"` orders.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | string | Yes | The order's unique identifier |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | New status: `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, or `"cancelled"` |
| `tracking_number` | string | No | Shipment tracking number (typically set when status is `"shipped"`) |

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

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique order identifier |
| `user_id` | string | The user who placed the order |
| `items` | array of `OrderItem` | Line items in the order |
| `items[].product_id` | string | Product identifier |
| `items[].quantity` | integer | Quantity ordered |
| `items[].unit_price_cents` | integer | Unit price in USD cents |
| `shipping_address` | string | Full shipping address |
| `status` | string | Order status: `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, or `"cancelled"` |
| `total_cents` | integer | Order total in USD cents |
| `promo_code` | string or null | Promotional code applied to the order |
| `tracking_number` | string or null | Shipment tracking number |
| `created_at` | string | ISO 8601 timestamp of when the order was created |
| `updated_at` | string | ISO 8601 timestamp of when the order was last updated |

**Curl Example**

```bash
curl -X PATCH "https://api.datastack.io/orders/ord_001/status" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped",
    "tracking_number": "1Z999AA10123456784"
  }'
```

---

## Error Codes

| Code | Meaning               |
|------|-----------------------|
| 400  | Bad request           |
| 401  | Unauthorized          |
| 404  | Resource not found    |
| 422  | Validation error      |
| 500  | Internal server error |
