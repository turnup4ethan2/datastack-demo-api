# DataStack API Reference

> **Last updated: March 2026** — Auto-generated from source code. See commit history for changes.

## Authentication

All API requests require a Bearer token passed in the `Authorization` header:

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

**Query Parameters**

| Parameter         | Type   | Required | Description                        |
|-------------------|--------|----------|------------------------------------|
| organization_id   | string | Yes      | The organization to list users for |

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Response** `200 OK`

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

**Example**

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

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Request Body**

| Field            | Type   | Required | Description                                      |
|------------------|--------|----------|--------------------------------------------------|
| email            | string | Yes      | User email address                               |
| name             | string | Yes      | User display name                                |
| role             | string | No       | `"admin"`, `"member"`, or `"viewer"` (default: `"member"`) |
| organization_id  | string | Yes      | Organization the user belongs to                 |

```json
{
  "email": "alice@datastack.io",
  "name": "Alice",
  "role": "member",
  "organization_id": "org_xyz"
}
```

**Response** `201 Created`

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

**Example**

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

### Get User

```
GET /users/{user_id}
```

Fetch a single user by ID.

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Yes      | The user ID |

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Response** `200 OK`

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

**Example**

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

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Yes      | The user ID |

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Response** `204 No Content`

No response body.

**Example**

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

**Query Parameters**

| Parameter | Type   | Required | Description                  |
|-----------|--------|----------|------------------------------|
| tag       | string | No       | Filter products by this tag  |

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Response** `200 OK`

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

**Example**

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

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Request Body**

| Field            | Type         | Required | Description                        |
|------------------|--------------|----------|------------------------------------|
| name             | string       | Yes      | Product name                       |
| description      | string       | Yes      | Product description                |
| price_cents      | integer      | Yes      | Price in cents (USD)               |
| sku              | string       | Yes      | Stock-keeping unit identifier      |
| inventory_count  | integer      | No       | Initial inventory count (default: `0`) |
| tags             | string[]     | No       | List of tags (default: `[]`)       |

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

**Response** `201 Created`

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

**Example**

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

**Path Parameters**

| Parameter   | Type   | Required | Description    |
|-------------|--------|----------|----------------|
| product_id  | string | Yes      | The product ID |

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Response** `200 OK`

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

**Example**

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

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. Returns the order in "pending" status.

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Request Body**

| Field             | Type         | Required | Description                            |
|-------------------|--------------|----------|----------------------------------------|
| user_id           | string       | Yes      | The user placing the order             |
| items             | OrderItem[]  | Yes      | List of items in the order             |
| shipping_address  | string       | Yes      | Shipping address for the order         |
| promo_code        | string       | No       | Promotional code to apply              |
| gift_message      | string       | No       | Gift message to attach to the order    |

Each `OrderItem` contains:

| Field            | Type    | Required | Description                  |
|------------------|---------|----------|------------------------------|
| product_id       | string  | Yes      | The product ID               |
| quantity         | integer | Yes      | Quantity ordered              |
| unit_price_cents | integer | Yes      | Unit price in cents (USD)    |

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
  "gift_message": "Happy birthday!"
}
```

**Response** `201 Created`

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
  "gift_message": "Happy birthday!",
  "tracking_number": null,
  "created_at": "2026-03-20T00:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Example**

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
    "gift_message": "Happy birthday!"
  }'
```

---

### Get Order

```
GET /orders/{order_id}
```

Fetch a single order by ID. Users can only fetch their own orders.

**Path Parameters**

| Parameter | Type   | Required | Description  |
|-----------|--------|----------|--------------|
| order_id  | string | Yes      | The order ID |

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Response** `200 OK`

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
  "gift_message": null,
  "tracking_number": "1Z999AA10123456784",
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-19T08:30:00Z"
}
```

**Example**

```bash
curl -X GET "https://api.datastack.io/orders/ord_001" \
  -H "Authorization: Bearer <token>"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition to "confirmed", "shipped", or "delivered". Users may cancel their own "pending" orders.

**Path Parameters**

| Parameter | Type   | Required | Description  |
|-----------|--------|----------|--------------|
| order_id  | string | Yes      | The order ID |

**Headers**

| Header          | Type   | Required | Description          |
|-----------------|--------|----------|----------------------|
| Authorization   | string | Yes      | `Bearer <token>`     |

**Request Body**

| Field            | Type   | Required | Description                                                                 |
|------------------|--------|----------|-----------------------------------------------------------------------------|
| status           | string | Yes      | New status: `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, or `"cancelled"` |
| tracking_number  | string | No       | Tracking number (typically set when status is `"shipped"`)                  |

```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response** `200 OK`

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
  "gift_message": null,
  "tracking_number": "1Z999AA10123456784",
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-20T00:00:00Z"
}
```

**Example**

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

| Code | Meaning               |
|------|-----------------------|
| 400  | Bad request           |
| 401  | Unauthorized          |
| 404  | Resource not found    |
| 422  | Validation error      |
| 500  | Internal server error |
