# DataStack API Reference

DataStack API `v2.1.0` — user management, product catalog, and order processing.

Base URL used in examples: `https://api.datastack.io`

## Authentication

All `/users`, `/products`, and `/orders` endpoints require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are not supported. Requests missing the `Authorization` header are rejected with `422 Unprocessable Entity`.

---

## Users

### `GET /users`

Return all users in the given organization.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field             | Type     | Required | Description                         |
|-------------------|----------|----------|-------------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users to return. |

**Response** — `200 OK`

Array of user objects:

| Field             | Type     | Description                                  |
|-------------------|----------|----------------------------------------------|
| `id`              | `string` | User ID.                                     |
| `email`           | `string` | User email address.                          |
| `name`            | `string` | Display name.                                |
| `role`            | `string` | One of `admin`, `member`, `viewer`.          |
| `organization_id` | `string` | Organization the user belongs to.            |
| `created_at`      | `string` | ISO 8601 creation timestamp (UTC).           |

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
curl -X GET "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `POST /users`

Create a new user. Requires `admin` role on the organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type                     | Required | Description                                                     |
|-------------------|--------------------------|----------|-----------------------------------------------------------------|
| `email`           | `string` (email)         | Yes      | User email address; must be a valid email.                      |
| `name`            | `string`                 | Yes      | Display name.                                                   |
| `role`            | `string`                 | No       | One of `admin`, `member`, `viewer`. Defaults to `member`.       |
| `organization_id` | `string`                 | Yes      | Organization to add the user to.                                |

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
curl -X POST "https://api.datastack.io/users" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@datastack.io", "name": "Alice", "role": "member", "organization_id": "org_xyz"}'
```

---

### `GET /users/{user_id}`

Fetch a single user by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID.    |

**Response** — `200 OK`

| Field             | Type     | Description                                  |
|-------------------|----------|----------------------------------------------|
| `id`              | `string` | User ID.                                     |
| `email`           | `string` | User email address.                          |
| `name`            | `string` | Display name.                                |
| `role`            | `string` | One of `admin`, `member`, `viewer`.          |
| `organization_id` | `string` | Organization the user belongs to.            |
| `created_at`      | `string` | ISO 8601 creation timestamp (UTC).           |

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
curl -X GET "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `DELETE /users/{user_id}`

Permanently delete a user. You cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description         |
|-----------|----------|----------|---------------------|
| `user_id` | `string` | Yes      | ID of user to delete. |

**Response** — `204 No Content`

Empty body.

**Example**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### `GET /products`

List all products, optionally filtered by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type     | Required | Description                               |
|-------|----------|----------|-------------------------------------------|
| `tag` | `string` | No       | Only return products with this tag.       |

**Response** — `200 OK`

Array of product objects:

| Field             | Type            | Description                          |
|-------------------|-----------------|--------------------------------------|
| `id`              | `string`        | Product ID.                          |
| `name`            | `string`        | Product name.                        |
| `description`     | `string`        | Product description.                 |
| `price_cents`     | `integer`       | Price in USD cents (e.g. `4999` = $49.99). |
| `sku`             | `string`        | Stock-keeping unit.                  |
| `inventory_count` | `integer`       | Units in stock.                      |
| `tags`            | `array[string]` | Product tags.                        |
| `created_at`      | `string`        | ISO 8601 creation timestamp (UTC).   |

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
curl -X GET "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `POST /products`

Create a new product in the catalog.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type            | Required | Description                                  |
|-------------------|-----------------|----------|----------------------------------------------|
| `name`            | `string`        | Yes      | Product name.                                |
| `description`     | `string`        | Yes      | Product description.                         |
| `price_cents`     | `integer`       | Yes      | Price in USD cents (e.g. `4999` = $49.99).   |
| `sku`             | `string`        | Yes      | Stock-keeping unit.                          |
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
curl -X POST "https://api.datastack.io/products" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget Pro", "description": "Our best-selling widget.", "price_cents": 4999, "sku": "WGT-PRO-001", "inventory_count": 142, "tags": ["hardware", "featured"]}'
```

---

### `GET /products/{product_id}`

Fetch a single product by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `product_id` | `string` | Yes      | Product ID. |

**Response** — `200 OK`

| Field             | Type            | Description                          |
|-------------------|-----------------|--------------------------------------|
| `id`              | `string`        | Product ID.                          |
| `name`            | `string`        | Product name.                        |
| `description`     | `string`        | Product description.                 |
| `price_cents`     | `integer`       | Price in USD cents (e.g. `4999` = $49.99). |
| `sku`             | `string`        | Stock-keeping unit.                  |
| `inventory_count` | `integer`       | Units in stock.                      |
| `tags`            | `array[string]` | Product tags.                        |
| `created_at`      | `string`        | ISO 8601 creation timestamp (UTC).   |

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
curl -X GET "https://api.datastack.io/products/prod_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

### Order object

Returned by all order endpoints.

| Field              | Type             | Description                                                                     |
|--------------------|------------------|---------------------------------------------------------------------------------|
| `id`               | `string`         | Order ID.                                                                       |
| `user_id`          | `string`         | ID of the user who placed the order.                                            |
| `items`            | `array[object]`  | Line items; each has `product_id` (`string`), `quantity` (`integer`), `unit_price_cents` (`integer`, USD cents). |
| `shipping_address` | `string`         | Shipping address.                                                               |
| `status`           | `string`         | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.             |
| `total_cents`      | `integer`        | Order total in USD cents (sum of `quantity * unit_price_cents`).                |
| `promo_code`       | `string \| null` | Promo code applied to the order, if any.                                        |
| `tracking_number`  | `string \| null` | Carrier tracking number, if shipped.                                            |
| `created_at`       | `string`         | ISO 8601 creation timestamp (UTC).                                              |
| `updated_at`       | `string`         | ISO 8601 last-update timestamp (UTC).                                           |

---

### `POST /orders`

Place a new order. Inventory is reserved immediately and payment is captured asynchronously; the order is returned in `pending` status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field                       | Type             | Required | Description                                       |
|-----------------------------|------------------|----------|---------------------------------------------------|
| `user_id`                   | `string`         | Yes      | ID of the user placing the order.                 |
| `items`                     | `array[object]`  | Yes      | Line items (see below).                           |
| `items[].product_id`        | `string`         | Yes      | Product ID.                                       |
| `items[].quantity`          | `integer`        | Yes      | Quantity ordered.                                 |
| `items[].unit_price_cents`  | `integer`        | Yes      | Unit price in USD cents.                          |
| `shipping_address`          | `string`         | Yes      | Shipping address.                                 |
| `promo_code`                | `string \| null` | No       | Promo code to apply. Defaults to `null`.          |
| `priority_shipping`         | `boolean`        | No       | Request priority shipping. Defaults to `false`.   |
| `gift_message`              | `string \| null` | No       | Gift message to include. Defaults to `null`.      |

`priority_shipping` and `gift_message` are accepted on create but are not included in the order response.

```json
{
  "user_id": "usr_abc123",
  "items": [
    {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": "SPRING10",
  "priority_shipping": true,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

Returns an [order object](#order-object).

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
  "promo_code": "SPRING10",
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Example**

```bash
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usr_abc123", "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}], "shipping_address": "123 Main St, San Francisco, CA 94105", "promo_code": "SPRING10", "priority_shipping": true, "gift_message": "Happy birthday!"}'
```

---

### `GET /orders/{order_id}`

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID.   |

**Response** — `200 OK`

Returns an [order object](#order-object).

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
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `PATCH /orders/{order_id}/status`

Update the status of an order. Only admins can transition an order to `confirmed`, `shipped`, or `delivered`; users may cancel their own `pending` orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID.   |

**Request Body**

| Field             | Type             | Required | Description                                                         |
|-------------------|------------------|----------|---------------------------------------------------------------------|
| `status`          | `string`         | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. |
| `tracking_number` | `string \| null` | No       | Carrier tracking number. Defaults to `null`.                        |

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
curl -X PATCH "https://api.datastack.io/orders/ord_001/status" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped", "tracking_number": "1Z999AA10123456784"}'
```

---

## Health

### `GET /health`

Liveness check. Does not require authentication.

**Response** — `200 OK`

| Field    | Type     | Description       |
|----------|----------|-------------------|
| `status` | `string` | Always `ok`.      |

```json
{"status": "ok"}
```

**Example**

```bash
curl -X GET "https://api.datastack.io/health"
```

---

## Error Codes

| Code | Meaning                                                                                       |
|------|-----------------------------------------------------------------------------------------------|
| 400  | Bad request                                                                                   |
| 401  | Missing or invalid bearer token                                                               |
| 404  | Resource not found                                                                            |
| 422  | Validation error — missing `Authorization` header, missing/invalid fields, or invalid enum value |
| 500  | Internal server error                                                                         |

Validation errors (`422`) return:

```json
{
  "detail": [
    {"loc": ["body", "price_cents"], "msg": "Input should be a valid integer", "type": "int_parsing"}
  ]
}
```
