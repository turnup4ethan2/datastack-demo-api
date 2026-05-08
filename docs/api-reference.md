# DataStack API Reference

> Generated from `app/routes/` by Devin. Reflects the API as implemented at commit `596063f`.

## Authentication

All endpoints require a Bearer token passed via the `Authorization` header:

```
Authorization: Bearer <token>
```

Requests missing or with an invalid `Authorization` header return `401 Unauthorized`.

> The previous `?api_key=` query-parameter pattern has been removed and is no longer accepted.

---

## Users

### GET /users — List Users

Returns all users belonging to the given organization.

**Authentication**

`Authorization: Bearer <token>`

**Request — Query Parameters**

| Field             | Type     | Required | Description                                |
|-------------------|----------|----------|--------------------------------------------|
| `organization_id` | `string` | Yes      | Organization whose users should be listed. |

**Response — `200 OK`**

| Field             | Type     | Description                                            |
|-------------------|----------|--------------------------------------------------------|
| `id`              | `string` | User ID (`usr_…`).                                     |
| `email`           | `string` | User's email address.                                  |
| `name`            | `string` | Display name.                                          |
| `role`            | `string` | One of `admin`, `member`, `viewer`.                    |
| `organization_id` | `string` | Organization the user belongs to.                      |
| `created_at`      | `string` | ISO 8601 timestamp of when the user was created (UTC). |

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

### POST /users — Create User

Creates a new user. Requires admin role on the target organization.

**Authentication**

`Authorization: Bearer <token>`

**Request — Body**

| Field             | Type     | Required | Description                                                  |
|-------------------|----------|----------|--------------------------------------------------------------|
| `email`           | `string` | Yes      | Valid email address.                                         |
| `name`            | `string` | Yes      | Display name.                                                |
| `role`            | `string` | No       | One of `admin`, `member`, `viewer`. Defaults to `member`.    |
| `organization_id` | `string` | Yes      | Organization to which the new user will belong.              |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response — `201 Created`**

| Field             | Type     | Description                                  |
|-------------------|----------|----------------------------------------------|
| `id`              | `string` | New user ID.                                 |
| `email`           | `string` | User's email address.                        |
| `name`            | `string` | Display name.                                |
| `role`            | `string` | One of `admin`, `member`, `viewer`.          |
| `organization_id` | `string` | Organization the user belongs to.            |
| `created_at`      | `string` | ISO 8601 timestamp of creation (UTC).        |

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

### GET /users/{user_id} — Get User

Fetches a single user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request — Path Parameters**

| Field     | Type     | Required | Description    |
|-----------|----------|----------|----------------|
| `user_id` | `string` | Yes      | User ID.       |

**Response — `200 OK`**

Same schema as `POST /users` response.

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

### DELETE /users/{user_id} — Delete User

Permanently deletes a user. A token cannot be used to delete its own account.

**Authentication**

`Authorization: Bearer <token>`

**Request — Path Parameters**

| Field     | Type     | Required | Description    |
|-----------|----------|----------|----------------|
| `user_id` | `string` | Yes      | User ID.       |

**Response — `204 No Content`**

Empty response body.

**Curl**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### GET /products — List Products

Returns all products in the catalog. Optionally filters by tag.

**Authentication**

`Authorization: Bearer <token>`

**Request — Query Parameters**

| Field | Type     | Required | Description                                  |
|-------|----------|----------|----------------------------------------------|
| `tag` | `string` | No       | Return only products containing this tag.    |

**Response — `200 OK`**

| Field             | Type            | Description                                              |
|-------------------|-----------------|----------------------------------------------------------|
| `id`              | `string`        | Product ID (`prod_…`).                                   |
| `name`            | `string`        | Product name.                                            |
| `description`     | `string`        | Product description.                                     |
| `price_cents`     | `integer`       | Price in USD cents (e.g. `4999` = $49.99).               |
| `sku`             | `string`        | Stock keeping unit.                                      |
| `inventory_count` | `integer`       | Units currently on hand.                                 |
| `tags`            | `array<string>` | Free-form tags attached to the product.                  |
| `created_at`      | `string`        | ISO 8601 timestamp of creation (UTC).                    |

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

### POST /products — Create Product

Adds a product to the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request — Body**

| Field             | Type            | Required | Description                                                |
|-------------------|-----------------|----------|------------------------------------------------------------|
| `name`            | `string`        | Yes      | Product name.                                              |
| `description`     | `string`        | Yes      | Product description.                                       |
| `price_cents`     | `integer`       | Yes      | Price in USD cents (e.g. `4999` = $49.99).                 |
| `sku`             | `string`        | Yes      | Stock keeping unit. Must be unique within the catalog.     |
| `inventory_count` | `integer`       | No       | Initial units on hand. Defaults to `0`.                    |
| `tags`            | `array<string>` | No       | Free-form tags. Defaults to `[]`.                          |

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

### GET /products/{product_id} — Get Product

Fetches a single product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Request — Path Parameters**

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `product_id` | `string` | Yes      | Product ID. |

**Response — `200 OK`**

Same schema as `POST /products` response.

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

### POST /orders — Create Order

Places a new order. Inventory is reserved immediately; payment is captured asynchronously. The returned order is always in `pending` status.

**Authentication**

`Authorization: Bearer <token>`

**Request — Body**

| Field               | Type              | Required | Description                                                       |
|---------------------|-------------------|----------|-------------------------------------------------------------------|
| `user_id`           | `string`          | Yes      | User placing the order.                                           |
| `items`             | `array<OrderItem>`| Yes      | Line items. Must contain at least one item.                       |
| `shipping_address`  | `string`          | Yes      | Full shipping address as a single string.                         |
| `promo_code`        | `string`          | No       | Optional promotional code.                                        |
| `priority_shipping` | `boolean`         | No       | Whether to use priority shipping. Defaults to `false`.            |
| `gift_message`      | `string`          | No       | Optional gift message printed on the packing slip.                |

`OrderItem`:

| Field              | Type      | Required | Description                                |
|--------------------|-----------|----------|--------------------------------------------|
| `product_id`       | `string`  | Yes      | Product ID being ordered.                  |
| `quantity`         | `integer` | Yes      | Number of units.                           |
| `unit_price_cents` | `integer` | Yes      | Per-unit price in USD cents.               |

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

**Response — `201 Created`**

| Field              | Type              | Description                                                                |
|--------------------|-------------------|----------------------------------------------------------------------------|
| `id`               | `string`          | Order ID (`ord_…`).                                                        |
| `user_id`          | `string`          | Owning user.                                                               |
| `items`            | `array<OrderItem>`| Line items as submitted.                                                   |
| `shipping_address` | `string`          | Shipping address.                                                          |
| `status`           | `string`          | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.        |
| `total_cents`      | `integer`         | Sum of `quantity * unit_price_cents` across all items, in USD cents.       |
| `promo_code`       | `string \| null`  | Promo code applied, if any.                                                |
| `tracking_number`  | `string \| null`  | Carrier tracking number; `null` until shipment.                            |
| `created_at`       | `string`          | ISO 8601 timestamp of creation (UTC).                                      |
| `updated_at`       | `string`          | ISO 8601 timestamp of the last update (UTC).                               |

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

**Curl**

```bash
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer $DATASTACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usr_abc123",
    "items": [
      { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
    ],
    "shipping_address": "123 Main St, San Francisco, CA 94105",
    "promo_code": "SPRING10",
    "priority_shipping": true,
    "gift_message": "Happy birthday!"
  }'
```

---

### GET /orders/{order_id} — Get Order

Fetches a single order by ID. Non-admin tokens may only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Request — Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID.   |

**Response — `200 OK`**

Same schema as `POST /orders` response.

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

**Curl**

```bash
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### PATCH /orders/{order_id}/status — Update Order Status

Updates an order's status. Only admins may transition orders to `confirmed`, `shipped`, or `delivered`. Regular users may cancel their own `pending` orders.

**Authentication**

`Authorization: Bearer <token>`

**Request — Path Parameters**

| Field      | Type     | Required | Description |
|------------|----------|----------|-------------|
| `order_id` | `string` | Yes      | Order ID.   |

**Request — Body**

| Field             | Type     | Required | Description                                                          |
|-------------------|----------|----------|----------------------------------------------------------------------|
| `status`          | `string` | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.  |
| `tracking_number` | `string` | No       | Carrier tracking number. Typically set when transitioning to `shipped`. |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response — `200 OK`**

Same schema as `POST /orders` response.

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

| Code | Meaning                                              |
|------|------------------------------------------------------|
| 400  | Bad request (malformed body or invalid field value). |
| 401  | Missing or invalid `Authorization` Bearer token.     |
| 403  | Authenticated but not permitted to perform action.   |
| 404  | Resource not found.                                  |
| 422  | Request body failed validation.                      |
| 500  | Internal server error.                               |
