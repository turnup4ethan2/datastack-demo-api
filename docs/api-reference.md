# DataStack API Reference

> **API version: 2.1.0** — This document is kept in sync with `app/routes/` automatically.

## Authentication

All API requests (except `GET /health`) require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are no longer supported.

---

## Health

### GET /health

Returns the service health status. No authentication required.

**Response** — `200 OK`

| Field    | Type     | Description  |
|----------|----------|--------------|
| `status` | `string` | Always `ok`. |

```json
{ "status": "ok" }
```

**Example**

```bash
curl https://api.datastack.io/health
```

---

## Users

### GET /users

Returns all users in the given organization.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field             | Type     | Required | Description                        |
|-------------------|----------|----------|------------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users to return |

**Response** — `200 OK` — array of User objects

| Field             | Type     | Description                                  |
|-------------------|----------|----------------------------------------------|
| `id`              | `string` | User ID                                      |
| `email`           | `string` | Email address                                |
| `name`            | `string` | Display name                                 |
| `role`            | `string` | One of `admin`, `member`, `viewer`           |
| `organization_id` | `string` | Owning organization ID                       |
| `created_at`      | `string` | ISO 8601 timestamp                           |

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
curl "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /users

Creates a new user. Requires `admin` role on the organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type     | Required | Description                                          |
|-------------------|----------|----------|------------------------------------------------------|
| `email`           | `string` | Yes      | Valid email address                                  |
| `name`            | `string` | Yes      | Display name                                         |
| `role`            | `string` | No       | One of `admin`, `member`, `viewer`. Default `member` |
| `organization_id` | `string` | Yes      | Organization to add the user to                      |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created` — User object

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
curl -X POST https://api.datastack.io/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"member","organization_id":"org_xyz"}'
```

---

### GET /users/{user_id}

Fetches a single user by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID     |

**Response** — `200 OK` — User object

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
curl https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $TOKEN"
```

---

### DELETE /users/{user_id}

Permanently deletes a user. You cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID     |

**Response** — `204 No Content` — empty body

**Example**

```bash
curl -X DELETE https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Products

### GET /products

Lists all products in the catalog, optionally filtered by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type     | Required | Description                        |
|-------|----------|----------|------------------------------------|
| `tag` | `string` | No       | Return only products with this tag |

**Response** — `200 OK` — array of Product objects

| Field             | Type       | Description                          |
|-------------------|------------|--------------------------------------|
| `id`              | `string`   | Product ID                           |
| `name`            | `string`   | Product name                         |
| `description`     | `string`   | Product description                  |
| `price_cents`     | `integer`  | Price in USD cents                   |
| `sku`             | `string`   | Stock keeping unit                   |
| `inventory_count` | `integer`  | Units in stock                       |
| `tags`            | `string[]` | Tags                                 |
| `created_at`      | `string`   | ISO 8601 timestamp                   |

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
curl "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /products

Creates a new product in the catalog.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type       | Required | Description                     |
|-------------------|------------|----------|---------------------------------|
| `name`            | `string`   | Yes      | Product name                    |
| `description`     | `string`   | Yes      | Product description             |
| `price_cents`     | `integer`  | Yes      | Price in USD cents              |
| `sku`             | `string`   | Yes      | Stock keeping unit              |
| `inventory_count` | `integer`  | No       | Units in stock. Default `0`     |
| `tags`            | `string[]` | No       | Tags. Default `[]`              |

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

**Response** — `201 Created` — Product object

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
curl -X POST https://api.datastack.io/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### GET /products/{product_id}

Fetches a single product by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `product_id` | `string` | Yes      | Product ID  |

**Response** — `200 OK` — Product object

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
curl https://api.datastack.io/products/prod_001 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Orders

### Order object

| Field              | Type             | Description                                                              |
|--------------------|------------------|--------------------------------------------------------------------------|
| `id`               | `string`         | Order ID                                                                 |
| `user_id`          | `string`         | ID of the user who placed the order                                      |
| `items`            | `OrderItem[]`    | Line items (see below)                                                   |
| `shipping_address` | `string`         | Shipping address                                                         |
| `status`           | `string`         | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`       |
| `total_cents`      | `integer`        | Order total in USD cents (sum of `quantity * unit_price_cents`)          |
| `promo_code`       | `string \| null` | Promo code applied, if any                                               |
| `tracking_number`  | `string \| null` | Carrier tracking number, if assigned                                     |
| `created_at`       | `string`         | ISO 8601 timestamp                                                       |
| `updated_at`       | `string`         | ISO 8601 timestamp                                                       |

**OrderItem**

| Field              | Type      | Required | Description             |
|--------------------|-----------|----------|-------------------------|
| `product_id`       | `string`  | Yes      | Product ID              |
| `quantity`         | `integer` | Yes      | Units ordered           |
| `unit_price_cents` | `integer` | Yes      | Unit price in USD cents |

---

### POST /orders

Places a new order. Inventory is reserved immediately; payment is captured asynchronously. The order is returned in `pending` status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field               | Type          | Required | Description                                                         |
|---------------------|---------------|----------|---------------------------------------------------------------------|
| `user_id`           | `string`      | Yes      | ID of the ordering user                                             |
| `items`             | `OrderItem[]` | Yes      | Line items                                                          |
| `shipping_address`  | `string`      | Yes      | Shipping address                                                    |
| `promo_code`        | `string`      | No       | Promo code to apply                                                 |
| `priority_shipping` | `boolean`     | No       | Request priority shipping. Default `false`                          |
| `gift_message`      | `string`      | No       | Gift message to include with the shipment                           |

> `priority_shipping` and `gift_message` are accepted on input but are not returned in the Order object.

```json
{
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": "SPRING10",
  "priority_shipping": false,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created` — Order object

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
curl -X POST https://api.datastack.io/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105"}'
```

---

### GET /orders/{order_id}

Fetches a single order by ID. Users can only fetch their own orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

**Response** — `200 OK` — Order object

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
curl https://api.datastack.io/orders/ord_001 \
  -H "Authorization: Bearer $TOKEN"
```

---

### PATCH /orders/{order_id}/status

Updates the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`; users may cancel their own `pending` orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

**Request Body**

| Field             | Type     | Required | Description                                                        |
|-------------------|----------|----------|--------------------------------------------------------------------|
| `status`          | `string` | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `tracking_number` | `string` | No       | Carrier tracking number                                            |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK` — Order object

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
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning                          |
|------|----------------------------------|
| 400  | Bad request                      |
| 401  | Missing or invalid Bearer token  |
| 404  | Resource not found               |
| 422  | Request validation failed        |
| 500  | Internal server error            |
