# DataStack API Reference

> Reference documentation for the DataStack core API (`v2.1.0`) — user management,
> product catalog, and order processing.

## Authentication

All endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Requests without a valid token receive `401 Unauthorized`.

---

## Users

### List users

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
| `organization_id` | string | Yes      | The organization whose users to return.      |

**Response** — `200 OK`

| Field             | Type   | Description                                  |
|-------------------|--------|----------------------------------------------|
| `id`              | string | User ID.                                     |
| `email`           | string | User email address.                          |
| `name`            | string | User display name.                           |
| `role`            | string | One of `admin`, `member`, `viewer`.          |
| `organization_id` | string | Owning organization ID.                      |
| `created_at`      | string | ISO 8601 timestamp.                          |

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

**Curl example**

```bash
curl -X GET "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create user

```
POST /users
```

Create a new user. Requires admin role on the organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field             | Type   | Required | Description                                            |
|-------------------|--------|----------|--------------------------------------------------------|
| `email`           | string | Yes      | User email address (must be a valid email).            |
| `name`            | string | Yes      | User display name.                                     |
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

**Response** — `201 Created`

| Field             | Type   | Description                                  |
|-------------------|--------|----------------------------------------------|
| `id`              | string | New user ID.                                 |
| `email`           | string | User email address.                          |
| `name`            | string | User display name.                           |
| `role`            | string | One of `admin`, `member`, `viewer`.          |
| `organization_id` | string | Owning organization ID.                      |
| `created_at`      | string | ISO 8601 timestamp.                          |

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

**Curl example**

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

### Get user

```
GET /users/{user_id}
```

Fetch a single user by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field     | Type   | Required | Description       |
|-----------|--------|----------|-------------------|
| `user_id` | string | Yes      | The user's ID.    |

**Response** — `200 OK`

| Field             | Type   | Description                                  |
|-------------------|--------|----------------------------------------------|
| `id`              | string | User ID.                                     |
| `email`           | string | User email address.                          |
| `name`            | string | User display name.                           |
| `role`            | string | One of `admin`, `member`, `viewer`.          |
| `organization_id` | string | Owning organization ID.                      |
| `created_at`      | string | ISO 8601 timestamp.                          |

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

**Curl example**

```bash
curl -X GET "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Delete user

```
DELETE /users/{user_id}
```

Permanently delete a user. You cannot delete your own account.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field     | Type   | Required | Description       |
|-----------|--------|----------|-------------------|
| `user_id` | string | Yes      | The user's ID.    |

**Response** — `204 No Content`

Empty body.

**Curl example**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### List products

```
GET /products
```

List all products in the catalog. Optionally filter by tag.

**Authentication**

```
Authorization: Bearer <token>
```

**Query Parameters**

| Field | Type   | Required | Description                          |
|-------|--------|----------|--------------------------------------|
| `tag` | string | No       | Only return products with this tag.  |

**Response** — `200 OK`

| Field             | Type            | Description                                            |
|-------------------|-----------------|--------------------------------------------------------|
| `id`              | string          | Product ID.                                            |
| `name`            | string          | Product name.                                          |
| `description`    | string          | Product description.                                   |
| `price_cents`     | integer         | Price in USD cents (e.g. `4999` = $49.99).             |
| `sku`             | string          | Stock-keeping unit identifier.                         |
| `inventory_count` | integer         | Number of units currently in stock.                    |
| `tags`            | array of string | Tags associated with the product.                      |
| `created_at`      | string          | ISO 8601 timestamp.                                    |

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

**Curl example**

```bash
curl -X GET "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Create product

```
POST /products
```

Create a new product in the catalog.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field             | Type            | Required | Description                                       |
|-------------------|-----------------|----------|---------------------------------------------------|
| `name`            | string          | Yes      | Product name.                                     |
| `description`    | string          | Yes      | Product description.                              |
| `price_cents`     | integer         | Yes      | Price in USD cents.                               |
| `sku`             | string          | Yes      | Stock-keeping unit identifier.                    |
| `inventory_count` | integer         | No       | Initial inventory. Defaults to `0`.               |
| `tags`            | array of string | No       | Tags for the product. Defaults to `[]`.           |

```json
{
  "name": "Widget Pro",
  "description": "Our best-selling widget.",
  "price_cents": 4999,
  "sku": "WGT-PRO-001",
  "inventory_count": 100,
  "tags": ["hardware", "featured"]
}
```

**Response** — `201 Created`

| Field             | Type            | Description                                            |
|-------------------|-----------------|--------------------------------------------------------|
| `id`              | string          | Product ID.                                            |
| `name`            | string          | Product name.                                          |
| `description`    | string          | Product description.                                   |
| `price_cents`     | integer         | Price in USD cents.                                    |
| `sku`             | string          | Stock-keeping unit identifier.                         |
| `inventory_count` | integer         | Current inventory count.                               |
| `tags`            | array of string | Product tags.                                          |
| `created_at`      | string          | ISO 8601 timestamp.                                    |

```json
{
  "id": "prod_001",
  "name": "Widget Pro",
  "description": "Our best-selling widget.",
  "price_cents": 4999,
  "sku": "WGT-PRO-001",
  "inventory_count": 100,
  "tags": ["hardware", "featured"],
  "created_at": "2026-03-20T00:00:00Z"
}
```

**Curl example**

```bash
curl -X POST "https://api.datastack.io/products" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Widget Pro",
    "description": "Our best-selling widget.",
    "price_cents": 4999,
    "sku": "WGT-PRO-001",
    "inventory_count": 100,
    "tags": ["hardware", "featured"]
  }'
```

---

### Get product

```
GET /products/{product_id}
```

Fetch a single product by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field        | Type   | Required | Description          |
|--------------|--------|----------|----------------------|
| `product_id` | string | Yes      | The product's ID.    |

**Response** — `200 OK`

| Field             | Type            | Description                                            |
|-------------------|-----------------|--------------------------------------------------------|
| `id`              | string          | Product ID.                                            |
| `name`            | string          | Product name.                                          |
| `description`    | string          | Product description.                                   |
| `price_cents`     | integer         | Price in USD cents.                                    |
| `sku`             | string          | Stock-keeping unit identifier.                         |
| `inventory_count` | integer         | Current inventory count.                               |
| `tags`            | array of string | Product tags.                                          |
| `created_at`      | string          | ISO 8601 timestamp.                                    |

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

**Curl example**

```bash
curl -X GET "https://api.datastack.io/products/prod_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Orders

### Create order

```
POST /orders
```

Place a new order. Inventory is reserved immediately; payment is captured
asynchronously. The returned order is in `pending` status.

**Authentication**

```
Authorization: Bearer <token>
```

**Request Body**

| Field               | Type                | Required | Description                                                            |
|---------------------|---------------------|----------|------------------------------------------------------------------------|
| `user_id`           | string              | Yes      | ID of the user placing the order.                                      |
| `items`             | array of OrderItem  | Yes      | Line items in the order. Must contain at least one item.               |
| `shipping_address`  | string              | Yes      | Destination shipping address.                                          |
| `promo_code`        | string              | No       | Optional promo code to apply.                                          |
| `priority_shipping` | boolean             | No       | Whether to use priority shipping. Defaults to `false`.                 |
| `gift_message`      | string              | No       | Optional gift message to include with the order.                       |

`OrderItem` fields:

| Field              | Type    | Required | Description                                  |
|--------------------|---------|----------|----------------------------------------------|
| `product_id`       | string  | Yes      | Product ID being ordered.                    |
| `quantity`         | integer | Yes      | Number of units.                             |
| `unit_price_cents` | integer | Yes      | Per-unit price in USD cents.                 |

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

| Field               | Type                | Description                                                                  |
|---------------------|---------------------|------------------------------------------------------------------------------|
| `id`                | string              | Order ID.                                                                    |
| `user_id`           | string              | ID of the user who placed the order.                                         |
| `items`             | array of OrderItem  | Line items.                                                                  |
| `shipping_address`  | string              | Shipping address.                                                            |
| `status`            | string              | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.          |
| `total_cents`       | integer             | Order total in USD cents (sum of `quantity * unit_price_cents` per item).    |
| `promo_code`        | string \| null      | Promo code applied, if any.                                                  |
| `tracking_number`   | string \| null      | Tracking number, set when the order ships.                                   |
| `created_at`        | string              | ISO 8601 timestamp.                                                          |
| `updated_at`        | string              | ISO 8601 timestamp.                                                          |

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

**Curl example**

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

### Get order

```
GET /orders/{order_id}
```

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field      | Type   | Required | Description        |
|------------|--------|----------|--------------------|
| `order_id` | string | Yes      | The order's ID.    |

**Response** — `200 OK`

Same schema as the `POST /orders` response (see above).

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

**Curl example**

```bash
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### Update order status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition an order to
`confirmed`, `shipped`, or `delivered`. Users may cancel their own orders
while in `pending` status.

**Authentication**

```
Authorization: Bearer <token>
```

**Path Parameters**

| Field      | Type   | Required | Description        |
|------------|--------|----------|--------------------|
| `order_id` | string | Yes      | The order's ID.    |

**Request Body**

| Field             | Type   | Required | Description                                                                |
|-------------------|--------|----------|----------------------------------------------------------------------------|
| `status`          | string | Yes      | New status. One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. |
| `tracking_number` | string | No       | Tracking number to record on the order.                                    |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Same schema as the `POST /orders` response (see above).

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

**Curl example**

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

| Code | Meaning                                          |
|------|--------------------------------------------------|
| 400  | Bad request                                      |
| 401  | Missing or invalid Bearer token                  |
| 403  | Authenticated but not allowed to perform action  |
| 404  | Resource not found                               |
| 422  | Validation error in request body or parameters   |
| 500  | Internal server error                            |
