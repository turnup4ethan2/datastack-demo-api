# DataStack API Reference

DataStack API `v2.1.0` — user management, product catalog, and order processing.

## Authentication

All resource endpoints (Users, Products, Orders) require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Requests without an `Authorization` header are rejected with `422 Unprocessable Entity`. Query-parameter API keys (`?api_key=`) are deprecated and not accepted.

Curl examples use the local development server (`uvicorn app.main:app`, `http://localhost:8000`); substitute your deployment host as needed.

All request and response bodies are JSON. Timestamps are ISO 8601 strings in UTC (e.g. `2026-03-20T00:00:00Z`). All monetary amounts are integers in USD cents.

---

## Users

### GET /users

Returns all users in the given organization.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field             | Type     | Required | Description                        |
|-------------------|----------|----------|------------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users to list.  |

**Response** — `200 OK`

Array of user objects:

| Field             | Type     | Description                                      |
|-------------------|----------|--------------------------------------------------|
| `id`              | `string` | User ID (e.g. `usr_abc123`).                     |
| `email`           | `string` | User email address.                              |
| `name`            | `string` | Display name.                                    |
| `role`            | `string` | One of `admin`, `member`, `viewer`.              |
| `organization_id` | `string` | Organization the user belongs to.                |
| `created_at`      | `string` | Creation timestamp (ISO 8601).                   |

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
curl -X GET "http://localhost:8000/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### POST /users

Creates a new user in an organization; requires the `admin` role on that organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type     | Required | Description                                                        |
|-------------------|----------|----------|--------------------------------------------------------------------|
| `email`           | `string` | Yes      | Valid email address (validated; invalid values return `422`).      |
| `name`            | `string` | Yes      | Display name.                                                      |
| `role`            | `string` | No       | One of `admin`, `member`, `viewer`. Defaults to `member`.          |
| `organization_id` | `string` | Yes      | Organization to add the user to.                                   |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

Returns the created user object (same fields as `GET /users`).

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
curl -X POST "http://localhost:8000/users" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@datastack.io", "name": "Alice", "role": "admin", "organization_id": "org_xyz"}'
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

Returns a user object (same fields as `GET /users`).

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
curl -X GET "http://localhost:8000/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### DELETE /users/{user_id}

Permanently deletes a user; you cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description         |
|-----------|----------|----------|---------------------|
| `user_id` | `string` | Yes      | User ID to delete.  |

**Response** — `204 No Content`

Empty response body.

**Curl**

```bash
curl -X DELETE "http://localhost:8000/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### GET /products

Lists all products in the catalog, optionally filtered by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type     | Required | Description                                  |
|-------|----------|----------|----------------------------------------------|
| `tag` | `string` | No       | Only return products that have this tag.     |

**Response** — `200 OK`

Array of product objects:

| Field             | Type       | Description                          |
|-------------------|------------|--------------------------------------|
| `id`              | `string`   | Product ID (e.g. `prod_001`).        |
| `name`            | `string`   | Product name.                        |
| `description`     | `string`   | Product description.                 |
| `price_cents`     | `integer`  | Price in USD cents (`4999` = $49.99).|
| `sku`             | `string`   | Stock keeping unit.                  |
| `inventory_count` | `integer`  | Units in stock.                      |
| `tags`            | `string[]` | Product tags.                        |
| `created_at`      | `string`   | Creation timestamp (ISO 8601).       |

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
curl -X GET "http://localhost:8000/products?tag=featured" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### POST /products

Creates a new product in the catalog.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type       | Required | Description                               |
|-------------------|------------|----------|-------------------------------------------|
| `name`            | `string`   | Yes      | Product name.                             |
| `description`     | `string`   | Yes      | Product description.                      |
| `price_cents`     | `integer`  | Yes      | Price in USD cents (`4999` = $49.99).     |
| `sku`             | `string`   | Yes      | Stock keeping unit.                       |
| `inventory_count` | `integer`  | No       | Units in stock. Defaults to `0`.          |
| `tags`            | `string[]` | No       | Product tags. Defaults to `[]`.           |

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

Returns the created product object (same fields as `GET /products`).

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
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget Pro", "description": "Our best-selling widget.", "price_cents": 4999, "sku": "WGT-PRO-001", "inventory_count": 142, "tags": ["hardware", "featured"]}'
```

---

### GET /products/{product_id}

Fetches a single product by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field        | Type     | Required | Description  |
|--------------|----------|----------|--------------|
| `product_id` | `string` | Yes      | Product ID.  |

**Response** — `200 OK`

Returns a product object (same fields as `GET /products`).

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
curl -X GET "http://localhost:8000/products/prod_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

### POST /orders

Places a new order; inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field               | Type          | Required | Description                                   |
|---------------------|---------------|----------|-----------------------------------------------|
| `user_id`           | `string`      | Yes      | User placing the order.                       |
| `items`             | `OrderItem[]` | Yes      | Line items (see below).                       |
| `shipping_address`  | `string`      | Yes      | Shipping address.                             |
| `promo_code`        | `string`      | No       | Promotional code. Defaults to `null`.         |
| `priority_shipping` | `boolean`     | No       | Request priority shipping. Defaults to `false`. |
| `gift_message`      | `string`      | No       | Gift message to include. Defaults to `null`.  |

`OrderItem`:

| Field              | Type      | Required | Description                     |
|--------------------|-----------|----------|---------------------------------|
| `product_id`       | `string`  | Yes      | Product ID.                     |
| `quantity`         | `integer` | Yes      | Number of units.                |
| `unit_price_cents` | `integer` | Yes      | Unit price in USD cents.        |

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

| Field              | Type             | Description                                                                          |
|--------------------|------------------|--------------------------------------------------------------------------------------|
| `id`               | `string`         | Order ID (e.g. `ord_001`).                                                           |
| `user_id`          | `string`         | User who placed the order.                                                           |
| `items`            | `OrderItem[]`    | Line items.                                                                          |
| `shipping_address` | `string`         | Shipping address.                                                                    |
| `status`           | `string`         | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. New orders are `pending`. |
| `total_cents`      | `integer`        | Order total in USD cents: sum of `quantity * unit_price_cents` over all items.       |
| `promo_code`       | `string \| null` | Promotional code, if any.                                                            |
| `tracking_number`  | `string \| null` | Carrier tracking number; `null` until set.                                           |
| `created_at`       | `string`         | Creation timestamp (ISO 8601).                                                       |
| `updated_at`       | `string`         | Last update timestamp (ISO 8601).                                                    |

`priority_shipping` and `gift_message` are accepted on create but are not returned in order responses.

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

**Curl**

```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usr_abc123", "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}], "shipping_address": "123 Main St, San Francisco, CA 94105", "promo_code": "SPRING10", "priority_shipping": true, "gift_message": "Happy birthday!"}'
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

Returns an order object (same fields as `POST /orders` response).

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
curl -X GET "http://localhost:8000/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### PATCH /orders/{order_id}/status

Updates an order's status; only admins can transition to `confirmed`, `shipped`, or `delivered`, and users may cancel their own `pending` orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID.   |

**Request Body**

| Field             | Type     | Required | Description                                                                              |
|-------------------|----------|----------|------------------------------------------------------------------------------------------|
| `status`          | `string` | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. Other values return `422`. |
| `tracking_number` | `string` | No       | Carrier tracking number. Defaults to `null`.                                             |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Returns the updated order object (same fields as `POST /orders` response).

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
curl -X PATCH "http://localhost:8000/orders/ord_001/status" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped", "tracking_number": "1Z999AA10123456784"}'
```

---

## System

### GET /health

Returns service health status; does not require authentication.

**Authentication:** None.

**Response** — `200 OK`

| Field    | Type     | Description           |
|----------|----------|-----------------------|
| `status` | `string` | Always `ok`.          |

```json
{ "status": "ok" }
```

**Curl**

```bash
curl -X GET "http://localhost:8000/health"
```

---

## Error Codes

| Code | Meaning                                                                                   |
|------|-------------------------------------------------------------------------------------------|
| 400  | Bad request                                                                               |
| 401  | Invalid bearer token                                                                      |
| 404  | Resource not found                                                                        |
| 422  | Validation error — missing `Authorization` header, missing/invalid fields, or invalid enum value |
| 500  | Internal server error                                                                     |
