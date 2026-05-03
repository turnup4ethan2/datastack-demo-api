# DataStack API Reference

> **Last updated: May 2026** — Auto-generated from `app/routes/`.

The DataStack API is a JSON HTTP API for user management, product catalog, and order processing.

## Authentication

All endpoints require a Bearer token passed in the `Authorization` header:

```
Authorization: Bearer <token>
```

> The legacy `?api_key=` query-parameter authentication has been deprecated and removed. All requests must now use the `Authorization` header.

---

## Users

### List Users

```
GET /users
```

Return all users in the given organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Query Parameters**

| Field             | Type   | Required | Description                                  |
|-------------------|--------|----------|----------------------------------------------|
| `organization_id` | string | Yes      | Organization whose users should be returned. |

**Response** — `200 OK`

| Field             | Type   | Description                                                  |
|-------------------|--------|--------------------------------------------------------------|
| `id`              | string | User ID, prefixed with `usr_`.                               |
| `email`           | string | Email address.                                               |
| `name`            | string | Display name.                                                |
| `role`            | string | One of `admin`, `member`, `viewer`.                          |
| `organization_id` | string | Organization the user belongs to.                            |
| `created_at`      | string | ISO 8601 timestamp.                                          |

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
curl https://api.datastack.io/users?organization_id=org_xyz \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create User

```
POST /users
```

Create a new user. Requires admin role on the organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field             | Type   | Required | Description                                                            |
|-------------------|--------|----------|------------------------------------------------------------------------|
| `email`           | string | Yes      | Email address. Must be a valid email.                                  |
| `name`            | string | Yes      | Display name.                                                          |
| `role`            | string | No       | One of `admin`, `member`, `viewer`. Defaults to `member`.              |
| `organization_id` | string | Yes      | Organization the new user will belong to.                              |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field             | Type   | Description                          |
|-------------------|--------|--------------------------------------|
| `id`              | string | User ID, prefixed with `usr_`.       |
| `email`           | string | Email address.                       |
| `name`            | string | Display name.                        |
| `role`            | string | One of `admin`, `member`, `viewer`.  |
| `organization_id` | string | Organization the user belongs to.    |
| `created_at`      | string | ISO 8601 timestamp.                  |

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

### Get User

```
GET /users/{user_id}
```

Fetch a single user by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `user_id` | string | Yes      | User ID.    |

**Response** — `200 OK`

| Field             | Type   | Description                          |
|-------------------|--------|--------------------------------------|
| `id`              | string | User ID.                             |
| `email`           | string | Email address.                       |
| `name`            | string | Display name.                        |
| `role`            | string | One of `admin`, `member`, `viewer`.  |
| `organization_id` | string | Organization the user belongs to.    |
| `created_at`      | string | ISO 8601 timestamp.                  |

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
curl https://api.datastack.io/users/usr_abc123 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently delete a user. Cannot delete your own account.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field     | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| `user_id` | string | Yes      | User ID to delete.    |

**Response** — `204 No Content`

No response body.

**Curl**

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

**Authentication**

```
Authorization: Bearer <token>
```

**Query Parameters**

| Field | Type   | Required | Description                                  |
|-------|--------|----------|----------------------------------------------|
| `tag` | string | No       | Return only products that have this tag.     |

**Response** — `200 OK`

| Field             | Type     | Description                                |
|-------------------|----------|--------------------------------------------|
| `id`              | string   | Product ID, prefixed with `prod_`.         |
| `name`            | string   | Product name.                              |
| `description`     | string   | Product description.                       |
| `price_cents`     | integer  | Price in USD cents.                        |
| `sku`             | string   | Stock-keeping unit.                        |
| `inventory_count` | integer  | Current inventory count.                   |
| `tags`            | string[] | Product tags.                              |
| `created_at`      | string   | ISO 8601 timestamp.                        |

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
curl "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create Product

```
POST /products
```

Create a new product in the catalog.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field             | Type     | Required | Description                                            |
|-------------------|----------|----------|--------------------------------------------------------|
| `name`            | string   | Yes      | Product name.                                          |
| `description`     | string   | Yes      | Product description.                                   |
| `price_cents`     | integer  | Yes      | Price in USD cents (e.g. `4999` = $49.99).             |
| `sku`             | string   | Yes      | Stock-keeping unit.                                    |
| `inventory_count` | integer  | No       | Initial inventory count. Defaults to `0`.              |
| `tags`            | string[] | No       | Product tags. Defaults to `[]`.                        |

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

| Field             | Type     | Description                          |
|-------------------|----------|--------------------------------------|
| `id`              | string   | Product ID, prefixed with `prod_`.   |
| `name`            | string   | Product name.                        |
| `description`     | string   | Product description.                 |
| `price_cents`     | integer  | Price in USD cents.                  |
| `sku`             | string   | Stock-keeping unit.                  |
| `inventory_count` | integer  | Current inventory count.             |
| `tags`            | string[] | Product tags.                        |
| `created_at`      | string   | ISO 8601 timestamp.                  |

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
curl -X POST https://api.datastack.io/products \
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

### Get Product

```
GET /products/{product_id}
```

Fetch a single product by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field        | Type   | Required | Description |
|--------------|--------|----------|-------------|
| `product_id` | string | Yes      | Product ID. |

**Response** — `200 OK`

| Field             | Type     | Description                          |
|-------------------|----------|--------------------------------------|
| `id`              | string   | Product ID.                          |
| `name`            | string   | Product name.                        |
| `description`     | string   | Product description.                 |
| `price_cents`     | integer  | Price in USD cents.                  |
| `sku`             | string   | Stock-keeping unit.                  |
| `inventory_count` | integer  | Current inventory count.             |
| `tags`            | string[] | Product tags.                        |
| `created_at`      | string   | ISO 8601 timestamp.                  |

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
curl https://api.datastack.io/products/prod_001 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

### Create Order

```
POST /orders
```

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. The order is returned in `pending` status.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field               | Type        | Required | Description                                                |
|---------------------|-------------|----------|------------------------------------------------------------|
| `user_id`           | string      | Yes      | User placing the order.                                    |
| `items`             | OrderItem[] | Yes      | Items in the order. Must contain at least one item.        |
| `shipping_address`  | string      | Yes      | Full shipping address.                                     |
| `promo_code`        | string      | No       | Promo code applied to the order.                           |
| `priority_shipping` | boolean     | No       | Whether to use priority shipping. Defaults to `false`.     |
| `gift_message`      | string      | No       | Optional gift message included with the order.             |

Each `OrderItem`:

| Field              | Type    | Required | Description                                      |
|--------------------|---------|----------|--------------------------------------------------|
| `product_id`       | string  | Yes      | ID of the product being ordered.                 |
| `quantity`         | integer | Yes      | Quantity ordered.                                |
| `unit_price_cents` | integer | Yes      | Per-unit price at order time, in USD cents.      |

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
  "promo_code": "SPRING10",
  "priority_shipping": true,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

| Field              | Type        | Description                                                       |
|--------------------|-------------|-------------------------------------------------------------------|
| `id`               | string      | Order ID, prefixed with `ord_`.                                   |
| `user_id`          | string      | User who placed the order.                                        |
| `items`            | OrderItem[] | Items in the order.                                               |
| `shipping_address` | string      | Full shipping address.                                            |
| `status`           | string      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. |
| `total_cents`      | integer     | Order total in USD cents.                                         |
| `promo_code`       | string\|null | Promo code applied to the order, if any.                         |
| `tracking_number`  | string\|null | Carrier tracking number, if available.                           |
| `created_at`       | string      | ISO 8601 timestamp.                                               |
| `updated_at`       | string      | ISO 8601 timestamp.                                               |

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
  "promo_code": "SPRING10",
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
  -d '{
    "user_id": "usr_abc123",
    "items": [
      {"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}
    ],
    "shipping_address": "123 Main St, San Francisco, CA 94105",
    "promo_code": "SPRING10",
    "priority_shipping": true,
    "gift_message": "Happy birthday!"
  }'
```

---

### Get Order

```
GET /orders/{order_id}
```

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field      | Type   | Required | Description |
|------------|--------|----------|-------------|
| `order_id` | string | Yes      | Order ID.   |

**Response** — `200 OK`

Same schema as the response from `POST /orders`.

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
curl https://api.datastack.io/orders/ord_001 \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`. Users may cancel their own `pending` orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field      | Type   | Required | Description |
|------------|--------|----------|-------------|
| `order_id` | string | Yes      | Order ID.   |

**Request Body**

| Field             | Type   | Required | Description                                                       |
|-------------------|--------|----------|-------------------------------------------------------------------|
| `status`          | string | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. |
| `tracking_number` | string | No       | Carrier tracking number.                                          |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Same schema as the response from `POST /orders`, with the updated `status` and `tracking_number`.

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
curl -X PATCH https://api.datastack.io/orders/ord_001/status \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped",
    "tracking_number": "1Z999AA10123456784"
  }'
```

---

## Error Codes

| Code | Meaning                                      |
|------|----------------------------------------------|
| 400  | Bad request                                  |
| 401  | Missing or invalid `Authorization` token     |
| 403  | Authenticated but not permitted               |
| 404  | Resource not found                           |
| 422  | Request body failed validation               |
| 500  | Internal server error                        |
