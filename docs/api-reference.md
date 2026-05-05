# DataStack API Reference

> Auto-generated reference for the DataStack core API (user management, product catalog, and order processing). Last synced from `app/routes/` by Devin.

## Authentication

All endpoints require a Bearer token passed via the `Authorization` header.

```
Authorization: Bearer <token>
```

> The previous `?api_key=` query-parameter pattern has been deprecated and is no longer accepted.

---

## Users

### `GET /users`

List all users in a given organization.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field             | Type   | Required | Description                                            |
|-------------------|--------|----------|--------------------------------------------------------|
| `organization_id` | string | Yes      | The organization whose users should be returned.       |

**Response** — `200 OK`

Returns an array of `User` objects.

| Field             | Type   | Description                                                |
|-------------------|--------|------------------------------------------------------------|
| `id`              | string | Unique user ID.                                            |
| `email`           | string | User's email address.                                      |
| `name`            | string | User's display name.                                       |
| `role`            | string | One of `admin`, `member`, `viewer`.                        |
| `organization_id` | string | The organization the user belongs to.                      |
| `created_at`      | string | ISO 8601 timestamp of when the user was created.           |

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

Create a new user. Requires `admin` role on the target organization.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field             | Type   | Required | Description                                                       |
|-------------------|--------|----------|-------------------------------------------------------------------|
| `email`           | string | Yes      | User's email address. Must be a valid email.                      |
| `name`            | string | Yes      | User's display name.                                              |
| `role`            | string | No       | One of `admin`, `member`, `viewer`. Defaults to `member`.         |
| `organization_id` | string | Yes      | The organization the user will belong to.                         |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "admin",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

Returns the created `User` object.

| Field             | Type   | Description                                      |
|-------------------|--------|--------------------------------------------------|
| `id`              | string | Unique user ID.                                  |
| `email`           | string | User's email address.                            |
| `name`            | string | User's display name.                             |
| `role`            | string | One of `admin`, `member`, `viewer`.              |
| `organization_id` | string | The organization the user belongs to.            |
| `created_at`      | string | ISO 8601 timestamp of when the user was created. |

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

| Field     | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| `user_id` | string | Yes      | The user ID to fetch. |

**Response** — `200 OK`

Returns the `User` object.

| Field             | Type   | Description                                      |
|-------------------|--------|--------------------------------------------------|
| `id`              | string | Unique user ID.                                  |
| `email`           | string | User's email address.                            |
| `name`            | string | User's display name.                             |
| `role`            | string | One of `admin`, `member`, `viewer`.              |
| `organization_id` | string | The organization the user belongs to.            |
| `created_at`      | string | ISO 8601 timestamp of when the user was created. |

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

| Field     | Type   | Required | Description            |
|-----------|--------|----------|------------------------|
| `user_id` | string | Yes      | The user ID to delete. |

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

List all products in the catalog. Optionally filter by tag.

**Authentication**

`Authorization: Bearer <token>`

**Query Parameters**

| Field | Type   | Required | Description                              |
|-------|--------|----------|------------------------------------------|
| `tag` | string | No       | If provided, only products with this tag are returned. |

**Response** — `200 OK`

Returns an array of `Product` objects.

| Field             | Type           | Description                                              |
|-------------------|----------------|----------------------------------------------------------|
| `id`              | string         | Unique product ID.                                       |
| `name`            | string         | Product name.                                            |
| `description`     | string         | Product description.                                     |
| `price_cents`     | integer        | Price in USD cents.                                      |
| `sku`             | string         | Stock keeping unit.                                      |
| `inventory_count` | integer        | Current available inventory.                             |
| `tags`            | array<string>  | List of tags applied to the product.                     |
| `created_at`      | string         | ISO 8601 timestamp of when the product was created.      |

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

Create a new product in the catalog.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field             | Type           | Required | Description                                                   |
|-------------------|----------------|----------|---------------------------------------------------------------|
| `name`            | string         | Yes      | Product name.                                                 |
| `description`     | string         | Yes      | Product description.                                          |
| `price_cents`     | integer        | Yes      | Price in USD cents.                                           |
| `sku`             | string         | Yes      | Stock keeping unit.                                           |
| `inventory_count` | integer        | No       | Initial inventory count. Defaults to `0`.                     |
| `tags`            | array<string>  | No       | List of tags. Defaults to `[]`.                               |

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

Returns the created `Product` object.

| Field             | Type           | Description                                              |
|-------------------|----------------|----------------------------------------------------------|
| `id`              | string         | Unique product ID.                                       |
| `name`            | string         | Product name.                                            |
| `description`     | string         | Product description.                                     |
| `price_cents`     | integer        | Price in USD cents.                                      |
| `sku`             | string         | Stock keeping unit.                                      |
| `inventory_count` | integer        | Current available inventory.                             |
| `tags`            | array<string>  | List of tags applied to the product.                     |
| `created_at`      | string         | ISO 8601 timestamp of when the product was created.      |

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
    "inventory_count": 100,
    "tags": ["hardware", "featured"]
  }'
```

---

### `GET /products/{product_id}`

Fetch a single product by ID.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field        | Type   | Required | Description              |
|--------------|--------|----------|--------------------------|
| `product_id` | string | Yes      | The product ID to fetch. |

**Response** — `200 OK`

Returns the `Product` object.

| Field             | Type           | Description                                              |
|-------------------|----------------|----------------------------------------------------------|
| `id`              | string         | Unique product ID.                                       |
| `name`            | string         | Product name.                                            |
| `description`     | string         | Product description.                                     |
| `price_cents`     | integer        | Price in USD cents.                                      |
| `sku`             | string         | Stock keeping unit.                                      |
| `inventory_count` | integer        | Current available inventory.                             |
| `tags`            | array<string>  | List of tags applied to the product.                     |
| `created_at`      | string         | ISO 8601 timestamp of when the product was created.      |

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

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. The returned order is in `pending` status.

**Authentication**

`Authorization: Bearer <token>`

**Request Body**

| Field               | Type             | Required | Description                                                          |
|---------------------|------------------|----------|----------------------------------------------------------------------|
| `user_id`           | string           | Yes      | The user placing the order.                                          |
| `items`             | array<OrderItem> | Yes      | Line items in the order. Must contain at least one entry.            |
| `shipping_address`  | string           | Yes      | Full shipping address as a single string.                            |
| `promo_code`        | string           | No       | Optional promo code to apply to the order.                           |
| `priority_shipping` | boolean          | No       | Request priority shipping. Defaults to `false`.                      |
| `gift_message`      | string           | No       | Optional gift message to include with the shipment.                  |

`OrderItem` fields:

| Field               | Type    | Required | Description                              |
|---------------------|---------|----------|------------------------------------------|
| `product_id`        | string  | Yes      | The product being ordered.               |
| `quantity`          | integer | Yes      | Number of units ordered.                 |
| `unit_price_cents`  | integer | Yes      | Per-unit price in USD cents.             |

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
  "promo_code": "SUMMER10",
  "priority_shipping": true,
  "gift_message": "Happy birthday!"
}
```

**Response** — `201 Created`

Returns the created `Order` object.

| Field              | Type             | Description                                                                  |
|--------------------|------------------|------------------------------------------------------------------------------|
| `id`               | string           | Unique order ID.                                                             |
| `user_id`          | string           | The user who placed the order.                                               |
| `items`            | array<OrderItem> | Line items in the order.                                                     |
| `shipping_address` | string           | Shipping address.                                                            |
| `status`           | string           | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.          |
| `total_cents`      | integer          | Total order amount in USD cents (sum of `quantity * unit_price_cents`).      |
| `promo_code`       | string \| null   | Promo code applied to the order, if any.                                     |
| `tracking_number`  | string \| null   | Carrier tracking number, set once the order ships.                           |
| `created_at`       | string           | ISO 8601 timestamp of when the order was created.                            |
| `updated_at`       | string           | ISO 8601 timestamp of the most recent update.                                |

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
  "promo_code": "SUMMER10",
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
    "promo_code": "SUMMER10",
    "priority_shipping": true,
    "gift_message": "Happy birthday!"
  }'
```

---

### `GET /orders/{order_id}`

Fetch a single order by ID. Non-admin users can only fetch their own orders.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type   | Required | Description            |
|------------|--------|----------|------------------------|
| `order_id` | string | Yes      | The order ID to fetch. |

**Response** — `200 OK`

Returns the `Order` object. Field schema is identical to `POST /orders`.

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

Update the status of an order. Only admins can transition an order to `confirmed`, `shipped`, or `delivered`. Users may cancel their own orders while still in `pending`.

**Authentication**

`Authorization: Bearer <token>`

**Path Parameters**

| Field      | Type   | Required | Description             |
|------------|--------|----------|-------------------------|
| `order_id` | string | Yes      | The order ID to update. |

**Request Body**

| Field             | Type   | Required | Description                                                                  |
|-------------------|--------|----------|------------------------------------------------------------------------------|
| `status`          | string | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`.          |
| `tracking_number` | string | No       | Carrier tracking number. Typically supplied when transitioning to `shipped`. |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Returns the updated `Order` object. Field schema is identical to `POST /orders`.

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

| Code | Meaning                              |
|------|--------------------------------------|
| 400  | Bad request                          |
| 401  | Missing or invalid bearer token      |
| 403  | Authenticated but not authorized     |
| 404  | Resource not found                   |
| 422  | Request body failed validation       |
| 500  | Internal server error                |
