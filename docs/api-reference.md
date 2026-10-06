# DataStack API Reference

DataStack API `v2.1.0` — user management, product catalog, and order processing.

Examples below use `$BASE_URL` for the API host (e.g. `http://localhost:8000` when running locally with `uvicorn app.main:app`) and `$TOKEN` for your access token.

## Authentication

All resource endpoints (`/users`, `/products`, `/orders`) require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are no longer supported. `GET /health` does not require authentication.

---

## Health

### GET /health

Returns the service health status.

**Authentication**

None.

**Request**

No parameters.

**Response** — `200 OK`

| Field    | Type     | Description              |
|----------|----------|--------------------------|
| `status` | `string` | Always `"ok"` when up    |

```json
{
  "status": "ok"
}
```

**Curl example**

```bash
curl "$BASE_URL/health"
```

---

## Users

### GET /users

Returns all users in the given organization.

**Authentication**

`Authorization: Bearer <token>`

**Request — query parameters**

| Field             | Type     | Required | Description                         |
|-------------------|----------|----------|-------------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users to return  |

**Response** — `200 OK`

Array of user objects:

| Field             | Type     | Description                                   |
|-------------------|----------|-----------------------------------------------|
| `id`              | `string` | User ID                                       |
| `email`           | `string` | User email address                            |
| `name`            | `string` | Display name                                  |
| `role`            | `string` | `admin`, `member`, or `viewer`                |
| `organization_id` | `string` | Organization the user belongs to              |
| `created_at`      | `string` | Creation timestamp (ISO 8601)                 |

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
curl "$BASE_URL/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /users

Creates a new user. Requires the `admin` role on the organization.

**Authentication**

`Authorization: Bearer <token>`

**Request — body**

| Field             | Type              | Required | Description                                              |
|-------------------|-------------------|----------|----------------------------------------------------------|
| `email`           | `string` (email)  | Yes      | User email address; must be a valid email                |
| `name`            | `string`          | Yes      | Display name                                             |
| `role`            | `string`          | No       | `admin`, `member`, or `viewer`. Defaults to `member`     |
| `organization_id` | `string`          | Yes      | Organization to add the user to                          |

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

**Curl example**

```bash
curl -X POST "$BASE_URL/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@datastack.io", "name": "Alice", "role": "member", "organization_id": "org_xyz"}'
```

---

### GET /users/{user_id}

Fetches a single user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request — path parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID     |

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

**Curl example**

```bash
curl "$BASE_URL/users/usr_abc123" \
  -H "Authorization: Bearer $TOKEN"
```

---

### DELETE /users/{user_id}

Permanently deletes a user. You cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>`

**Request — path parameters**

| Field     | Type     | Required | Description       |
|-----------|----------|----------|-------------------|
| `user_id` | `string` | Yes      | User ID to delete |

**Response** — `204 No Content`

Empty body.

**Curl example**

```bash
curl -X DELETE "$BASE_URL/users/usr_abc123" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Products

### GET /products

Lists all products in the catalog, optionally filtered by tag.

**Authentication**

`Authorization: Bearer <token>`

**Request — query parameters**

| Field | Type     | Required | Description                          |
|-------|----------|----------|--------------------------------------|
| `tag` | `string` | No       | Only return products with this tag   |

**Response** — `200 OK`

Array of product objects:

| Field             | Type            | Description                          |
|-------------------|-----------------|--------------------------------------|
| `id`              | `string`        | Product ID                           |
| `name`            | `string`        | Product name                         |
| `description`     | `string`        | Product description                  |
| `price_cents`     | `integer`       | Price in USD cents (e.g. `4999` = $49.99) |
| `sku`             | `string`        | Stock keeping unit                   |
| `inventory_count` | `integer`       | Units in stock                       |
| `tags`            | `array[string]` | Product tags                         |
| `created_at`      | `string`        | Creation timestamp (ISO 8601)        |

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
curl "$BASE_URL/products?tag=featured" \
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /products

Creates a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request — body**

| Field             | Type            | Required | Description                                  |
|-------------------|-----------------|----------|----------------------------------------------|
| `name`            | `string`        | Yes      | Product name                                 |
| `description`     | `string`        | Yes      | Product description                          |
| `price_cents`     | `integer`       | Yes      | Price in USD cents                           |
| `sku`             | `string`        | Yes      | Stock keeping unit                           |
| `inventory_count` | `integer`       | No       | Units in stock. Defaults to `0`              |
| `tags`            | `array[string]` | No       | Product tags. Defaults to `[]`               |

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

**Curl example**

```bash
curl -X POST "$BASE_URL/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget Pro", "description": "Our best-selling widget.", "price_cents": 4999, "sku": "WGT-PRO-001", "inventory_count": 142, "tags": ["hardware", "featured"]}'
```

---

### GET /products/{product_id}

Fetches a single product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request — path parameters**

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `product_id` | `string` | Yes      | Product ID  |

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

**Curl example**

```bash
curl "$BASE_URL/products/prod_001" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Orders

### Order object

Returned by all order endpoints.

| Field              | Type             | Description                                                              |
|--------------------|------------------|--------------------------------------------------------------------------|
| `id`               | `string`         | Order ID                                                                 |
| `user_id`          | `string`         | ID of the user who placed the order                                      |
| `items`            | `array[object]`  | Line items (see below)                                                   |
| `shipping_address` | `string`         | Shipping address                                                         |
| `status`           | `string`         | `pending`, `confirmed`, `shipped`, `delivered`, or `cancelled`           |
| `total_cents`      | `integer`        | Order total in USD cents (sum of `quantity × unit_price_cents`)          |
| `promo_code`       | `string \| null` | Promo code applied to the order                                          |
| `tracking_number`  | `string \| null` | Carrier tracking number, once set                                        |
| `created_at`       | `string`         | Creation timestamp (ISO 8601)                                            |
| `updated_at`       | `string`         | Last update timestamp (ISO 8601)                                         |

Line item (`items[]`):

| Field              | Type      | Description                   |
|--------------------|-----------|-------------------------------|
| `product_id`       | `string`  | Product ID                    |
| `quantity`         | `integer` | Number of units               |
| `unit_price_cents` | `integer` | Price per unit in USD cents   |

---

### POST /orders

Places a new order; inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication**

`Authorization: Bearer <token>`

**Request — body**

| Field                        | Type             | Required | Description                                       |
|------------------------------|------------------|----------|---------------------------------------------------|
| `user_id`                    | `string`         | Yes      | ID of the user placing the order                  |
| `items`                      | `array[object]`  | Yes      | Line items                                        |
| `items[].product_id`         | `string`         | Yes      | Product ID                                        |
| `items[].quantity`           | `integer`        | Yes      | Number of units                                   |
| `items[].unit_price_cents`   | `integer`        | Yes      | Price per unit in USD cents                       |
| `shipping_address`           | `string`         | Yes      | Shipping address                                  |
| `promo_code`                 | `string \| null` | No       | Promo code to apply. Defaults to `null`           |
| `priority_shipping`          | `boolean`        | No       | Request priority shipping. Defaults to `false`    |
| `gift_message`               | `string \| null` | No       | Gift message to include. Defaults to `null`       |

> `priority_shipping` and `gift_message` are accepted on create but are not included in the order object returned by the API.

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

Returns the created [order object](#order-object).

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

**Curl example**

```bash
curl -X POST "$BASE_URL/orders" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usr_abc123", "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}], "shipping_address": "123 Main St, San Francisco, CA 94105", "priority_shipping": true, "gift_message": "Happy birthday!"}'
```

---

### GET /orders/{order_id}

Fetches a single order by ID; users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Request — path parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

**Response** — `200 OK`

Returns an [order object](#order-object).

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
curl "$BASE_URL/orders/ord_001" \
  -H "Authorization: Bearer $TOKEN"
```

---

### PATCH /orders/{order_id}/status

Updates the status of an order; only admins can transition to `confirmed`, `shipped`, or `delivered`, and users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>`

**Request — path parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

**Request — body**

| Field             | Type             | Required | Description                                                         |
|-------------------|------------------|----------|---------------------------------------------------------------------|
| `status`          | `string`         | Yes      | `pending`, `confirmed`, `shipped`, `delivered`, or `cancelled`      |
| `tracking_number` | `string \| null` | No       | Carrier tracking number. Defaults to `null`                         |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Returns the updated [order object](#order-object).

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
curl -X PATCH "$BASE_URL/orders/ord_001/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped", "tracking_number": "1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning                                                                                      |
|------|----------------------------------------------------------------------------------------------|
| 400  | Bad request                                                                                  |
| 401  | Invalid or expired Bearer token                                                              |
| 404  | Resource not found                                                                           |
| 422  | Validation error — missing/invalid body fields, query params, or `Authorization` header      |
| 500  | Internal server error                                                                        |
