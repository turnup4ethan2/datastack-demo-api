# DataStack API Reference

DataStack core API (v2.1.0) — user management, product catalog, and order processing.

Curl examples assume the API is running locally (`uvicorn app.main:app`) at `http://localhost:8000` and that `$TOKEN` holds a valid bearer token.

## Authentication

All endpoints except `GET /health` require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are no longer supported. Requests that omit the `Authorization` header are rejected with `422 Unprocessable Entity`.

---

## Users

### GET /users

Returns all users in the given organization.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field             | Type     | Required | Description                         |
|-------------------|----------|----------|-------------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users to return. |

**Response** — `200 OK`

Array of user objects.

| Field             | Type     | Description                                   |
|-------------------|----------|-----------------------------------------------|
| `id`              | `string` | User ID.                                      |
| `email`           | `string` | User email address.                           |
| `name`            | `string` | Display name.                                 |
| `role`            | `string` | One of `admin`, `member`, `viewer`.           |
| `organization_id` | `string` | Organization the user belongs to.             |
| `created_at`      | `string` | Creation timestamp (ISO 8601, UTC).           |

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
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /users

Creates a new user. Requires the `admin` role on the organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type     | Required | Description                                                      |
|-------------------|----------|----------|------------------------------------------------------------------|
| `email`           | `string` | Yes      | Email address; must be a valid email.                            |
| `name`            | `string` | Yes      | Display name.                                                    |
| `role`            | `string` | No       | One of `admin`, `member`, `viewer`. Defaults to `member`.        |
| `organization_id` | `string` | Yes      | Organization to create the user in.                              |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

Returns the created user object (same fields as [`GET /users`](#get-users)).

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
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@datastack.io", "name": "Alice", "role": "member", "organization_id": "org_xyz"}'
```

---

### GET /users/{user_id}

Fetches a single user by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID.    |

**Response** — `200 OK`

A user object (same fields as [`GET /users`](#get-users)).

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
  -H "Authorization: Bearer $TOKEN"
```

---

### DELETE /users/{user_id}

Permanently deletes a user. You cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description         |
|-----------|----------|----------|---------------------|
| `user_id` | `string` | Yes      | ID of user to delete. |

**Response** — `204 No Content`

Empty body.

**Example**

```bash
curl -X DELETE "http://localhost:8000/users/usr_abc123" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Products

### GET /products

Lists all products in the catalog, optionally filtered by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type     | Required | Description                               |
|-------|----------|----------|-------------------------------------------|
| `tag` | `string` | No       | Only return products with this tag.       |

**Response** — `200 OK`

Array of product objects.

| Field             | Type            | Description                           |
|-------------------|-----------------|---------------------------------------|
| `id`              | `string`        | Product ID.                           |
| `name`            | `string`        | Product name.                         |
| `description`     | `string`        | Product description.                  |
| `price_cents`     | `integer`       | Price in USD cents (e.g. `4999` = $49.99). |
| `sku`             | `string`        | Stock keeping unit.                   |
| `inventory_count` | `integer`       | Units in stock.                       |
| `tags`            | `array[string]` | Product tags.                         |
| `created_at`      | `string`        | Creation timestamp (ISO 8601, UTC).   |

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
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /products

Creates a new product in the catalog.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type            | Required | Description                                  |
|-------------------|-----------------|----------|----------------------------------------------|
| `name`            | `string`        | Yes      | Product name.                                |
| `description`     | `string`        | Yes      | Product description.                         |
| `price_cents`     | `integer`       | Yes      | Price in USD cents.                          |
| `sku`             | `string`        | Yes      | Stock keeping unit.                          |
| `inventory_count` | `integer`       | No       | Units in stock. Defaults to `0`.             |
| `tags`            | `array[string]` | No       | Product tags. Defaults to `[]`.              |

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

Returns the created product object (same fields as [`GET /products`](#get-products)).

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
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget Pro", "description": "Our best-selling widget.", "price_cents": 4999, "sku": "WGT-PRO-001", "inventory_count": 142, "tags": ["hardware", "featured"]}'
```

---

### GET /products/{product_id}

Fetches a single product by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `product_id` | `string` | Yes      | Product ID. |

**Response** — `200 OK`

A product object (same fields as [`GET /products`](#get-products)).

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
  -H "Authorization: Bearer $TOKEN"
```

---

## Orders

### Order object

Returned by all order endpoints.

| Field              | Type                | Description                                                                 |
|--------------------|---------------------|-----------------------------------------------------------------------------|
| `id`               | `string`            | Order ID.                                                                   |
| `user_id`          | `string`            | ID of the user who placed the order.                                        |
| `items`            | `array[OrderItem]`  | Line items (see below).                                                     |
| `shipping_address` | `string`            | Shipping address.                                                           |
| `status`           | `string`            | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.         |
| `total_cents`      | `integer`           | Order total in USD cents (sum of `quantity * unit_price_cents`).            |
| `promo_code`       | `string \| null`    | Promo code applied to the order.                                            |
| `tracking_number`  | `string \| null`    | Carrier tracking number, once shipped.                                      |
| `created_at`       | `string`            | Creation timestamp (ISO 8601, UTC).                                         |
| `updated_at`       | `string`            | Last-update timestamp (ISO 8601, UTC).                                      |

**OrderItem**

| Field              | Type      | Description                  |
|--------------------|-----------|------------------------------|
| `product_id`       | `string`  | Product ID.                  |
| `quantity`         | `integer` | Number of units.             |
| `unit_price_cents` | `integer` | Unit price in USD cents.     |

---

### POST /orders

Places a new order; inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field               | Type               | Required | Description                                                    |
|---------------------|--------------------|----------|----------------------------------------------------------------|
| `user_id`           | `string`           | Yes      | ID of the user placing the order.                              |
| `items`             | `array[OrderItem]` | Yes      | Line items; each requires `product_id` (`string`), `quantity` (`integer`), and `unit_price_cents` (`integer`, USD cents). |
| `shipping_address`  | `string`           | Yes      | Shipping address.                                              |
| `promo_code`        | `string \| null`   | No       | Promo code to apply. Defaults to `null`.                       |
| `priority_shipping` | `boolean`          | No       | Request priority shipping. Defaults to `false`. Not echoed in the response. |
| `gift_message`      | `string \| null`   | No       | Gift message to include with the order. Defaults to `null`. Not echoed in the response. |

```json
{
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": null,
  "priority_shipping": true,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

An [order object](#order-object).

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

**Example**

```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usr_abc123", "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}], "shipping_address": "123 Main St, San Francisco, CA 94105", "priority_shipping": true, "gift_message": "Happy birthday!"}'
```

---

### GET /orders/{order_id}

Fetches a single order by ID; users can only fetch their own orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID.   |

**Response** — `200 OK`

An [order object](#order-object).

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

**Example**

```bash
curl -X GET "http://localhost:8000/orders/ord_001" \
  -H "Authorization: Bearer $TOKEN"
```

---

### PATCH /orders/{order_id}/status

Updates an order's status; only admins can transition to `confirmed`, `shipped`, or `delivered`, while users may cancel their own `pending` orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID.   |

**Request Body**

| Field             | Type             | Required | Description                                                          |
|-------------------|------------------|----------|----------------------------------------------------------------------|
| `status`          | `string`         | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.  |
| `tracking_number` | `string \| null` | No       | Carrier tracking number. Defaults to `null`.                         |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

The updated [order object](#order-object).

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

**Example**

```bash
curl -X PATCH "http://localhost:8000/orders/ord_001/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped", "tracking_number": "1Z999AA10123456784"}'
```

---

## Health

### GET /health

Returns service health. Does not require authentication.

**Response** — `200 OK`

| Field    | Type     | Description       |
|----------|----------|-------------------|
| `status` | `string` | Always `ok`.      |

```json
{ "status": "ok" }
```

**Example**

```bash
curl -X GET "http://localhost:8000/health"
```

---

## Error Codes

| Code | Meaning                                                                                       |
|------|-----------------------------------------------------------------------------------------------|
| 400  | Bad request                                                                                   |
| 401  | Invalid or missing credentials                                                                |
| 404  | Resource not found                                                                            |
| 422  | Validation error — missing/invalid body fields, query params, enum values, or missing `Authorization` header |
| 500  | Internal server error                                                                         |
