# DataStack API Reference

> **Last updated: May 2026** — Synced from `app/routes/`.

## Authentication

All API requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Requests without a valid token return `401`.

---

## Users

### `GET /users`

List all users in an organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Query parameters:

| Field             | Type   | Required | Description                                  |
|-------------------|--------|----------|----------------------------------------------|
| `organization_id` | string | Yes      | Organization whose users should be returned. |

**Response** — `200 OK`

| Field              | Type   | Description                                            |
|--------------------|--------|--------------------------------------------------------|
| `id`               | string | Unique user ID.                                        |
| `email`            | string | User's email address.                                  |
| `name`             | string | User's display name.                                   |
| `role`             | string | One of `admin`, `member`, `viewer`.                    |
| `organization_id`  | string | Organization the user belongs to.                      |
| `created_at`       | string | ISO 8601 timestamp.                                    |

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
curl -X GET "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `POST /users`

Create a new user. Requires `admin` role on the target organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Body fields:

| Field              | Type   | Required | Description                                              |
|--------------------|--------|----------|----------------------------------------------------------|
| `email`            | string | Yes      | Valid email address.                                     |
| `name`             | string | Yes      | User's display name.                                     |
| `role`             | string | No       | One of `admin`, `member`, `viewer`. Defaults to `member`.|
| `organization_id`  | string | Yes      | Organization to add the user to.                         |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field              | Type   | Description                                            |
|--------------------|--------|--------------------------------------------------------|
| `id`               | string | Unique user ID.                                        |
| `email`            | string | User's email address.                                  |
| `name`             | string | User's display name.                                   |
| `role`             | string | One of `admin`, `member`, `viewer`.                    |
| `organization_id`  | string | Organization the user belongs to.                      |
| `created_at`       | string | ISO 8601 timestamp.                                    |

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
curl -X POST "https://api.datastack.io/users" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@datastack.io",
    "name": "Alice",
    "role": "admin",
    "organization_id": "org_xyz"
  }'
```

---

### `GET /users/{user_id}`

Fetch a single user by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field     | Type   | Required | Description     |
|-----------|--------|----------|-----------------|
| `user_id` | string | Yes      | The user's ID.  |

**Response** — `200 OK`

| Field              | Type   | Description                                            |
|--------------------|--------|--------------------------------------------------------|
| `id`               | string | Unique user ID.                                        |
| `email`            | string | User's email address.                                  |
| `name`             | string | User's display name.                                   |
| `role`             | string | One of `admin`, `member`, `viewer`.                    |
| `organization_id`  | string | Organization the user belongs to.                      |
| `created_at`       | string | ISO 8601 timestamp.                                    |

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
curl -X GET "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `DELETE /users/{user_id}`

Permanently delete a user. You cannot delete your own account.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field     | Type   | Required | Description              |
|-----------|--------|----------|--------------------------|
| `user_id` | string | Yes      | The user's ID to delete. |

**Response** — `204 No Content`

Empty response body.

**Curl**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### `GET /products`

List all products in the catalog. Optionally filter by tag.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Query parameters:

| Field | Type   | Required | Description                                |
|-------|--------|----------|--------------------------------------------|
| `tag` | string | No       | If supplied, only products with this tag.  |

**Response** — `200 OK`

| Field              | Type           | Description                              |
|--------------------|----------------|------------------------------------------|
| `id`               | string         | Unique product ID.                       |
| `name`             | string         | Product name.                            |
| `description`     | string         | Product description.                     |
| `price_cents`      | integer        | Price in USD cents.                      |
| `sku`              | string         | Stock-keeping unit.                      |
| `inventory_count`  | integer        | Units currently in stock.                |
| `tags`             | array<string>  | Free-form tags for categorization.       |
| `created_at`       | string         | ISO 8601 timestamp.                      |

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
curl -X GET "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `POST /products`

Create a new product in the catalog.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Body fields:

| Field              | Type           | Required | Description                                       |
|--------------------|----------------|----------|---------------------------------------------------|
| `name`             | string         | Yes      | Product name.                                     |
| `description`      | string         | Yes      | Product description.                              |
| `price_cents`      | integer        | Yes      | Price in USD cents.                               |
| `sku`              | string         | Yes      | Stock-keeping unit.                               |
| `inventory_count`  | integer        | No       | Units in stock. Defaults to `0`.                  |
| `tags`             | array<string>  | No       | Free-form tags. Defaults to `[]`.                 |

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

Same schema as `GET /products` items.

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
curl -X POST "https://api.datastack.io/products" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
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

### `GET /products/{product_id}`

Fetch a single product by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field         | Type   | Required | Description        |
|---------------|--------|----------|--------------------|
| `product_id`  | string | Yes      | The product's ID.  |

**Response** — `200 OK`

Same schema as `GET /products` items.

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
curl -X GET "https://api.datastack.io/products/prod_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

### `POST /orders`

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. The order is returned in `pending` status.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Body fields:

| Field                | Type             | Required | Description                                         |
|----------------------|------------------|----------|-----------------------------------------------------|
| `user_id`            | string           | Yes      | ID of the user placing the order.                   |
| `items`              | array<OrderItem> | Yes      | One or more line items (see below).                 |
| `shipping_address`   | string           | Yes      | Full shipping address as a single string.           |
| `promo_code`         | string           | No       | Optional promo code to apply.                       |
| `priority_shipping`  | boolean          | No       | Request priority shipping. Defaults to `false`.     |
| `gift_message`       | string           | No       | Optional gift message to include with the order.    |

`OrderItem` fields:

| Field               | Type    | Required | Description                       |
|---------------------|---------|----------|-----------------------------------|
| `product_id`        | string  | Yes      | Product to order.                 |
| `quantity`          | integer | Yes      | Number of units.                  |
| `unit_price_cents`  | integer | Yes      | Per-unit price in USD cents.      |

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
  "promo_code": "WELCOME10",
  "priority_shipping": false,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

| Field              | Type             | Description                                                                        |
|--------------------|------------------|------------------------------------------------------------------------------------|
| `id`               | string           | Unique order ID.                                                                   |
| `user_id`          | string           | ID of the user who placed the order.                                               |
| `items`            | array<OrderItem> | Line items on the order.                                                           |
| `shipping_address` | string           | Shipping address.                                                                  |
| `status`           | string           | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.                |
| `total_cents`      | integer          | Total in USD cents (sum of `quantity * unit_price_cents` across items).            |
| `promo_code`       | string \| null   | Applied promo code, if any.                                                        |
| `tracking_number`  | string \| null   | Carrier tracking number, set once shipped.                                         |
| `created_at`       | string           | ISO 8601 timestamp.                                                                |
| `updated_at`       | string           | ISO 8601 timestamp.                                                                |

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
  "promo_code": "WELCOME10",
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl**

```bash
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usr_abc123",
    "items": [
      {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
    ],
    "shipping_address": "123 Main St, San Francisco, CA 94105",
    "promo_code": "WELCOME10",
    "priority_shipping": false,
    "gift_message": "Happy birthday!"
  }'
```

---

### `GET /orders/{order_id}`

Fetch a single order by ID. Non-admin users may only fetch their own orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field       | Type   | Required | Description       |
|-------------|--------|----------|-------------------|
| `order_id`  | string | Yes      | The order's ID.   |

**Response** — `200 OK`

Same schema as `POST /orders`.

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

**Curl**

```bash
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `PATCH /orders/{order_id}/status`

Update the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`. Users may cancel their own `pending` orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field       | Type   | Required | Description       |
|-------------|--------|----------|-------------------|
| `order_id`  | string | Yes      | The order's ID.   |

Body fields:

| Field              | Type   | Required | Description                                                                |
|--------------------|--------|----------|----------------------------------------------------------------------------|
| `status`           | string | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.        |
| `tracking_number`  | string | No       | Carrier tracking number; typically set when transitioning to `shipped`.    |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Same schema as `POST /orders`.

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

**Curl**

```bash
curl -X PATCH "https://api.datastack.io/orders/ord_001/status" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped",
    "tracking_number": "1Z999AA10123456784"
  }'
```

---

## Error Codes

| Code | Meaning                                    |
|------|--------------------------------------------|
| 400  | Bad request (validation error)             |
| 401  | Missing or invalid Bearer token            |
| 403  | Authenticated but not authorized           |
| 404  | Resource not found                         |
| 422  | Unprocessable entity (schema mismatch)     |
| 500  | Internal server error                      |
