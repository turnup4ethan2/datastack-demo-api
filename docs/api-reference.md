# DataStack API Reference

Base URL for local development: `http://localhost:8000`

## Authentication

All user, product, and order endpoints require a bearer token in the
`Authorization` header:

```http
Authorization: Bearer <token>
```

The health endpoint does not require authentication.

## System

### GET /health

Returns the API health status.

**Authentication**

None.

**Request**

No path parameters, query parameters, or request body.

**Response — `200 OK`**

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Current API status. |

```json
{
  "status": "ok"
}
```

**Curl example**

```bash
curl --request GET "http://localhost:8000/health"
```

## Users

### GET /users

Returns all users in the specified organization.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Query parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization_id` | `string` | Yes | Organization whose users should be returned. |

**Response — `200 OK`**

The response is an array of user objects.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | User identifier. |
| `email` | `string` | User email address. |
| `name` | `string` | User display name. |
| `role` | `string` | User role. |
| `organization_id` | `string` | Organization identifier. |
| `created_at` | `string` | User creation timestamp. |

```json
[]
```

**Curl example**

```bash
curl --request GET \
  "http://localhost:8000/users?organization_id=org_xyz" \
  --header "Authorization: Bearer <token>"
```

### POST /users

Creates a user in an organization; the caller must have the organization admin role.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | `string` | Yes | Valid email address. |
| `name` | `string` | Yes | User display name. |
| `role` | `string` | No | User role: `admin`, `member`, or `viewer`. Defaults to `member`. |
| `organization_id` | `string` | Yes | Organization identifier. |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response — `201 Created`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | User identifier. |
| `email` | `string` | User email address. |
| `name` | `string` | User display name. |
| `role` | `string` | User role. |
| `organization_id` | `string` | Organization identifier. |
| `created_at` | `string` | User creation timestamp. |

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

**Curl example**

```bash
curl --request POST "http://localhost:8000/users" \
  --header "Authorization: Bearer <token>" \
  --header "Content-Type: application/json" \
  --data '{
    "email": "alice@datastack.io",
    "name": "Alice",
    "role": "admin",
    "organization_id": "org_xyz"
  }'
```

### GET /users/{user_id}

Fetches a user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | User identifier. |

**Response — `200 OK`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | User identifier. |
| `email` | `string` | User email address. |
| `name` | `string` | User display name. |
| `role` | `string` | User role. |
| `organization_id` | `string` | Organization identifier. |
| `created_at` | `string` | User creation timestamp. |

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
curl --request GET "http://localhost:8000/users/usr_abc123" \
  --header "Authorization: Bearer <token>"
```

### DELETE /users/{user_id}

Permanently deletes a user; callers cannot delete their own account.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | User identifier. |

**Response — `204 No Content`**

The response has no body.

**Curl example**

```bash
curl --request DELETE "http://localhost:8000/users/usr_abc123" \
  --header "Authorization: Bearer <token>"
```

## Products

### GET /products

Returns all products, optionally filtered by tag.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Query parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | `string` | No | Tag used to filter products. |

**Response — `200 OK`**

The response is an array of product objects.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product identifier. |
| `name` | `string` | Product name. |
| `description` | `string` | Product description. |
| `price_cents` | `integer` | Product price in USD cents. |
| `sku` | `string` | Stock-keeping unit. |
| `inventory_count` | `integer` | Available inventory quantity. |
| `tags` | `array<string>` | Product tags. |
| `created_at` | `string` | Product creation timestamp. |

```json
[]
```

**Curl example**

```bash
curl --request GET "http://localhost:8000/products?tag=featured" \
  --header "Authorization: Bearer <token>"
```

### POST /products

Creates a product in the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | Product name. |
| `description` | `string` | Yes | Product description. |
| `price_cents` | `integer` | Yes | Product price in USD cents. |
| `sku` | `string` | Yes | Stock-keeping unit. |
| `inventory_count` | `integer` | No | Initial inventory quantity. Defaults to `0`. |
| `tags` | `array<string>` | No | Product tags. Defaults to an empty array. |

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

**Response — `201 Created`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product identifier. |
| `name` | `string` | Product name. |
| `description` | `string` | Product description. |
| `price_cents` | `integer` | Product price in USD cents. |
| `sku` | `string` | Stock-keeping unit. |
| `inventory_count` | `integer` | Available inventory quantity. |
| `tags` | `array<string>` | Product tags. |
| `created_at` | `string` | Product creation timestamp. |

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
curl --request POST "http://localhost:8000/products" \
  --header "Authorization: Bearer <token>" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Widget Pro",
    "description": "Our best-selling widget.",
    "price_cents": 4999,
    "sku": "WGT-PRO-001",
    "inventory_count": 142,
    "tags": ["hardware", "featured"]
  }'
```

### GET /products/{product_id}

Fetches a product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | `string` | Yes | Product identifier. |

**Response — `200 OK`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Product identifier. |
| `name` | `string` | Product name. |
| `description` | `string` | Product description. |
| `price_cents` | `integer` | Product price in USD cents. |
| `sku` | `string` | Stock-keeping unit. |
| `inventory_count` | `integer` | Available inventory quantity. |
| `tags` | `array<string>` | Product tags. |
| `created_at` | `string` | Product creation timestamp. |

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
curl --request GET "http://localhost:8000/products/prod_001" \
  --header "Authorization: Bearer <token>"
```

## Orders

### POST /orders

Places an order, reserves inventory immediately, and returns it in `pending` status while payment is captured asynchronously.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | `string` | Yes | Identifier of the user placing the order. |
| `items` | `array<object>` | Yes | Items included in the order. |
| `items[].product_id` | `string` | Yes | Product identifier. |
| `items[].quantity` | `integer` | Yes | Number of units ordered. |
| `items[].unit_price_cents` | `integer` | Yes | Per-unit price in USD cents. |
| `shipping_address` | `string` | Yes | Delivery address. |
| `promo_code` | `string \| null` | No | Promotional code. Defaults to `null`. |
| `priority_shipping` | `boolean` | No | Whether priority shipping is requested. Defaults to `false`. |
| `gift_message` | `string \| null` | No | Message to include with the order. Defaults to `null`. |

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
  "priority_shipping": true,
  "gift_message": "Happy birthday!"
}
```

**Response — `201 Created`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Order identifier. |
| `user_id` | `string` | Identifier of the user who placed the order. |
| `items` | `array<object>` | Items included in the order. |
| `items[].product_id` | `string` | Product identifier. |
| `items[].quantity` | `integer` | Number of units ordered. |
| `items[].unit_price_cents` | `integer` | Per-unit price in USD cents. |
| `shipping_address` | `string` | Delivery address. |
| `status` | `string` | Order status: `pending`, `confirmed`, `shipped`, `delivered`, or `cancelled`. |
| `total_cents` | `integer` | Order total in USD cents. |
| `promo_code` | `string \| null` | Applied promotional code. |
| `tracking_number` | `string \| null` | Carrier tracking number. |
| `created_at` | `string` | Order creation timestamp. |
| `updated_at` | `string` | Most recent order update timestamp. |

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

**Curl example**

```bash
curl --request POST "http://localhost:8000/orders" \
  --header "Authorization: Bearer <token>" \
  --header "Content-Type: application/json" \
  --data '{
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
    "priority_shipping": true,
    "gift_message": "Happy birthday!"
  }'
```

### GET /orders/{order_id}

Fetches an order by ID; users may only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | Order identifier. |

**Response — `200 OK`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Order identifier. |
| `user_id` | `string` | Identifier of the user who placed the order. |
| `items` | `array<object>` | Items included in the order. |
| `items[].product_id` | `string` | Product identifier. |
| `items[].quantity` | `integer` | Number of units ordered. |
| `items[].unit_price_cents` | `integer` | Per-unit price in USD cents. |
| `shipping_address` | `string` | Delivery address. |
| `status` | `string` | Order status: `pending`, `confirmed`, `shipped`, `delivered`, or `cancelled`. |
| `total_cents` | `integer` | Order total in USD cents. |
| `promo_code` | `string \| null` | Applied promotional code. |
| `tracking_number` | `string \| null` | Carrier tracking number. |
| `created_at` | `string` | Order creation timestamp. |
| `updated_at` | `string` | Most recent order update timestamp. |

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

**Curl example**

```bash
curl --request GET "http://localhost:8000/orders/ord_001" \
  --header "Authorization: Bearer <token>"
```

### PATCH /orders/{order_id}/status

Updates an order status; admins may transition to `confirmed`, `shipped`, or `delivered`, while users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

Path parameters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | `string` | Yes | Order identifier. |

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `string` | Yes | New status: `pending`, `confirmed`, `shipped`, `delivered`, or `cancelled`. |
| `tracking_number` | `string \| null` | No | Carrier tracking number. Defaults to `null`. |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response — `200 OK`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Order identifier. |
| `user_id` | `string` | Identifier of the user who placed the order. |
| `items` | `array<object>` | Items included in the order. |
| `items[].product_id` | `string` | Product identifier. |
| `items[].quantity` | `integer` | Number of units ordered. |
| `items[].unit_price_cents` | `integer` | Per-unit price in USD cents. |
| `shipping_address` | `string` | Delivery address. |
| `status` | `string` | Order status: `pending`, `confirmed`, `shipped`, `delivered`, or `cancelled`. |
| `total_cents` | `integer` | Order total in USD cents. |
| `promo_code` | `string \| null` | Applied promotional code. |
| `tracking_number` | `string \| null` | Carrier tracking number. |
| `created_at` | `string` | Order creation timestamp. |
| `updated_at` | `string` | Most recent order update timestamp. |

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

**Curl example**

```bash
curl --request PATCH "http://localhost:8000/orders/ord_001/status" \
  --header "Authorization: Bearer <token>" \
  --header "Content-Type: application/json" \
  --data '{
    "status": "shipped",
    "tracking_number": "1Z999AA10123456784"
  }'
```
