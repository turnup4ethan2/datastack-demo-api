# DataStack API Reference

> **Last updated: July 2026** — Reflects the current route implementations in `app/routes/`.

## Authentication

All API requests require a Bearer token passed in the `Authorization` header:

```
Authorization: Bearer <token>
```

> API key query parameters (`?api_key=...`) are deprecated and no longer supported.

The examples below use `https://api.datastack.io` as the base URL.

---

## Users

### GET /users

List all users in the given organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Query parameters:

| Field             | Type   | Required | Description                        |
|-------------------|--------|----------|------------------------------------|
| `organization_id` | string | Yes      | Organization whose users to return |

**Response** — `200 OK`

Returns an array of user objects.

| Field             | Type   | Description                                |
|-------------------|--------|--------------------------------------------|
| `id`              | string | Unique user ID                             |
| `email`           | string | User email address                         |
| `name`            | string | User display name                          |
| `role`            | string | One of `admin`, `member`, `viewer`         |
| `organization_id` | string | Organization the user belongs to           |
| `created_at`      | string | ISO 8601 creation timestamp                |

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
curl "https://api.datastack.io/users?organization_id=org_xyz" \
  -H "Authorization: Bearer <token>"
```

---

### POST /users

Create a new user. Requires `admin` role on the organization.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Request body fields:

| Field             | Type   | Required | Description                                          |
|-------------------|--------|----------|------------------------------------------------------|
| `email`           | string | Yes      | User email address (must be a valid email)           |
| `name`            | string | Yes      | User display name                                    |
| `role`            | string | No       | One of `admin`, `member`, `viewer` (default `member`)|
| `organization_id` | string | Yes      | Organization the user belongs to                     |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** — `201 Created`

| Field             | Type   | Description                        |
|-------------------|--------|------------------------------------|
| `id`              | string | Unique user ID                     |
| `email`           | string | User email address                 |
| `name`            | string | User display name                  |
| `role`            | string | One of `admin`, `member`, `viewer` |
| `organization_id` | string | Organization the user belongs to   |
| `created_at`      | string | ISO 8601 creation timestamp        |

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

**Curl example**

```bash
curl -X POST "https://api.datastack.io/users" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@datastack.io",
    "name": "Alice",
    "role": "member",
    "organization_id": "org_xyz"
  }'
```

---

### GET /users/{user_id}

Fetch a single user by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field     | Type   | Required | Description        |
|-----------|--------|----------|--------------------|
| `user_id` | string | Yes      | ID of the user     |

**Response** — `200 OK`

| Field             | Type   | Description                        |
|-------------------|--------|------------------------------------|
| `id`              | string | Unique user ID                     |
| `email`           | string | User email address                 |
| `name`            | string | User display name                  |
| `role`            | string | One of `admin`, `member`, `viewer` |
| `organization_id` | string | Organization the user belongs to   |
| `created_at`      | string | ISO 8601 creation timestamp        |

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
curl "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

### DELETE /users/{user_id}

Permanently delete a user. You cannot delete your own account.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field     | Type   | Required | Description             |
|-----------|--------|----------|-------------------------|
| `user_id` | string | Yes      | ID of the user to delete|

**Response** — `204 No Content`

Returns an empty body on success.

**Curl example**

```bash
curl -X DELETE "https://api.datastack.io/users/usr_abc123" \
  -H "Authorization: Bearer <token>"
```

---

## Products

### GET /products

List all products. Optionally filter by tag.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Query parameters:

| Field | Type   | Required | Description                     |
|-------|--------|----------|---------------------------------|
| `tag` | string | No       | Filter products by a single tag |

**Response** — `200 OK`

Returns an array of product objects.

| Field             | Type          | Description                          |
|-------------------|---------------|--------------------------------------|
| `id`              | string        | Unique product ID                    |
| `name`            | string        | Product name                         |
| `description`     | string        | Product description                  |
| `price_cents`     | integer       | Price in USD cents                   |
| `sku`             | string        | Stock keeping unit                   |
| `inventory_count` | integer       | Units in stock                       |
| `tags`            | array[string] | Product tags                         |
| `created_at`      | string        | ISO 8601 creation timestamp          |

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
curl "https://api.datastack.io/products?tag=featured" \
  -H "Authorization: Bearer <token>"
```

---

### POST /products

Create a new product in the catalog.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Request body fields:

| Field             | Type          | Required | Description                        |
|-------------------|---------------|----------|------------------------------------|
| `name`            | string        | Yes      | Product name                       |
| `description`     | string        | Yes      | Product description                |
| `price_cents`     | integer       | Yes      | Price in USD cents                 |
| `sku`             | string        | Yes      | Stock keeping unit                 |
| `inventory_count` | integer       | No       | Units in stock (default `0`)       |
| `tags`            | array[string] | No       | Product tags (default `[]`)        |

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

| Field             | Type          | Description                 |
|-------------------|---------------|-----------------------------|
| `id`              | string        | Unique product ID           |
| `name`            | string        | Product name                |
| `description`     | string        | Product description         |
| `price_cents`     | integer       | Price in USD cents          |
| `sku`             | string        | Stock keeping unit          |
| `inventory_count` | integer       | Units in stock              |
| `tags`            | array[string] | Product tags                |
| `created_at`      | string        | ISO 8601 creation timestamp |

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

**Curl example**

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

### GET /products/{product_id}

Fetch a single product by ID.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field        | Type   | Required | Description        |
|--------------|--------|----------|--------------------|
| `product_id` | string | Yes      | ID of the product  |

**Response** — `200 OK`

| Field             | Type          | Description                 |
|-------------------|---------------|-----------------------------|
| `id`              | string        | Unique product ID           |
| `name`            | string        | Product name                |
| `description`     | string        | Product description         |
| `price_cents`     | integer       | Price in USD cents          |
| `sku`             | string        | Stock keeping unit          |
| `inventory_count` | integer       | Units in stock              |
| `tags`            | array[string] | Product tags                |
| `created_at`      | string        | ISO 8601 creation timestamp |

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
curl "https://api.datastack.io/products/prod_001" \
  -H "Authorization: Bearer <token>"
```

---

## Orders

The order object (`OrderResponse`) has the following shape:

| Field             | Type              | Description                                                              |
|-------------------|-------------------|--------------------------------------------------------------------------|
| `id`              | string            | Unique order ID                                                          |
| `user_id`         | string            | ID of the user who placed the order                                      |
| `items`           | array[OrderItem]  | Line items (see below)                                                   |
| `shipping_address`| string            | Shipping address                                                         |
| `status`          | string            | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`       |
| `total_cents`     | integer           | Order total in USD cents                                                 |
| `promo_code`      | string \| null    | Applied promo code, if any                                               |
| `tracking_number` | string \| null    | Shipment tracking number, if available                                   |
| `created_at`      | string            | ISO 8601 creation timestamp                                              |
| `updated_at`      | string            | ISO 8601 last-update timestamp                                           |

Each `OrderItem` has:

| Field              | Type    | Description                    |
|--------------------|---------|--------------------------------|
| `product_id`       | string  | ID of the product ordered      |
| `quantity`         | integer | Number of units                |
| `unit_price_cents` | integer | Per-unit price in USD cents    |

### POST /orders

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. Returns the order in `pending` status.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Request body fields:

| Field              | Type             | Required | Description                                       |
|--------------------|------------------|----------|---------------------------------------------------|
| `user_id`          | string           | Yes      | ID of the user placing the order                  |
| `items`            | array[OrderItem] | Yes      | Line items; each has `product_id`, `quantity`, `unit_price_cents` |
| `shipping_address` | string           | Yes      | Shipping address                                  |
| `promo_code`       | string           | No       | Promo code to apply (default `null`)              |
| `priority_shipping`| boolean          | No       | Request priority shipping (default `false`)       |
| `gift_message`     | string           | No       | Gift message to include (default `null`)          |

```json
{
  "user_id": "usr_abc123",
  "items": [
    { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
  ],
  "shipping_address": "123 Main St, San Francisco, CA 94105",
  "promo_code": "SAVE10",
  "priority_shipping": false,
  "gift_message": "Happy Birthday!"
}
```

**Response** — `201 Created`

Returns an order object (see the schema above). `total_cents` is computed as the sum of `quantity * unit_price_cents` across items.

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
  "promo_code": "SAVE10",
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Curl example**

```bash
curl -X POST "https://api.datastack.io/orders" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usr_abc123",
    "items": [
      { "product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999 }
    ],
    "shipping_address": "123 Main St, San Francisco, CA 94105",
    "promo_code": "SAVE10",
    "priority_shipping": false,
    "gift_message": "Happy Birthday!"
  }'
```

---

### GET /orders/{order_id}

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field      | Type   | Required | Description      |
|------------|--------|----------|------------------|
| `order_id` | string | Yes      | ID of the order  |

**Response** — `200 OK`

Returns an order object (see the schema above).

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

**Curl example**

```bash
curl "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer <token>"
```

---

### PATCH /orders/{order_id}/status

Update the status of an order. Only admins can transition to `confirmed`, `shipped`, or `delivered`. Users may cancel their own `pending` orders.

**Authentication**

```
Authorization: Bearer <token>
```

**Request**

Path parameters:

| Field      | Type   | Required | Description      |
|------------|--------|----------|------------------|
| `order_id` | string | Yes      | ID of the order  |

Request body fields:

| Field             | Type   | Required | Description                                                          |
|-------------------|--------|----------|----------------------------------------------------------------------|
| `status`          | string | Yes      | One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`   |
| `tracking_number` | string | No       | Shipment tracking number (default `null`)                            |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** — `200 OK`

Returns the updated order object (see the schema above).

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

**Curl example**

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

## Error Codes

| Code | Meaning                          |
|------|----------------------------------|
| 400  | Bad request                      |
| 401  | Missing or invalid Bearer token  |
| 404  | Resource not found               |
| 500  | Internal server error            |
