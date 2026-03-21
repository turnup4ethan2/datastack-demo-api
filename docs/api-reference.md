# DataStack API Reference

> **Last updated: March 2026** — This document is automatically maintained by Devin.

## Authentication

All API requests require a Bearer token passed via the `Authorization` header:

```
Authorization: Bearer <token>
```

---

## Users

### List Users

```
GET /users
```

Returns all users in the given organization.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| `organization_id` | `string` | Yes | The organization to list users for |

**Response** — `200 OK`

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
|---|---|---|
| `id` | `string` | Unique user identifier |
| `email` | `string` | User email address |
| `name` | `string` | User display name |
| `role` | `string` | User role: `"admin"`, `"member"`, or `"viewer"` |
| `organization_id` | `string` | Organization the user belongs to |
| `created_at` | `string` | ISO 8601 timestamp of when the user was created |

**Curl Example**

```bash
curl -X GET "https://api.datastack.example/users?organization_id=org_xyz" \
  -H "Authorization: Bearer <token>"
```

---

### Create User

```
POST /users
```

Creates a new user. Requires admin role on the organization.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | `string` (email) | Yes | Email address for the new user |
| `name` | `string` | Yes | Display name |
| `role` | `string` | No | User role: `"admin"`, `"member"`, or `"viewer"` (default: `"member"`) |
| `organization_id` | `string` | Yes | Organization to add the user to |

```json
{
  "email": "alice@example.com",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

```json
{
  "id": "usr_abc123",
  "email": "alice@example.com",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz",
  "created_at": "2026-03-20T00:00:00Z"
}
```

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Unique user identifier |
| `email` | `string` | User email address |
| `name` | `string` | User display name |
| `role` | `string` | User role |
| `organization_id` | `string` | Organization the user belongs to |
| `created_at` | `string` | ISO 8601 timestamp of when the user was created |

**Curl Example**

```bash
curl -X POST "https://api.datastack.example/users" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "name": "Alice",
    "role": "member",
    "organization_id": "org_xyz"
  }'
```

---

### Get User

```
GET /users/{user_id}
```

Fetches a single user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| `user_id` | `string` | Yes | The user ID to fetch |

**Response** — `200 OK`

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
|---|---|---|
| `id` | `string` | Unique user identifier |
| `email` | `string` | User email address |
| `name` | `string` | User display name |
| `role` | `string` | User role |
| `organization_id` | `string` | Organization the user belongs to |
| `created_at` | `string` | ISO 8601 timestamp of when the user was created |

**Curl Example**

```bash
curl -X GET "https://api.datastack.example/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently deletes a user. Cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| `user_id` | `string` | Yes | The user ID to delete |

**Response** — `204 No Content`

No response body.

**Curl Example**

```bash
curl -X DELETE "https://api.datastack.example/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

## Products

### List Products

```
GET /products
```

Lists all products in the catalog. Optionally filter by tag.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| `tag` | `string` | No | Filter products by tag |

**Response** — `200 OK`

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
|---|---|---|
| `id` | `string` | Unique product identifier |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents |
| `sku` | `string` | Stock keeping unit |
| `inventory_count` | `integer` | Current inventory count |
| `tags` | `string[]` | List of tags |
| `created_at` | `string` | ISO 8601 timestamp of when the product was created |

**Curl Example**

```bash
curl -X GET "https://api.datastack.example/products?tag=featured" \
  -H "Authorization: Bearer <token>"
```

---

### Create Product

```
POST /products
```

Creates a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | Yes | Product name |
| `description` | `string` | Yes | Product description |
| `price_cents` | `integer` | Yes | Price in USD cents |
| `sku` | `string` | Yes | Stock keeping unit |
| `inventory_count` | `integer` | No | Initial inventory count (default: `0`) |
| `tags` | `string[]` | No | List of tags (default: `[]`) |

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
|---|---|---|
| `id` | `string` | Unique product identifier |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents |
| `sku` | `string` | Stock keeping unit |
| `inventory_count` | `integer` | Current inventory count |
| `tags` | `string[]` | List of tags |
| `created_at` | `string` | ISO 8601 timestamp of when the product was created |

**Curl Example**

```bash
curl -X POST "https://api.datastack.example/products" \
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

### Get Product

```
GET /products/{product_id}
```

Fetches a single product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| `product_id` | `string` | Yes | The product ID to fetch |

**Response** — `200 OK`

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
|---|---|---|
| `id` | `string` | Unique product identifier |
| `name` | `string` | Product name |
| `description` | `string` | Product description |
| `price_cents` | `integer` | Price in USD cents |
| `sku` | `string` | Stock keeping unit |
| `inventory_count` | `integer` | Current inventory count |
| `tags` | `string[]` | List of tags |
| `created_at` | `string` | ISO 8601 timestamp of when the product was created |

**Curl Example**

```bash
curl -X GET "https://api.datastack.example/products/prod_001" \
  -H "Authorization: Bearer <token>"
```

---

## Orders

### Create Order

```
POST /orders
```

Places a new order. Inventory is reserved immediately; payment is captured asynchronously. Returns the order in `"pending"` status.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `user_id` | `string` | Yes | ID of the user placing the order |
| `items` | `OrderItem[]` | Yes | List of order items (see below) |
| `shipping_address` | `string` | Yes | Shipping address for the order |
| `promo_code` | `string` | No | Promotional code to apply |

**`OrderItem` fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `product_id` | `string` | Yes | ID of the product being ordered |
| `quantity` | `integer` | Yes | Number of units |
| `unit_price_cents` | `integer` | Yes | Unit price in USD cents |

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

**Response** — `201 Created`

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
|---|---|---|
| `id` | `string` | Unique order identifier |
| `user_id` | `string` | ID of the user who placed the order |
| `items` | `OrderItem[]` | List of order items |
| `shipping_address` | `string` | Shipping address |
| `status` | `string` | Order status: `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, or `"cancelled"` |
| `total_cents` | `integer` | Total order amount in USD cents |
| `promo_code` | `string` or `null` | Applied promotional code |
| `tracking_number` | `string` or `null` | Shipment tracking number |
| `created_at` | `string` | ISO 8601 timestamp of order creation |
| `updated_at` | `string` | ISO 8601 timestamp of last update |

**Curl Example**

```bash
curl -X POST "https://api.datastack.example/orders" \
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

### Get Order

```
GET /orders/{order_id}
```

Fetches a single order by ID. Users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| `order_id` | `string` | Yes | The order ID to fetch |

**Response** — `200 OK`

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
|---|---|---|
| `id` | `string` | Unique order identifier |
| `user_id` | `string` | ID of the user who placed the order |
| `items` | `OrderItem[]` | List of order items |
| `shipping_address` | `string` | Shipping address |
| `status` | `string` | Order status: `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, or `"cancelled"` |
| `total_cents` | `integer` | Total order amount in USD cents |
| `promo_code` | `string` or `null` | Applied promotional code |
| `tracking_number` | `string` or `null` | Shipment tracking number |
| `created_at` | `string` | ISO 8601 timestamp of order creation |
| `updated_at` | `string` | ISO 8601 timestamp of last update |

**Curl Example**

```bash
curl -X GET "https://api.datastack.example/orders/ord_001" \
  -H "Authorization: Bearer <token>"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Updates the status of an order. Only admins can transition to `"confirmed"`, `"shipped"`, or `"delivered"`. Users may cancel their own `"pending"` orders.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| `order_id` | `string` | Yes | The order ID to update |

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `status` | `string` | Yes | New status: `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, or `"cancelled"` |
| `tracking_number` | `string` | No | Shipment tracking number (typically set when status is `"shipped"`) |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

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
|---|---|---|
| `id` | `string` | Unique order identifier |
| `user_id` | `string` | ID of the user who placed the order |
| `items` | `OrderItem[]` | List of order items |
| `shipping_address` | `string` | Shipping address |
| `status` | `string` | Order status |
| `total_cents` | `integer` | Total order amount in USD cents |
| `promo_code` | `string` or `null` | Applied promotional code |
| `tracking_number` | `string` or `null` | Shipment tracking number |
| `created_at` | `string` | ISO 8601 timestamp of order creation |
| `updated_at` | `string` | ISO 8601 timestamp of last update |

**Curl Example**

```bash
curl -X PATCH "https://api.datastack.example/orders/ord_001/status" \
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
| 401  | Unauthorized (invalid or missing Bearer token) |
| 404  | Resource not found    |
| 422  | Validation error      |
| 500  | Internal server error |
