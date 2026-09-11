# DataStack API Reference

> **API version: 2.1.0** — This document is kept in sync with `app/routes/` automatically.

## Authentication

All endpoints (except `GET /health`) require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Requests without the header are rejected with `422 Unprocessable Entity` (missing required header).

---

## Health

### Health Check

```
GET /health
```

Returns the service status. No authentication required.

**Response** — `200 OK`

| Field  | Type   | Description  |
|--------|--------|--------------|
| status | string | Always `ok`. |

```json
{ "status": "ok" }
```

```bash
curl https://api.datastack.io/health
```

---

## Users

### User Object

| Field           | Type   | Description                                  |
|-----------------|--------|----------------------------------------------|
| id              | string | User ID (e.g. `usr_abc123`).                 |
| email           | string | Email address.                               |
| name            | string | Display name.                                |
| role            | string | One of `admin`, `member`, `viewer`.          |
| organization_id | string | ID of the organization the user belongs to.  |
| created_at      | string | ISO 8601 timestamp.                          |

---

### List Users

```
GET /users
```

Returns all users in the given organization.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Parameter       | Type   | Required | Description                        |
|-----------------|--------|----------|------------------------------------|
| organization_id | string | Yes      | Organization to list users for.    |

**Response** — `200 OK` — array of [User](#user-object) objects.

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

```bash
curl "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Create User

```
POST /users
```

Creates a new user. Requires admin role on the organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field           | Type   | Required | Description                                            |
|-----------------|--------|----------|--------------------------------------------------------|
| email           | string | Yes      | Must be a valid email address.                         |
| name            | string | Yes      | Display name.                                          |
| role            | string | No       | `admin`, `member`, or `viewer`. Defaults to `member`.  |
| organization_id | string | Yes      | Organization to create the user in.                    |

**Response** — `201 Created` — a [User](#user-object) object.

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

```bash
curl -X POST https://api.datastack.io/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"member","organization_id":"org_xyz"}'
```

---

### Get User

```
GET /users/{user_id}
```

Fetches a single user by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter | Type   | Required | Description  |
|-----------|--------|----------|--------------|
| user_id   | string | Yes      | The user ID. |

**Response** — `200 OK` — a [User](#user-object) object.

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

```bash
curl https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $TOKEN"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently deletes a user. You cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter | Type   | Required | Description  |
|-----------|--------|----------|--------------|
| user_id   | string | Yes      | The user ID. |

**Response** — `204 No Content` — empty body.

```bash
curl -X DELETE https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Products

### Product Object

| Field           | Type     | Description                          |
|-----------------|----------|--------------------------------------|
| id              | string   | Product ID (e.g. `prod_001`).        |
| name            | string   | Product name.                        |
| description     | string   | Product description.                 |
| price_cents     | integer  | Price in USD cents.                  |
| sku             | string   | Stock keeping unit.                  |
| inventory_count | integer  | Units in stock.                      |
| tags            | string[] | Tags for filtering.                  |
| created_at      | string   | ISO 8601 timestamp.                  |

---

### List Products

```
GET /products
```

Lists all products, optionally filtered by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| tag       | string | No       | Only return products with this tag.  |

**Response** — `200 OK` — array of [Product](#product-object) objects.

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

```bash
curl "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Create Product

```
POST /products
```

Creates a new product in the catalog.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field           | Type     | Required | Description                        |
|-----------------|----------|----------|------------------------------------|
| name            | string   | Yes      | Product name.                      |
| description     | string   | Yes      | Product description.               |
| price_cents     | integer  | Yes      | Price in USD cents.                |
| sku             | string   | Yes      | Stock keeping unit.                |
| inventory_count | integer  | No       | Units in stock. Defaults to `0`.   |
| tags            | string[] | No       | Tags. Defaults to `[]`.            |

**Response** — `201 Created` — a [Product](#product-object) object.

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

```bash
curl -X POST https://api.datastack.io/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### Get Product

```
GET /products/{product_id}
```

Fetches a single product by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter  | Type   | Required | Description     |
|------------|--------|----------|-----------------|
| product_id | string | Yes      | The product ID. |

**Response** — `200 OK` — a [Product](#product-object) object.

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

```bash
curl https://api.datastack.io/products/prod_001 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Orders

### Order Item Object

| Field            | Type    | Description                 |
|------------------|---------|-----------------------------|
| product_id       | string  | ID of the product ordered.  |
| quantity         | integer | Number of units.            |
| unit_price_cents | integer | Price per unit in USD cents.|

### Order Object

| Field            | Type                     | Description                                                                 |
|------------------|--------------------------|-----------------------------------------------------------------------------|
| id               | string                   | Order ID (e.g. `ord_001`).                                                  |
| user_id          | string                   | ID of the user who placed the order.                                        |
| items            | [OrderItem](#order-item-object)[] | Line items.                                                        |
| shipping_address | string                   | Shipping address.                                                           |
| status           | string                   | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.         |
| total_cents      | integer                  | Sum of `quantity * unit_price_cents` across items, in USD cents.            |
| promo_code       | string \| null           | Promo code applied, if any.                                                 |
| tracking_number  | string \| null           | Carrier tracking number, once shipped.                                      |
| created_at       | string                   | ISO 8601 timestamp.                                                         |
| updated_at       | string                   | ISO 8601 timestamp.                                                         |

---

### Create Order

```
POST /orders
```

Places a new order. Inventory is reserved immediately; payment is captured asynchronously. The order is returned in `pending` status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type                     | Required | Description                                    |
|-------------------|--------------------------|----------|------------------------------------------------|
| user_id           | string                   | Yes      | User placing the order.                        |
| items             | [OrderItem](#order-item-object)[] | Yes | Line items.                                  |
| shipping_address  | string                   | Yes      | Shipping address.                              |
| promo_code        | string                   | No       | Promo code. Defaults to `null`.                |
| priority_shipping | boolean                  | No       | Request priority shipping. Defaults to `false`.|
| gift_message      | string                   | No       | Gift message to include. Defaults to `null`.   |

> `priority_shipping` and `gift_message` are accepted on creation but are not returned in the Order object.

**Response** — `201 Created` — an [Order](#order-object) object.

```json
{
  "id": "ord_001",
  "user_id": "usr_abc123",
  "items": [{ "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "status": "pending",
  "total_cents": 9998,
  "promo_code": null,
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

```bash
curl -X POST https://api.datastack.io/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","priority_shipping":true,"gift_message":"Happy birthday!"}'
```

---

### Get Order

```
GET /orders/{order_id}
```

Fetches a single order by ID. Users can only fetch their own orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter | Type   | Required | Description   |
|-----------|--------|----------|---------------|
| order_id  | string | Yes      | The order ID. |

**Response** — `200 OK` — an [Order](#order-object) object.

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

```bash
curl https://api.datastack.io/orders/ord_001 \
  -H "Authorization: Bearer $TOKEN"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Updates the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`. Users may cancel their own `pending` orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter | Type   | Required | Description   |
|-----------|--------|----------|---------------|
| order_id  | string | Yes      | The order ID. |

**Request Body**

| Field           | Type   | Required | Description                                                          |
|-----------------|--------|----------|----------------------------------------------------------------------|
| status          | string | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.  |
| tracking_number | string | No       | Carrier tracking number. Defaults to `null`.                         |

**Response** — `200 OK` — the updated [Order](#order-object) object.

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

```bash
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning                                                        |
|------|----------------------------------------------------------------|
| 400  | Bad request                                                    |
| 401  | Invalid or expired bearer token                                |
| 404  | Resource not found                                             |
| 422  | Validation error (missing `Authorization` header, invalid body)|
| 500  | Internal server error                                          |
