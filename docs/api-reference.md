# DataStack API Reference

> API version `2.1.0`. This document is kept in sync with `app/routes/` automatically.

## Authentication

All endpoints except `GET /health` require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Query-parameter API keys (`?api_key=...`) are deprecated and no longer supported.

---

## Health

### Health Check

```
GET /health
```

Liveness probe. Requires no authentication.

**Response** — `200 OK`

| Field  | Type   | Description               |
|--------|--------|---------------------------|
| status | string | Always `ok` when healthy. |

```json
{ "status": "ok" }
```

```bash
curl https://api.datastack.io/health
```

---

## Users

### List Users

```
GET /users
```

Return all users in the given organization.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field           | Type   | Required | Description                       |
|-----------------|--------|----------|-----------------------------------|
| organization_id | string | Yes      | Organization to list users for.   |

**Response** — `200 OK`, array of user objects.

| Field           | Type   | Description                              |
|-----------------|--------|------------------------------------------|
| id              | string | User ID.                                 |
| email           | string | User email address.                      |
| name            | string | Display name.                            |
| role            | string | One of `admin`, `member`, `viewer`.      |
| organization_id | string | Organization the user belongs to.        |
| created_at      | string | ISO 8601 UTC timestamp.                  |

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
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create User

```
POST /users
```

Create a new user. Requires admin role on the organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field           | Type   | Required | Description                                          |
|-----------------|--------|----------|------------------------------------------------------|
| email           | string | Yes      | Valid email address.                                 |
| name            | string | Yes      | Display name.                                        |
| role            | string | No       | `admin`, `member`, or `viewer`. Defaults to `member`.|
| organization_id | string | Yes      | Organization to create the user in.                  |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`, a user object (fields as in [List Users](#list-users)).

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

```bash
curl -X POST https://api.datastack.io/users \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@datastack.io","name":"Alice","role":"admin","organization_id":"org_xyz"}'
```

---

### Get User

```
GET /users/{user_id}
```

Fetch a single user by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field   | Type   | Required | Description |
|---------|--------|----------|-------------|
| user_id | string | Yes      | User ID.    |

**Response** — `200 OK`, a user object (fields as in [List Users](#list-users)).

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
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently delete a user. You cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field   | Type   | Required | Description         |
|---------|--------|----------|---------------------|
| user_id | string | Yes      | User ID to delete.  |

**Response** — `204 No Content`, empty body.

```bash
curl -X DELETE https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### List Products

```
GET /products
```

List all products. Optionally filter by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Field | Type   | Required | Description                |
|-------|--------|----------|----------------------------|
| tag   | string | No       | Only return products with this tag. |

**Response** — `200 OK`, array of product objects.

| Field           | Type            | Description                               |
|-----------------|-----------------|-------------------------------------------|
| id              | string          | Product ID.                               |
| name            | string          | Product name.                             |
| description     | string          | Product description.                      |
| price_cents     | integer         | Price in USD cents (e.g. `4999` = $49.99).|
| sku             | string          | Stock keeping unit.                       |
| inventory_count | integer         | Units currently in stock.                 |
| tags            | array of string | Product tags.                             |
| created_at      | string          | ISO 8601 UTC timestamp.                   |

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
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create Product

```
POST /products
```

Create a new product in the catalog.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field           | Type            | Required | Description                                |
|-----------------|-----------------|----------|--------------------------------------------|
| name            | string          | Yes      | Product name.                              |
| description     | string          | Yes      | Product description.                       |
| price_cents     | integer         | Yes      | Price in USD cents.                        |
| sku             | string          | Yes      | Stock keeping unit.                        |
| inventory_count | integer         | No       | Initial stock. Defaults to `0`.            |
| tags            | array of string | No       | Product tags. Defaults to `[]`.            |

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

**Response** — `201 Created`, a product object (fields as in [List Products](#list-products)).

```bash
curl -X POST https://api.datastack.io/products \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### Get Product

```
GET /products/{product_id}
```

Fetch a single product by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type   | Required | Description  |
|------------|--------|----------|--------------|
| product_id | string | Yes      | Product ID.  |

**Response** — `200 OK`, a product object (fields as in [List Products](#list-products)).

```bash
curl https://api.datastack.io/products/prod_001 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

An order item (`items[]`) has the following shape:

| Field            | Type    | Required | Description                     |
|------------------|---------|----------|---------------------------------|
| product_id       | string  | Yes      | Product being ordered.          |
| quantity         | integer | Yes      | Number of units.                |
| unit_price_cents | integer | Yes      | Per-unit price in USD cents.    |

Order `status` is one of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.

The order object returned by all order endpoints:

| Field            | Type              | Description                                |
|------------------|-------------------|--------------------------------------------|
| id               | string            | Order ID.                                  |
| user_id          | string            | User who placed the order.                 |
| items            | array of item     | Ordered items.                             |
| shipping_address | string            | Destination address.                       |
| status           | string            | Current order status.                      |
| total_cents      | integer           | Order total in USD cents.                  |
| promo_code       | string \| null    | Applied promo code, if any.                |
| tracking_number  | string \| null    | Carrier tracking number, if assigned.      |
| created_at       | string            | ISO 8601 UTC timestamp.                    |
| updated_at       | string            | ISO 8601 UTC timestamp.                    |

### Create Order

```
POST /orders
```

Place a new order. Inventory is reserved immediately and payment is captured asynchronously; the order is returned in `pending` status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type          | Required | Description                                  |
|-------------------|---------------|----------|----------------------------------------------|
| user_id           | string        | Yes      | User placing the order.                      |
| items             | array of item | Yes      | Items to order.                              |
| shipping_address  | string        | Yes      | Destination address.                         |
| promo_code        | string        | No       | Promo code to apply.                         |
| priority_shipping | boolean       | No       | Request priority shipping. Defaults to `false`. |
| gift_message      | string        | No       | Message to include with the shipment.        |

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

```bash
curl -X POST https://api.datastack.io/orders \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","promo_code":"SPRING10","priority_shipping":true,"gift_message":"Happy birthday!"}'
```

---

### Get Order

```
GET /orders/{order_id}
```

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field    | Type   | Required | Description |
|----------|--------|----------|-------------|
| order_id | string | Yes      | Order ID.   |

**Response** — `200 OK`, an order object.

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

```bash
curl https://api.datastack.io/orders/ord_001 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`; users may cancel their own `pending` orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Field    | Type   | Required | Description |
|----------|--------|----------|-------------|
| order_id | string | Yes      | Order ID.   |

**Request Body**

| Field           | Type   | Required | Description                                                                 |
|-----------------|--------|----------|-----------------------------------------------------------------------------|
| status          | string | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.          |
| tracking_number | string | No       | Carrier tracking number to attach to the order.                              |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`, the updated order object.

```bash
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning               |
|------|-----------------------|
| 400  | Bad request           |
| 401  | Missing or invalid Bearer token |
| 403  | Not permitted for this role |
| 404  | Resource not found    |
| 422  | Request body validation failed |
| 500  | Internal server error |
