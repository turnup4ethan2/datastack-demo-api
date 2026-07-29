# DataStack API Reference

API version `2.1.0`. Base URL: `https://api.datastack.io`.

## Authentication

All endpoints require a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

The old `api_key` query parameter is deprecated and no longer accepted.

---

## Health

### Health check

```
GET /health
```

Returns service liveness. No authentication required.

**Response** — `200 OK`

| Field    | Type     | Description             |
|----------|----------|-------------------------|
| `status` | `string` | Always `ok` when healthy |

```json
{
  "status": "ok"
}
```

**Curl**

```bash
curl https://api.datastack.io/health
```

---

## Users

### List users

```
GET /users
```

Return all users in the given organization.

**Authentication** — `Authorization: Bearer <token>`

**Query parameters**

| Field             | Type     | Required | Description                        |
|-------------------|----------|----------|------------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users to return |

**Response** — `200 OK`, array of user objects.

| Field             | Type     | Description                                     |
|-------------------|----------|-------------------------------------------------|
| `id`              | `string` | User ID                                          |
| `email`           | `string` | Email address                                    |
| `name`            | `string` | Display name                                     |
| `role`            | `string` | One of `admin`, `member`, `viewer`               |
| `organization_id` | `string` | Organization the user belongs to                 |
| `created_at`      | `string` | ISO 8601 UTC timestamp                           |

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
curl -H "Authorization: Bearer $DATASTACK_TOKEN" \
  "https://api.datastack.io/users?organization_id=org_xyz"
```

---

### Create user

```
POST /users
```

Create a new user. Requires admin role on the organization.

**Authentication** — `Authorization: Bearer <token>`

**Request body**

| Field             | Type     | Required | Description                                               |
|-------------------|----------|----------|-----------------------------------------------------------|
| `email`           | `string` | Yes      | Valid email address                                        |
| `name`            | `string` | Yes      | Display name                                               |
| `role`            | `string` | No       | `admin`, `member`, or `viewer`. Defaults to `member`       |
| `organization_id` | `string` | Yes      | Organization to create the user in                         |

```json
{
  "email": "bob@datastack.io",
  "name": "Bob",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`, a user object (same fields as [List users](#list-users)).

```json
{
  "id": "usr_abc123",
  "email": "bob@datastack.io",
  "name": "Bob",
  "role": "member",
  "organization_id": "org_xyz",
  "created_at": "2026-03-20T00:00:00Z"
}
```

**Curl**

```bash
curl -X POST https://api.datastack.io/users \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"bob@datastack.io","name":"Bob","role":"member","organization_id":"org_xyz"}'
```

---

### Get user

```
GET /users/{user_id}
```

Fetch a single user by ID.

**Authentication** — `Authorization: Bearer <token>`

**Path parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID     |

**Response** — `200 OK`, a user object (same fields as [List users](#list-users)).

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
curl -H "Authorization: Bearer $DATASTACK_TOKEN" \
  https://api.datastack.io/users/usr_abc123
```

---

### Delete user

```
DELETE /users/{user_id}
```

Permanently delete a user. You cannot delete your own account.

**Authentication** — `Authorization: Bearer <token>`

**Path parameters**

| Field     | Type     | Required | Description |
|-----------|----------|----------|-------------|
| `user_id` | `string` | Yes      | User ID     |

**Response** — `204 No Content`, empty body.

**Curl**

```bash
curl -X DELETE https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### List products

```
GET /products
```

List all products. Optionally filter by tag.

**Authentication** — `Authorization: Bearer <token>`

**Query parameters**

| Field | Type     | Required | Description                  |
|-------|----------|----------|------------------------------|
| `tag` | `string` | No       | Only return products with this tag |

**Response** — `200 OK`, array of product objects.

| Field             | Type            | Description                          |
|-------------------|-----------------|--------------------------------------|
| `id`              | `string`        | Product ID                            |
| `name`            | `string`        | Product name                          |
| `description`     | `string`        | Product description                   |
| `price_cents`     | `integer`       | Price in USD cents                    |
| `sku`             | `string`        | Stock keeping unit                    |
| `inventory_count` | `integer`       | Units currently in stock              |
| `tags`            | `array[string]` | Tags applied to the product           |
| `created_at`      | `string`        | ISO 8601 UTC timestamp                |

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
curl -H "Authorization: Bearer $DATASTACK_TOKEN" \
  "https://api.datastack.io/products?tag=featured"
```

---

### Create product

```
POST /products
```

Create a new product in the catalog.

**Authentication** — `Authorization: Bearer <token>`

**Request body**

| Field             | Type            | Required | Description                              |
|-------------------|-----------------|----------|------------------------------------------|
| `name`            | `string`        | Yes      | Product name                              |
| `description`     | `string`        | Yes      | Product description                       |
| `price_cents`     | `integer`       | Yes      | Price in USD cents                        |
| `sku`             | `string`        | Yes      | Stock keeping unit                        |
| `inventory_count` | `integer`       | No       | Units in stock. Defaults to `0`           |
| `tags`            | `array[string]` | No       | Tags. Defaults to `[]`                    |

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

**Response** — `201 Created`, a product object (same fields as [List products](#list-products)).

**Curl**

```bash
curl -X POST https://api.datastack.io/products \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget Pro","description":"Our best-selling widget.","price_cents":4999,"sku":"WGT-PRO-001","inventory_count":142,"tags":["hardware","featured"]}'
```

---

### Get product

```
GET /products/{product_id}
```

Fetch a single product by ID.

**Authentication** — `Authorization: Bearer <token>`

**Path parameters**

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `product_id` | `string` | Yes      | Product ID  |

**Response** — `200 OK`, a product object (same fields as [List products](#list-products)).

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
curl -H "Authorization: Bearer $DATASTACK_TOKEN" \
  https://api.datastack.io/products/prod_001
```

---

## Orders

An order item (`items[]`) has the following shape:

| Field              | Type      | Required | Description                  |
|--------------------|-----------|----------|------------------------------|
| `product_id`       | `string`  | Yes      | Product being ordered         |
| `quantity`         | `integer` | Yes      | Number of units               |
| `unit_price_cents` | `integer` | Yes      | Per-unit price in USD cents   |

### Create order

```
POST /orders
```

Place a new order. Inventory is reserved immediately and payment is captured asynchronously, so the order is returned in `pending` status.

**Authentication** — `Authorization: Bearer <token>`

**Request body**

| Field               | Type                 | Required | Description                                       |
|---------------------|----------------------|----------|---------------------------------------------------|
| `user_id`           | `string`             | Yes      | User placing the order                             |
| `items`             | `array[OrderItem]`   | Yes      | Line items                                         |
| `shipping_address`  | `string`             | Yes      | Full shipping address                              |
| `promo_code`        | `string` or `null`   | No       | Promotional code. Defaults to `null`               |
| `priority_shipping` | `boolean`            | No       | Request expedited shipping. Defaults to `false`    |
| `gift_message`      | `string` or `null`   | No       | Message included with the shipment. Defaults to `null` |

```json
{
  "user_id": "usr_abc123",
  "items": [
    {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": null,
  "priority_shipping": false,
  "gift_message": null
}
```

**Response** — `201 Created`

| Field              | Type                | Description                                                                |
|--------------------|---------------------|----------------------------------------------------------------------------|
| `id`               | `string`            | Order ID                                                                    |
| `user_id`          | `string`            | User who placed the order                                                   |
| `items`            | `array[OrderItem]`  | Line items                                                                  |
| `shipping_address` | `string`            | Shipping address                                                            |
| `status`           | `string`            | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`          |
| `total_cents`      | `integer`           | Sum of `quantity * unit_price_cents` across items, in USD cents             |
| `promo_code`       | `string` or `null`  | Promo code applied                                                          |
| `tracking_number`  | `string` or `null`  | Carrier tracking number, `null` until shipped                               |
| `created_at`       | `string`            | ISO 8601 UTC timestamp                                                      |
| `updated_at`       | `string`            | ISO 8601 UTC timestamp                                                      |

`priority_shipping` and `gift_message` are accepted on create but are not returned in the order object.

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
  "promo_code": null,
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl**

```bash
curl -X POST https://api.datastack.io/orders \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"usr_abc123","items":[{"product_id":"prod_001","quantity":2,"unit_price_cents":4999}],"shipping_address":"123 Main St, San Francisco, CA 94105","priority_shipping":false}'
```

---

### Get order

```
GET /orders/{order_id}
```

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication** — `Authorization: Bearer <token>`

**Path parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

**Response** — `200 OK`, an order object (same fields as [Create order](#create-order)).

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

**Curl**

```bash
curl -H "Authorization: Bearer $DATASTACK_TOKEN" \
  https://api.datastack.io/orders/ord_001
```

---

### Update order status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition an order to `confirmed`, `shipped`, or `delivered`; users may cancel their own `pending` orders.

**Authentication** — `Authorization: Bearer <token>`

**Path parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID    |

**Request body**

| Field             | Type               | Required | Description                                                        |
|-------------------|--------------------|----------|--------------------------------------------------------------------|
| `status`          | `string`           | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`  |
| `tracking_number` | `string` or `null` | No       | Carrier tracking number. Defaults to `null`                         |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`, the updated order object (same fields as [Create order](#create-order)).

**Curl**

```bash
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped","tracking_number":"1Z999AA10123456784"}'
```

---

## Error Codes

| Code | Meaning                                   |
|------|-------------------------------------------|
| 400  | Bad request                               |
| 401  | Missing or invalid bearer token           |
| 403  | Authenticated but not permitted           |
| 404  | Resource not found                        |
| 422  | Request body failed validation            |
| 500  | Internal server error                     |
