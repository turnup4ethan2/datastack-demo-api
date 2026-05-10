# DataStack API Reference

> Maintained automatically. All endpoints below reflect the current implementation under `app/routes/`.

## Authentication

All endpoints require a Bearer token passed in the `Authorization` header.

```
Authorization: Bearer <token>
```

Requests missing or carrying an invalid token receive `401 Unauthorized`.

---

## Users

### List Users

```
GET /users
```

Returns all users in the given organization.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field             | Type   | Required | Description                              |
|-------------------|--------|----------|------------------------------------------|
| `organization_id` | string | Yes      | Organization to list users for.          |

**Response — `200 OK`**

| Field             | Type   | Description                                   |
|-------------------|--------|-----------------------------------------------|
| `id`              | string | Unique user ID.                               |
| `email`           | string | User email address.                           |
| `name`            | string | Display name.                                 |
| `role`            | string | One of `admin`, `member`, `viewer`.           |
| `organization_id` | string | Organization the user belongs to.             |
| `created_at`      | string | ISO 8601 UTC timestamp.                       |

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

### Create User

```
POST /users
```

Creates a new user. Requires admin role on the organization.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field             | Type   | Required | Description                                            |
|-------------------|--------|----------|--------------------------------------------------------|
| `email`           | string | Yes      | Valid email address.                                   |
| `name`            | string | Yes      | Display name.                                          |
| `role`            | string | No       | One of `admin`, `member`, `viewer`. Defaults to `member`. |
| `organization_id` | string | Yes      | Organization the user belongs to.                      |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response — `201 Created`**

| Field             | Type   | Description                                   |
|-------------------|--------|-----------------------------------------------|
| `id`              | string | Unique user ID.                               |
| `email`           | string | User email address.                           |
| `name`            | string | Display name.                                 |
| `role`            | string | One of `admin`, `member`, `viewer`.           |
| `organization_id` | string | Organization the user belongs to.             |
| `created_at`      | string | ISO 8601 UTC timestamp.                       |

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

### Get User

```
GET /users/{user_id}
```

Fetch a single user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type   | Required | Description     |
|-----------|--------|----------|-----------------|
| `user_id` | string | Yes      | The user ID.    |

**Response — `200 OK`**

| Field             | Type   | Description                                   |
|-------------------|--------|-----------------------------------------------|
| `id`              | string | Unique user ID.                               |
| `email`           | string | User email address.                           |
| `name`            | string | Display name.                                 |
| `role`            | string | One of `admin`, `member`, `viewer`.           |
| `organization_id` | string | Organization the user belongs to.             |
| `created_at`      | string | ISO 8601 UTC timestamp.                       |

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
  "https://api.datastack.io/users/usr_abc123"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently delete a user. Cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| `user_id` | string | Yes      | The user ID to delete. |

**Response — `204 No Content`**

Empty response body on success.

**Curl**

```bash
curl -X DELETE \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  "https://api.datastack.io/users/usr_abc123"
```

---

## Products

### List Products

```
GET /products
```

List all products. Optionally filter by tag.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field | Type   | Required | Description                                  |
|-------|--------|----------|----------------------------------------------|
| `tag` | string | No       | Return only products containing this tag.    |

**Response — `200 OK`**

| Field             | Type            | Description                                   |
|-------------------|-----------------|-----------------------------------------------|
| `id`              | string          | Unique product ID.                            |
| `name`            | string          | Product name.                                 |
| `description`     | string          | Long-form description.                        |
| `price_cents`     | integer         | Price in USD cents.                           |
| `sku`             | string          | Stock-keeping unit code.                      |
| `inventory_count` | integer         | Units currently in stock.                     |
| `tags`            | array of string | Tags associated with the product.             |
| `created_at`      | string          | ISO 8601 UTC timestamp.                       |

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

### Create Product

```
POST /products
```

Create a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field             | Type            | Required | Description                                              |
|-------------------|-----------------|----------|----------------------------------------------------------|
| `name`            | string          | Yes      | Product name.                                            |
| `description`     | string          | Yes      | Long-form description.                                   |
| `price_cents`     | integer         | Yes      | Price in USD cents.                                      |
| `sku`             | string          | Yes      | Stock-keeping unit code.                                 |
| `inventory_count` | integer         | No       | Units in stock. Defaults to `0`.                         |
| `tags`            | array of string | No       | Tags to associate with the product. Defaults to `[]`.    |

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

**Response — `201 Created`**

| Field             | Type            | Description                                   |
|-------------------|-----------------|-----------------------------------------------|
| `id`              | string          | Unique product ID.                            |
| `name`            | string          | Product name.                                 |
| `description`     | string          | Long-form description.                        |
| `price_cents`     | integer         | Price in USD cents.                           |
| `sku`             | string          | Stock-keeping unit code.                      |
| `inventory_count` | integer         | Units currently in stock.                     |
| `tags`            | array of string | Tags associated with the product.             |
| `created_at`      | string          | ISO 8601 UTC timestamp.                       |

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

### Get Product

```
GET /products/{product_id}
```

Fetch a single product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field        | Type   | Required | Description       |
|--------------|--------|----------|-------------------|
| `product_id` | string | Yes      | The product ID.   |

**Response — `200 OK`**

| Field             | Type            | Description                                   |
|-------------------|-----------------|-----------------------------------------------|
| `id`              | string          | Unique product ID.                            |
| `name`            | string          | Product name.                                 |
| `description`     | string          | Long-form description.                        |
| `price_cents`     | integer         | Price in USD cents.                           |
| `sku`             | string          | Stock-keeping unit code.                      |
| `inventory_count` | integer         | Units currently in stock.                     |
| `tags`            | array of string | Tags associated with the product.             |
| `created_at`      | string          | ISO 8601 UTC timestamp.                       |

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
  "https://api.datastack.io/products/prod_001"
```

---

## Orders

### Create Order

```
POST /orders
```

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. The order is returned in `pending` status.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field               | Type             | Required | Description                                                                 |
|---------------------|------------------|----------|-----------------------------------------------------------------------------|
| `user_id`           | string           | Yes      | ID of the user placing the order.                                           |
| `items`             | array of object  | Yes      | Order line items. See **OrderItem** below.                                  |
| `shipping_address`  | string           | Yes      | Destination shipping address.                                               |
| `promo_code`        | string           | No       | Optional promotional code.                                                  |
| `priority_shipping` | boolean          | No       | Use priority shipping. Defaults to `false`.                                 |
| `gift_message`      | string           | No       | Optional gift message included with the order.                              |

**OrderItem**

| Field              | Type    | Required | Description                       |
|--------------------|---------|----------|-----------------------------------|
| `product_id`       | string  | Yes      | Product being ordered.            |
| `quantity`         | integer | Yes      | Number of units.                  |
| `unit_price_cents` | integer | Yes      | Per-unit price in USD cents.      |

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

**Response — `201 Created`**

| Field              | Type            | Description                                                                                 |
|--------------------|-----------------|---------------------------------------------------------------------------------------------|
| `id`               | string          | Unique order ID.                                                                            |
| `user_id`          | string          | Owner of the order.                                                                         |
| `items`            | array of object | Line items (see **OrderItem**).                                                             |
| `shipping_address` | string          | Destination shipping address.                                                               |
| `status`           | string          | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.                         |
| `total_cents`      | integer         | Sum of `quantity * unit_price_cents` across items, in USD cents.                            |
| `promo_code`       | string \| null  | Promotional code applied, or `null`.                                                        |
| `tracking_number`  | string \| null  | Carrier tracking number, or `null` if not yet shipped.                                      |
| `created_at`       | string          | ISO 8601 UTC timestamp.                                                                     |
| `updated_at`       | string          | ISO 8601 UTC timestamp.                                                                     |

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
curl -X POST "https://api.datastack.io/orders" \
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

`Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type   | Required | Description     |
|------------|--------|----------|-----------------|
| `order_id` | string | Yes      | The order ID.   |

**Response — `200 OK`**

Same schema as the **Create Order** response.

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
curl -H "Authorization: Bearer $DATASTACK_TOKEN" \
  "https://api.datastack.io/orders/ord_001"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`. Users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type   | Required | Description     |
|------------|--------|----------|-----------------|
| `order_id` | string | Yes      | The order ID.   |

**Request Body**

| Field             | Type   | Required | Description                                                                  |
|-------------------|--------|----------|------------------------------------------------------------------------------|
| `status`          | string | Yes      | New status. One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. |
| `tracking_number` | string | No       | Carrier tracking number. Typically set when transitioning to `shipped`.      |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response — `200 OK`**

Same schema as the **Create Order** response.

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

| Code | Meaning                                  |
|------|------------------------------------------|
| 400  | Bad request (validation error).          |
| 401  | Missing or invalid `Authorization` header. |
| 403  | Authenticated but not allowed to perform the action. |
| 404  | Resource not found.                      |
| 500  | Internal server error.                   |
