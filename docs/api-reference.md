# DataStack API Reference

> **Last updated: March 2026** — Auto-generated from source code.

## Authentication

All API requests require a Bearer token passed via the `Authorization` header:

```
Authorization: Bearer <token>
```

---

## Users

### List Users

```
GET /users
```

Return all users in the given organization.

**Authentication**

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Query Parameters**

| Parameter         | Type     | Required | Description                          |
|-------------------|----------|----------|--------------------------------------|
| `organization_id` | `string` | Yes      | The organization to list users for   |

**Response** — `200 OK`

| Field             | Type     | Description                              |
|-------------------|----------|------------------------------------------|
| `id`              | `string` | Unique user identifier                   |
| `email`           | `string` | User email address                       |
| `name`            | `string` | User display name                        |
| `role`            | `string` | User role (`admin`, `member`, `viewer`)  |
| `organization_id` | `string` | Organization the user belongs to         |
| `created_at`      | `string` | ISO 8601 creation timestamp              |

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

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer <token>"
```

---

### Create User

```
POST /users
```

Create a new user. Requires admin role on the organization.

**Authentication**

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Request Body**

| Field             | Type     | Required | Description                                                    |
|-------------------|----------|----------|----------------------------------------------------------------|
| `email`           | `string` | Yes      | Valid email address                                            |
| `name`            | `string` | Yes      | User display name                                              |
| `role`            | `string` | No       | User role — `admin`, `member`, or `viewer` (default: `member`) |
| `organization_id` | `string` | Yes      | Organization to add the user to                                |

```json
{
  "email": "bob@datastack.io",
  "name": "Bob",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field             | Type     | Description                      |
|-------------------|----------|----------------------------------|
| `id`              | `string` | Unique user identifier           |
| `email`           | `string` | User email address               |
| `name`            | `string` | User display name                |
| `role`            | `string` | User role                        |
| `organization_id` | `string` | Organization the user belongs to |
| `created_at`      | `string` | ISO 8601 creation timestamp      |

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

**Curl Example**

```bash
curl -X POST "https://api.datastack.io/users" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "bob@datastack.io",
    "name": "Bob",
    "role": "member",
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

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Path Parameters**

| Parameter | Type     | Required | Description            |
|-----------|----------|----------|------------------------|
| `user_id` | `string` | Yes      | Unique user identifier |

**Response** — `200 OK`

| Field             | Type     | Description                      |
|-------------------|----------|----------------------------------|
| `id`              | `string` | Unique user identifier           |
| `email`           | `string` | User email address               |
| `name`            | `string` | User display name                |
| `role`            | `string` | User role                        |
| `organization_id` | `string` | Organization the user belongs to |
| `created_at`      | `string` | ISO 8601 creation timestamp      |

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

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently delete a user. Cannot delete your own account.

**Authentication**

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Path Parameters**

| Parameter | Type     | Required | Description            |
|-----------|----------|----------|------------------------|
| `user_id` | `string` | Yes      | Unique user identifier |

**Response** — `204 No Content`

No response body.

**Curl Example**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

## Products

### List Products

```
GET /products
```

List all products in the catalog. Optionally filter by tag.

**Authentication**

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Query Parameters**

| Parameter | Type     | Required | Description            |
|-----------|----------|----------|------------------------|
| `tag`     | `string` | No       | Filter products by tag |

**Response** — `200 OK`

| Field             | Type       | Description                 |
|-------------------|------------|-----------------------------|
| `id`              | `string`   | Unique product identifier   |
| `name`            | `string`   | Product name                |
| `description`     | `string`   | Product description         |
| `price_cents`     | `integer`  | Price in USD cents          |
| `sku`             | `string`   | Stock keeping unit          |
| `inventory_count` | `integer`  | Current inventory quantity  |
| `tags`            | `string[]` | List of tags                |
| `created_at`      | `string`   | ISO 8601 creation timestamp |

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

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/products?tag=hardware" \
  -H "Authorization: Bearer <token>"
```

---

### Create Product

```
POST /products
```

Create a new product in the catalog.

**Authentication**

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Request Body**

| Field             | Type       | Required | Description                               |
|-------------------|------------|----------|-------------------------------------------|
| `name`            | `string`   | Yes      | Product name                              |
| `description`     | `string`   | Yes      | Product description                       |
| `price_cents`     | `integer`  | Yes      | Price in USD cents                        |
| `sku`             | `string`   | Yes      | Stock keeping unit                        |
| `inventory_count` | `integer`  | No       | Initial inventory quantity (default: `0`) |
| `tags`            | `string[]` | No       | List of tags (default: `[]`)              |

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

| Field             | Type       | Description                 |
|-------------------|------------|-----------------------------|
| `id`              | `string`   | Unique product identifier   |
| `name`            | `string`   | Product name                |
| `description`     | `string`   | Product description         |
| `price_cents`     | `integer`  | Price in USD cents          |
| `sku`             | `string`   | Stock keeping unit          |
| `inventory_count` | `integer`  | Current inventory quantity  |
| `tags`            | `string[]` | List of tags                |
| `created_at`      | `string`   | ISO 8601 creation timestamp |

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

**Curl Example**

```bash
curl -X POST "https://api.datastack.io/products" \
  -H "Authorization: Bearer <token>" \
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

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Path Parameters**

| Parameter    | Type     | Required | Description               |
|--------------|----------|----------|---------------------------|
| `product_id` | `string` | Yes      | Unique product identifier |

**Response** — `200 OK`

| Field             | Type       | Description                 |
|-------------------|------------|-----------------------------|
| `id`              | `string`   | Unique product identifier   |
| `name`            | `string`   | Product name                |
| `description`     | `string`   | Product description         |
| `price_cents`     | `integer`  | Price in USD cents          |
| `sku`             | `string`   | Stock keeping unit          |
| `inventory_count` | `integer`  | Current inventory quantity  |
| `tags`            | `string[]` | List of tags                |
| `created_at`      | `string`   | ISO 8601 creation timestamp |

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

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/products/prod_001" \
  -H "Authorization: Bearer <token>"
```

---

## Orders

### Create Order

```
POST /orders
```

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. Returns the order in `pending` status.

**Authentication**

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Request Body**

| Field               | Type          | Required | Description                                 |
|---------------------|---------------|----------|---------------------------------------------|
| `user_id`           | `string`      | Yes      | ID of the user placing the order            |
| `items`             | `OrderItem[]` | Yes      | List of items to order (see below)          |
| `shipping_address`  | `string`      | Yes      | Full shipping address                       |
| `promo_code`        | `string`      | No       | Promotional code to apply                   |
| `priority_shipping` | `boolean`     | No       | Enable priority shipping (default: `false`) |

**OrderItem**

| Field              | Type      | Required | Description                 |
|--------------------|-----------|----------|-----------------------------|
| `product_id`       | `string`  | Yes      | Product identifier          |
| `quantity`         | `integer` | Yes      | Number of units             |
| `unit_price_cents` | `integer` | Yes      | Price per unit in USD cents |

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
  "promo_code": "SAVE10",
  "priority_shipping": false
}
```

**Response** — `201 Created`

| Field              | Type            | Description                                                                |
|--------------------|-----------------|----------------------------------------------------------------------------|
| `id`               | `string`        | Unique order identifier                                                    |
| `user_id`          | `string`        | ID of the user who placed the order                                        |
| `items`            | `OrderItem[]`   | List of order items                                                        |
| `shipping_address` | `string`        | Shipping address                                                           |
| `status`           | `string`        | Order status (`pending`, `confirmed`, `shipped`, `delivered`, `cancelled`) |
| `total_cents`      | `integer`       | Order total in USD cents                                                   |
| `promo_code`       | `string\|null`  | Applied promo code, or `null`                                              |
| `tracking_number`  | `string\|null`  | Shipping tracking number, or `null`                                        |
| `created_at`       | `string`        | ISO 8601 creation timestamp                                                |
| `updated_at`       | `string`        | ISO 8601 last-updated timestamp                                            |

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
  "promo_code": "SAVE10",
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl Example**

```bash
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usr_abc123",
    "items": [
      {
        "product_id": "prod_001",
        "quantity": 2,
        "unit_price_cents": 4999
      }
    ],
    "shipping_address": "123 Main St, San Francisco, CA 94105",
    "promo_code": "SAVE10",
    "priority_shipping": false
  }'
```

---

### Get Order

```
GET /orders/{order_id}
```

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Path Parameters**

| Parameter  | Type     | Required | Description             |
|------------|----------|----------|-------------------------|
| `order_id` | `string` | Yes      | Unique order identifier |

**Response** — `200 OK`

| Field              | Type            | Description                         |
|--------------------|-----------------|-------------------------------------|
| `id`               | `string`        | Unique order identifier             |
| `user_id`          | `string`        | ID of the user who placed the order |
| `items`            | `OrderItem[]`   | List of order items                 |
| `shipping_address` | `string`        | Shipping address                    |
| `status`           | `string`        | Order status                        |
| `total_cents`      | `integer`       | Order total in USD cents            |
| `promo_code`       | `string\|null`  | Applied promo code, or `null`       |
| `tracking_number`  | `string\|null`  | Shipping tracking number, or `null` |
| `created_at`       | `string`        | ISO 8601 creation timestamp         |
| `updated_at`       | `string`        | ISO 8601 last-updated timestamp     |

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

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer <token>"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`. Users may cancel their own `pending` orders.

**Authentication**

| Header          | Format          | Required |
|-----------------|-----------------|----------|
| `Authorization` | `Bearer <token>` | Yes      |

**Path Parameters**

| Parameter  | Type     | Required | Description             |
|------------|----------|----------|-------------------------|
| `order_id` | `string` | Yes      | Unique order identifier |

**Request Body**

| Field             | Type     | Required | Description                                                                 |
|-------------------|----------|----------|-----------------------------------------------------------------------------|
| `status`          | `string` | Yes      | New status — `pending`, `confirmed`, `shipped`, `delivered`, or `cancelled` |
| `tracking_number` | `string` | No       | Shipping tracking number                                                    |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

| Field              | Type            | Description                         |
|--------------------|-----------------|-------------------------------------|
| `id`               | `string`        | Unique order identifier             |
| `user_id`          | `string`        | ID of the user who placed the order |
| `items`            | `OrderItem[]`   | List of order items                 |
| `shipping_address` | `string`        | Shipping address                    |
| `status`           | `string`        | Updated order status                |
| `total_cents`      | `integer`       | Order total in USD cents            |
| `promo_code`       | `string\|null`  | Applied promo code, or `null`       |
| `tracking_number`  | `string\|null`  | Shipping tracking number, or `null` |
| `created_at`       | `string`        | ISO 8601 creation timestamp         |
| `updated_at`       | `string`        | ISO 8601 last-updated timestamp     |

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

**Curl Example**

```bash
curl -X PATCH "https://api.datastack.io/orders/ord_001/status" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped",
    "tracking_number": "1Z999AA10123456784"
  }'
```

---

## Health

### Health Check

```
GET /health
```

Returns the current health status of the API. No authentication required.

**Response** — `200 OK`

```json
{
  "status": "ok"
}
```

**Curl Example**

```bash
curl -X GET "https://api.datastack.io/health"
```

---

## Error Codes

| Code | Meaning               |
|------|-----------------------|
| 400  | Bad request           |
| 401  | Unauthorized          |
| 404  | Resource not found    |
| 500  | Internal server error |
