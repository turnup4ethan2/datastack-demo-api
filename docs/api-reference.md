# DataStack API Reference

> DataStack API `v2.1.0`. Generated from the route definitions in `app/routes/` and `app/main.py`.

## Authentication

All endpoints except `GET /health` require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are no longer supported. Requests without an `Authorization` header are rejected with `422 Unprocessable Entity`.

Base URL in the examples below: `http://localhost:8000`.

---

## Users

### `GET /users`

Returns all users in the given organization.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field             | Type     | Required | Description                         |
|-------------------|----------|----------|-------------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users to list.   |

**Response** — `200 OK`

Array of user objects:

| Field             | Type     | Description                                   |
|-------------------|----------|-----------------------------------------------|
| `id`              | `string` | User ID (e.g. `usr_abc123`).                  |
| `email`           | `string` | User email address.                           |
| `name`            | `string` | Display name.                                 |
| `role`            | `string` | One of `admin`, `member`, `viewer`.           |
| `organization_id` | `string` | Organization the user belongs to.             |
| `created_at`      | `string` | ISO 8601 creation timestamp (UTC).            |

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

### `POST /users`

Creates a new user; requires the caller to have the `admin` role on the organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type     | Required | Description                                                    |
|-------------------|----------|----------|----------------------------------------------------------------|
| `email`           | `string` | Yes      | Valid email address (validated server-side).                   |
| `name`            | `string` | Yes      | Display name.                                                  |
| `role`            | `string` | No       | One of `admin`, `member`, `viewer`. Defaults to `member`.      |
| `organization_id` | `string` | Yes      | Organization to add the user to.                               |

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
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@datastack.io", "name": "Alice", "role": "member", "organization_id": "org_xyz"}'
```

---

### `GET /users/{user_id}`

Fetches a single user by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID.    |

**Response** — `200 OK`

Returns a user object (same fields as [`GET /users`](#get-users)).

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

### `DELETE /users/{user_id}`

Permanently deletes a user; you cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description        |
|-----------|----------|----------|--------------------|
| `user_id` | `string` | Yes      | User ID to delete. |

**Response** — `204 No Content`

Empty body.

**Example**

```bash
curl -X DELETE "http://localhost:8000/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### `GET /products`

Lists all products in the catalog, optionally filtered by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type     | Required | Description                                  |
|-------|----------|----------|----------------------------------------------|
| `tag` | `string` | No       | Only return products that have this tag.     |

**Response** — `200 OK`

Array of product objects:

| Field             | Type            | Description                              |
|-------------------|-----------------|------------------------------------------|
| `id`              | `string`        | Product ID (e.g. `prod_001`).            |
| `name`            | `string`        | Product name.                            |
| `description`     | `string`        | Product description.                     |
| `price_cents`     | `integer`       | Price in USD cents (e.g. `4999` = $49.99). |
| `sku`             | `string`        | Stock keeping unit.                      |
| `inventory_count` | `integer`       | Units in stock.                          |
| `tags`            | `array[string]` | Product tags.                            |
| `created_at`      | `string`        | ISO 8601 creation timestamp (UTC).       |

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

### `POST /products`

Creates a new product in the catalog.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type            | Required | Description                                |
|-------------------|-----------------|----------|--------------------------------------------|
| `name`            | `string`        | Yes      | Product name.                              |
| `description`     | `string`        | Yes      | Product description.                       |
| `price_cents`     | `integer`       | Yes      | Price in USD cents (e.g. `4999` = $49.99). |
| `sku`             | `string`        | Yes      | Stock keeping unit.                        |
| `inventory_count` | `integer`       | No       | Units in stock. Defaults to `0`.           |
| `tags`            | `array[string]` | No       | Product tags. Defaults to `[]`.            |

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
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget Pro", "description": "Our best-selling widget.", "price_cents": 4999, "sku": "WGT-PRO-001", "inventory_count": 142, "tags": ["hardware", "featured"]}'
```

---

### `GET /products/{product_id}`

Fetches a single product by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `product_id` | `string` | Yes      | Product ID. |

**Response** — `200 OK`

Returns a product object (same fields as [`GET /products`](#get-products)).

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

### Order object

Returned by all order endpoints.

| Field              | Type                  | Description                                                                 |
|--------------------|-----------------------|-----------------------------------------------------------------------------|
| `id`               | `string`              | Order ID (e.g. `ord_001`).                                                  |
| `user_id`          | `string`              | User who placed the order.                                                  |
| `items`            | `array[OrderItem]`    | Line items (see below).                                                     |
| `shipping_address` | `string`              | Shipping address.                                                           |
| `status`           | `string`              | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.         |
| `total_cents`      | `integer`             | Order total in USD cents: sum of `quantity * unit_price_cents` over `items`. |
| `promo_code`       | `string` \| `null`    | Promo code applied to the order.                                            |
| `tracking_number`  | `string` \| `null`    | Carrier tracking number, once shipped.                                      |
| `created_at`       | `string`              | ISO 8601 creation timestamp (UTC).                                          |
| `updated_at`       | `string`              | ISO 8601 last-update timestamp (UTC).                                       |

**OrderItem**

| Field              | Type      | Description                     |
|--------------------|-----------|---------------------------------|
| `product_id`       | `string`  | Product ID.                     |
| `quantity`         | `integer` | Number of units.                |
| `unit_price_cents` | `integer` | Price per unit in USD cents.    |

---

### `POST /orders`

Places a new order; inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field               | Type               | Required | Description                                                         |
|---------------------|--------------------|----------|---------------------------------------------------------------------|
| `user_id`           | `string`           | Yes      | User placing the order.                                             |
| `items`             | `array[OrderItem]` | Yes      | Line items. Each item requires `product_id` (`string`), `quantity` (`integer`), and `unit_price_cents` (`integer`, USD cents). |
| `shipping_address`  | `string`           | Yes      | Shipping address.                                                   |
| `promo_code`        | `string` \| `null` | No       | Promo code. Defaults to `null`.                                     |
| `priority_shipping` | `boolean`          | No       | Request priority shipping. Defaults to `false`. Not echoed in the response. |
| `gift_message`      | `string` \| `null` | No       | Gift message to include with the order. Defaults to `null`. Not echoed in the response. |

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

Returns an [Order object](#order-object).

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

**Example**

```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usr_abc123", "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}], "shipping_address": "123 Main St, San Francisco, CA 94105", "promo_code": "SPRING10", "priority_shipping": true, "gift_message": "Happy birthday!"}'
```

---

### `GET /orders/{order_id}`

Fetches a single order by ID; users can only fetch their own orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID.   |

**Response** — `200 OK`

Returns an [Order object](#order-object).

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
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `PATCH /orders/{order_id}/status`

Updates an order's status; only admins can transition to `confirmed`, `shipped`, or `delivered`, and users may cancel their own `pending` orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID.   |

**Request Body**

| Field             | Type               | Required | Description                                                          |
|-------------------|--------------------|----------|----------------------------------------------------------------------|
| `status`          | `string`           | Yes      | New status. One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. Other values are rejected with `422`. |
| `tracking_number` | `string` \| `null` | No       | Carrier tracking number. Defaults to `null`.                         |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Returns the updated [Order object](#order-object).

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
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped", "tracking_number": "1Z999AA10123456784"}'
```

---

## Health

### `GET /health`

Returns service liveness status.

**Authentication:** None.

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
| 401  | Missing or invalid Bearer token                                                               |
| 403  | Authenticated but not permitted (e.g. non-admin creating users or confirming/shipping orders) |
| 404  | Resource not found                                                                            |
| 422  | Validation error — missing `Authorization` header, missing/invalid fields, invalid enum value |
| 500  | Internal server error                                                                         |

`422` responses use the standard FastAPI validation error shape:

```json
{
  "detail": [
    { "type": "int_parsing", "loc": ["body", "price_cents"], "msg": "Input should be a valid integer, unable to parse string as an integer", "input": "x" }
  ]
}
```
