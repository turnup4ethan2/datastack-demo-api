# DataStack API Reference

## Authentication

All API requests must include a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Requests missing or with an invalid `Authorization` header are rejected with `401 Unauthorized`.

---

## Users

### `GET /users`

List all users in an organization.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field             | Type   | Required | Description                                       |
|-------------------|--------|----------|---------------------------------------------------|
| `organization_id` | string | Yes      | Organization whose users to return.               |

**Response** — `200 OK`

Returns an array of user objects.

| Field             | Type   | Description                                              |
|-------------------|--------|----------------------------------------------------------|
| `id`              | string | User ID (e.g. `usr_abc123`).                             |
| `email`           | string | User email address.                                      |
| `name`            | string | Display name.                                            |
| `role`            | string | One of `admin`, `member`, `viewer`.                      |
| `organization_id` | string | Organization the user belongs to.                        |
| `created_at`      | string | ISO 8601 timestamp.                                      |

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

### `POST /users`

Create a new user. Requires `admin` role on the organization.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field             | Type   | Required | Description                                              |
|-------------------|--------|----------|----------------------------------------------------------|
| `email`           | string | Yes      | Valid email address.                                     |
| `name`            | string | Yes      | Display name.                                            |
| `role`            | string | No       | One of `admin`, `member`, `viewer`. Defaults to `member`.|
| `organization_id` | string | Yes      | Organization to add the user to.                         |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field             | Type   | Description                                              |
|-------------------|--------|----------------------------------------------------------|
| `id`              | string | User ID.                                                 |
| `email`           | string | User email.                                              |
| `name`            | string | Display name.                                            |
| `role`            | string | One of `admin`, `member`, `viewer`.                      |
| `organization_id` | string | Organization the user belongs to.                        |
| `created_at`      | string | ISO 8601 timestamp.                                      |

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

### `GET /users/{user_id}`

Fetch a single user by ID.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type   | Required | Description    |
|-----------|--------|----------|----------------|
| `user_id` | string | Yes      | The user's ID. |

**Response** — `200 OK`

| Field             | Type   | Description                                              |
|-------------------|--------|----------------------------------------------------------|
| `id`              | string | User ID.                                                 |
| `email`           | string | User email.                                              |
| `name`            | string | Display name.                                            |
| `role`            | string | One of `admin`, `member`, `viewer`.                      |
| `organization_id` | string | Organization the user belongs to.                        |
| `created_at`      | string | ISO 8601 timestamp.                                      |

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

### `DELETE /users/{user_id}`

Permanently delete a user. You cannot delete your own account.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field     | Type   | Required | Description              |
|-----------|--------|----------|--------------------------|
| `user_id` | string | Yes      | The user's ID to delete. |

**Response** — `204 No Content`

Empty response body on success.

**Curl**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

## Products

### `GET /products`

List all products. Optionally filter by tag.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field | Type   | Required | Description                                |
|-------|--------|----------|--------------------------------------------|
| `tag` | string | No       | If set, only return products with this tag.|

**Response** — `200 OK`

Returns an array of product objects.

| Field             | Type           | Description                                     |
|-------------------|----------------|-------------------------------------------------|
| `id`              | string         | Product ID (e.g. `prod_001`).                   |
| `name`            | string         | Product name.                                   |
| `description`    | string         | Long-form product description.                  |
| `price_cents`     | integer        | Price in USD cents (e.g. `4999` = `$49.99`).    |
| `sku`             | string         | Stock keeping unit identifier.                  |
| `inventory_count` | integer        | Number of units in stock.                       |
| `tags`            | array<string>  | Tags associated with the product.               |
| `created_at`      | string         | ISO 8601 timestamp.                             |

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

### `POST /products`

Add a new product to the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field             | Type           | Required | Description                                  |
|-------------------|----------------|----------|----------------------------------------------|
| `name`            | string         | Yes      | Product name.                                |
| `description`     | string         | Yes      | Long-form product description.               |
| `price_cents`     | integer        | Yes      | Price in USD cents (e.g. `4999` = `$49.99`). |
| `sku`             | string         | Yes      | Stock keeping unit identifier.               |
| `inventory_count` | integer        | No       | Units in stock. Defaults to `0`.             |
| `tags`            | array<string>  | No       | Tags. Defaults to `[]`.                      |

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

| Field             | Type           | Description                                     |
|-------------------|----------------|-------------------------------------------------|
| `id`              | string         | Product ID.                                     |
| `name`            | string         | Product name.                                   |
| `description`     | string         | Long-form product description.                  |
| `price_cents`     | integer        | Price in USD cents.                             |
| `sku`             | string         | Stock keeping unit identifier.                  |
| `inventory_count` | integer        | Number of units in stock.                       |
| `tags`            | array<string>  | Tags associated with the product.               |
| `created_at`      | string         | ISO 8601 timestamp.                             |

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

### `GET /products/{product_id}`

Fetch a single product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field        | Type   | Required | Description       |
|--------------|--------|----------|-------------------|
| `product_id` | string | Yes      | The product's ID. |

**Response** — `200 OK`

| Field             | Type           | Description                                     |
|-------------------|----------------|-------------------------------------------------|
| `id`              | string         | Product ID.                                     |
| `name`            | string         | Product name.                                   |
| `description`     | string         | Long-form product description.                  |
| `price_cents`     | integer        | Price in USD cents.                             |
| `sku`             | string         | Stock keeping unit identifier.                  |
| `inventory_count` | integer        | Number of units in stock.                       |
| `tags`            | array<string>  | Tags associated with the product.               |
| `created_at`      | string         | ISO 8601 timestamp.                             |

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

### `POST /orders`

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. The order is returned in `pending` status.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field               | Type             | Required | Description                                                |
|---------------------|------------------|----------|------------------------------------------------------------|
| `user_id`           | string           | Yes      | ID of the user placing the order.                          |
| `items`             | array<OrderItem> | Yes      | Line items (see below). Must contain at least one entry.   |
| `shipping_address`  | string           | Yes      | Full shipping address as a single string.                  |
| `promo_code`        | string           | No       | Optional promotional code.                                 |
| `priority_shipping` | boolean          | No       | If `true`, use priority shipping. Defaults to `false`.     |
| `gift_message`      | string           | No       | Optional gift message included with the order.             |

**`OrderItem` object**

| Field              | Type    | Required | Description                                    |
|--------------------|---------|----------|------------------------------------------------|
| `product_id`       | string  | Yes      | Product ID.                                    |
| `quantity`         | integer | Yes      | Number of units ordered.                       |
| `unit_price_cents` | integer | Yes      | Per-unit price in USD cents at time of order.  |

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
  "promo_code": "WELCOME10",
  "priority_shipping": false,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

| Field              | Type             | Description                                                                       |
|--------------------|------------------|-----------------------------------------------------------------------------------|
| `id`               | string           | Order ID (e.g. `ord_001`).                                                        |
| `user_id`          | string           | Owning user ID.                                                                   |
| `items`            | array<OrderItem> | Line items as submitted.                                                          |
| `shipping_address` | string           | Shipping address.                                                                 |
| `status`           | string           | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.               |
| `total_cents`      | integer          | Order total in USD cents (sum of `quantity * unit_price_cents` for each item).    |
| `promo_code`       | string \| null   | Applied promo code, or `null`.                                                    |
| `tracking_number`  | string \| null   | Carrier tracking number once shipped, or `null`.                                  |
| `created_at`       | string           | ISO 8601 timestamp.                                                               |
| `updated_at`       | string           | ISO 8601 timestamp.                                                               |

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
  "promo_code": "WELCOME10",
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
    "promo_code": "WELCOME10",
    "priority_shipping": false,
    "gift_message": "Happy birthday!"
  }'
```

---

### `GET /orders/{order_id}`

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type   | Required | Description     |
|------------|--------|----------|-----------------|
| `order_id` | string | Yes      | The order's ID. |

**Response** — `200 OK`

Same schema as the `POST /orders` response.

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
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer $DATASTACK_TOKEN"
```

---

### `PATCH /orders/{order_id}/status`

Update the status of an order. Only admins may transition an order to `confirmed`, `shipped`, or `delivered`. A user may cancel their own order while it is still `pending`.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type   | Required | Description     |
|------------|--------|----------|-----------------|
| `order_id` | string | Yes      | The order's ID. |

**Request Body**

| Field             | Type   | Required | Description                                                            |
|-------------------|--------|----------|------------------------------------------------------------------------|
| `status`          | string | Yes      | New status. One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`. |
| `tracking_number` | string | No       | Carrier tracking number. Typically set when transitioning to `shipped`.|

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Same schema as the `POST /orders` response, with the updated `status` and `tracking_number` reflected.

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

| Code | Meaning                                         |
|------|-------------------------------------------------|
| 400  | Bad request (invalid or missing fields).        |
| 401  | Missing or invalid `Authorization` Bearer token.|
| 403  | Authenticated but not permitted for this action.|
| 404  | Resource not found.                             |
| 422  | Request body failed schema validation.          |
| 500  | Internal server error.                          |
