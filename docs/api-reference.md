# DataStack API Reference

> API version `2.1.0`. This document is kept in sync with `app/routes/` automatically.

## Authentication

All endpoints except `GET /health` require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are deprecated and no longer accepted.

---

## Health

### GET /health

Liveness probe. Requires no authentication.

**Request**

No parameters.

**Response** — `200 OK`

| Field    | Type   | Description                |
|----------|--------|----------------------------|
| `status` | string | Always `ok` when healthy.  |

```json
{ "status": "ok" }
```

**Curl**

```bash
curl https://api.datastack.io/health
```

---

## Users

### GET /users

Return all users in the given organization.

**Authentication**

`Authorization: Bearer <token>`

**Request**

| Field             | Type   | Required | Description                        |
|-------------------|--------|----------|------------------------------------|
| `organization_id` | string | Yes      | Query param. Organization to list. |

**Response** — `200 OK`, array of user objects

| Field             | Type   | Description                                    |
|-------------------|--------|------------------------------------------------|
| `id`              | string | User ID.                                       |
| `email`           | string | Email address.                                 |
| `name`            | string | Display name.                                  |
| `role`            | string | One of `admin`, `member`, `viewer`.            |
| `organization_id` | string | Organization the user belongs to.              |
| `created_at`      | string | ISO 8601 timestamp.                            |

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
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.datastack.io/users?organization_id=org_xyz"
```

---

### POST /users

Create a new user. Requires admin role on the organization.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field             | Type   | Required | Description                                             |
|-------------------|--------|----------|---------------------------------------------------------|
| `email`           | string | Yes      | Valid email address.                                    |
| `name`            | string | Yes      | Display name.                                           |
| `role`            | string | No       | One of `admin`, `member`, `viewer`. Default `member`.   |
| `organization_id` | string | Yes      | Organization to create the user in.                     |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

Same fields as the user object in `GET /users`.

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
curl -X POST https://api.datastack.io/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"admin","organization_id":"org_xyz"}'
```

---

### GET /users/{user_id}

Fetch a single user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request**

| Field     | Type   | Required | Description             |
|-----------|--------|----------|-------------------------|
| `user_id` | string | Yes      | Path param. User ID.    |

**Response** — `200 OK`

Same fields as the user object in `GET /users`.

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
curl -H "Authorization: Bearer $TOKEN" \
  https://api.datastack.io/users/usr_abc123
```

---

### DELETE /users/{user_id}

Permanently delete a user. You cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>`

**Request**

| Field     | Type   | Required | Description                     |
|-----------|--------|----------|---------------------------------|
| `user_id` | string | Yes      | Path param. User to delete.     |

**Response** — `204 No Content`, empty body.

**Curl**

```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  https://api.datastack.io/users/usr_abc123
```

---

## Products

### GET /products

List all products. Optionally filter by tag.

**Authentication**

`Authorization: Bearer <token>`

**Request**

| Field | Type   | Required | Description                          |
|-------|--------|----------|--------------------------------------|
| `tag` | string | No       | Query param. Return only products carrying this tag. |

**Response** — `200 OK`, array of product objects

| Field             | Type            | Description                          |
|-------------------|-----------------|--------------------------------------|
| `id`              | string          | Product ID.                          |
| `name`            | string          | Product name.                        |
| `description`     | string          | Product description.                 |
| `price_cents`     | integer         | Price in USD cents.                  |
| `sku`             | string          | Stock keeping unit.                  |
| `inventory_count` | integer         | Units in stock.                      |
| `tags`            | array of string | Tags applied to the product.         |
| `created_at`      | string          | ISO 8601 timestamp.                  |

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
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.datastack.io/products?tag=featured"
```

---

### POST /products

Create a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field             | Type            | Required | Description                            |
|-------------------|-----------------|----------|----------------------------------------|
| `name`            | string          | Yes      | Product name.                          |
| `description`     | string          | Yes      | Product description.                   |
| `price_cents`     | integer         | Yes      | Price in USD cents.                    |
| `sku`             | string          | Yes      | Stock keeping unit.                    |
| `inventory_count` | integer         | No       | Units in stock. Default `0`.           |
| `tags`            | array of string | No       | Tags. Default `[]`.                    |

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

Same fields as the product object in `GET /products`.

**Curl**

```bash
curl -X POST https://api.datastack.io/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### GET /products/{product_id}

Fetch a single product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request**

| Field        | Type   | Required | Description             |
|--------------|--------|----------|-------------------------|
| `product_id` | string | Yes      | Path param. Product ID. |

**Response** — `200 OK`

Same fields as the product object in `GET /products`.

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
curl -H "Authorization: Bearer $TOKEN" \
  https://api.datastack.io/products/prod_001
```

---

## Orders

The order object is returned by every endpoint in this section:

| Field              | Type                  | Description                                                                 |
|--------------------|-----------------------|-----------------------------------------------------------------------------|
| `id`               | string                | Order ID.                                                                   |
| `user_id`          | string                | User who placed the order.                                                  |
| `items`            | array of order item   | Line items — see below.                                                     |
| `shipping_address` | string                | Destination address.                                                        |
| `status`           | string                | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.         |
| `total_cents`      | integer               | Order total in USD cents (sum of `quantity` × `unit_price_cents`).          |
| `promo_code`       | string or null        | Promo code applied to the order.                                            |
| `tracking_number`  | string or null        | Carrier tracking number, `null` until shipped.                              |
| `created_at`       | string                | ISO 8601 timestamp.                                                         |
| `updated_at`       | string                | ISO 8601 timestamp.                                                         |

Order item fields:

| Field              | Type    | Required | Description                    |
|--------------------|---------|----------|--------------------------------|
| `product_id`       | string  | Yes      | Product being ordered.         |
| `quantity`         | integer | Yes      | Units ordered.                 |
| `unit_price_cents` | integer | Yes      | Price per unit in USD cents.   |

### POST /orders

Place a new order — inventory is reserved immediately, payment is captured asynchronously, and the order is returned in `pending` status.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field               | Type                | Required | Description                                          |
|---------------------|---------------------|----------|------------------------------------------------------|
| `user_id`           | string              | Yes      | User placing the order.                              |
| `items`             | array of order item | Yes      | Line items.                                          |
| `shipping_address`  | string              | Yes      | Destination address.                                 |
| `promo_code`        | string or null      | No       | Promo code to apply.                                 |
| `priority_shipping` | boolean             | No       | Request expedited shipping. Default `false`.         |
| `gift_message`      | string or null      | No       | Message to include with the shipment.                |

`priority_shipping` and `gift_message` are accepted on input but are not part of the order response.

```json
{
  "user_id": "usr_abc123",
  "items": [{ "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": "SPRING10",
  "priority_shipping": true,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`, an order object.

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [{ "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }],
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
curl -X POST https://api.datastack.io/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","priority_shipping":true,"gift_message":"Happy birthday!"}'
```

---

### GET /orders/{order_id}

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

| Field      | Type   | Required | Description           |
|------------|--------|----------|-----------------------|
| `order_id` | string | Yes      | Path param. Order ID. |

**Response** — `200 OK`, an order object.

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [{ "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }],
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
curl -H "Authorization: Bearer $TOKEN" \
  https://api.datastack.io/orders/ord_001
```

---

### PATCH /orders/{order_id}/status

Update the status of an order. Only admins can transition an order to `confirmed`, `shipped`, or `delivered`; users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>`

**Request**

| Field      | Type   | Required | Description                        |
|------------|--------|----------|------------------------------------|
| `order_id` | string | Yes      | Path param. Order to update.       |

Body:

| Field             | Type           | Required | Description                                                          |
|-------------------|----------------|----------|----------------------------------------------------------------------|
| `status`          | string         | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.  |
| `tracking_number` | string or null | No       | Carrier tracking number.                                             |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`, an order object.

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [{ "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }],
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
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning                            |
|------|------------------------------------|
| 400  | Bad request                        |
| 401  | Missing or invalid Bearer token    |
| 404  | Resource not found                 |
| 422  | Request body failed validation     |
| 500  | Internal server error              |
