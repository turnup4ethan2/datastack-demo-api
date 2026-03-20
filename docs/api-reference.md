# DataStack API Reference

> **Last updated: March 2026** — This document is auto-generated from the current source code.

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

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Parameter       | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| organization_id | string | Yes      | The organization to list users for   |

**Response** `200 OK`

```json
[
  {
    "id": "string",
    "email": "string",
    "name": "string",
    "role": "string",
    "organization_id": "string",
    "created_at": "string (ISO 8601)"
  }
]
```

**Example**

```bash
curl -X GET "https://api.datastack.example/users?organization_id=org_xyz" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Create User

```
POST /users
```

Create a new user. Requires admin role on the organization.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field           | Type   | Required | Description                                    |
|-----------------|--------|----------|------------------------------------------------|
| email           | string | Yes      | Valid email address                            |
| name            | string | Yes      | User's display name                            |
| role            | string | No       | One of `"admin"`, `"member"`, `"viewer"` (default: `"member"`) |
| organization_id | string | Yes      | Organization the user belongs to               |

**Response** `201 Created`

```json
{
  "id": "string",
  "email": "string",
  "name": "string",
  "role": "string",
  "organization_id": "string",
  "created_at": "string (ISO 8601)"
}
```

**Example**

```bash
curl -X POST "https://api.datastack.example/users" \
  -H "Authorization: Bearer YOUR_TOKEN" \
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

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Yes      | The user ID |

**Response** `200 OK`

```json
{
  "id": "string",
  "email": "string",
  "name": "string",
  "role": "string",
  "organization_id": "string",
  "created_at": "string (ISO 8601)"
}
```

**Example**

```bash
curl -X GET "https://api.datastack.example/users/usr_abc123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently delete a user. Cannot delete your own account.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Yes      | The user ID |

**Response** `204 No Content`

No response body.

**Example**

```bash
curl -X DELETE "https://api.datastack.example/users/usr_abc123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Products

### List Products

```
GET /products
```

List all products in the catalog. Optionally filter by tag.

**Authentication:** `Authorization: Bearer <token>`

**Query Parameters**

| Parameter | Type   | Required | Description                    |
|-----------|--------|----------|--------------------------------|
| tag       | string | No       | Filter products by this tag    |

**Response** `200 OK`

```json
[
  {
    "id": "string",
    "name": "string",
    "description": "string",
    "price_cents": "integer",
    "sku": "string",
    "inventory_count": "integer",
    "tags": ["string"],
    "created_at": "string (ISO 8601)"
  }
]
```

**Example**

```bash
curl -X GET "https://api.datastack.example/products?tag=hardware" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Create Product

```
POST /products
```

Create a new product in the catalog.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field           | Type     | Required | Description                          |
|-----------------|----------|----------|--------------------------------------|
| name            | string   | Yes      | Product name                         |
| description     | string   | Yes      | Product description                  |
| price_cents     | integer  | Yes      | Price in cents (USD)                 |
| sku             | string   | Yes      | Stock keeping unit identifier        |
| inventory_count | integer  | No       | Number of items in stock (default: 0)|
| tags            | string[] | No       | List of tags (default: [])           |

**Response** `201 Created`

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price_cents": "integer",
  "sku": "string",
  "inventory_count": "integer",
  "tags": ["string"],
  "created_at": "string (ISO 8601)"
}
```

**Example**

```bash
curl -X POST "https://api.datastack.example/products" \
  -H "Authorization: Bearer YOUR_TOKEN" \
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

### Get Product

```
GET /products/{product_id}
```

Fetch a single product by ID.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter  | Type   | Required | Description    |
|------------|--------|----------|----------------|
| product_id | string | Yes      | The product ID |

**Response** `200 OK`

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price_cents": "integer",
  "sku": "string",
  "inventory_count": "integer",
  "tags": ["string"],
  "created_at": "string (ISO 8601)"
}
```

**Example**

```bash
curl -X GET "https://api.datastack.example/products/prod_001" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Orders

### Create Order

```
POST /orders
```

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. Returns the order in "pending" status.

**Authentication:** `Authorization: Bearer <token>`

**Request Body**

| Field             | Type     | Required | Description                                   |
|-------------------|----------|----------|-----------------------------------------------|
| user_id           | string   | Yes      | The user placing the order                    |
| items             | object[] | Yes      | List of order items (see below)               |
| shipping_address  | string   | Yes      | Full shipping address                         |
| promo_code        | string   | No       | Promotional code to apply                     |
| gift_message      | string   | No       | Gift message to attach to the order           |
| priority_shipping | boolean  | No       | Enable priority shipping (default: false)     |

**Order Item Object**

| Field           | Type    | Required | Description               |
|-----------------|---------|----------|---------------------------|
| product_id      | string  | Yes      | Product identifier        |
| quantity        | integer | Yes      | Number of units           |
| unit_price_cents| integer | Yes      | Price per unit in cents   |

**Response** `201 Created`

```json
{
  "id": "string",
  "user_id": "string",
  "items": [
    {
      "product_id": "string",
      "quantity": "integer",
      "unit_price_cents": "integer"
    }
  ],
  "shipping_address": "string",
  "status": "string",
  "total_cents": "integer",
  "promo_code": "string | null",
  "gift_message": "string | null",
  "tracking_number": "string | null",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

**Example**

```bash
curl -X POST "https://api.datastack.example/orders" \
  -H "Authorization: Bearer YOUR_TOKEN" \
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
    "promo_code": null,
    "gift_message": "Happy Birthday!",
    "priority_shipping": true
  }'
```

---

### Get Order

```
GET /orders/{order_id}
```

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter | Type   | Required | Description  |
|-----------|--------|----------|--------------|
| order_id  | string | Yes      | The order ID |

**Response** `200 OK`

```json
{
  "id": "string",
  "user_id": "string",
  "items": [
    {
      "product_id": "string",
      "quantity": "integer",
      "unit_price_cents": "integer"
    }
  ],
  "shipping_address": "string",
  "status": "string",
  "total_cents": "integer",
  "promo_code": "string | null",
  "gift_message": "string | null",
  "tracking_number": "string | null",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

**Example**

```bash
curl -X GET "https://api.datastack.example/orders/ord_001" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition to "confirmed", "shipped", or "delivered". Users may cancel their own "pending" orders.

**Authentication:** `Authorization: Bearer <token>`

**Path Parameters**

| Parameter | Type   | Required | Description  |
|-----------|--------|----------|--------------|
| order_id  | string | Yes      | The order ID |

**Request Body**

| Field           | Type   | Required | Description                                                                 |
|-----------------|--------|----------|-----------------------------------------------------------------------------|
| status          | string | Yes      | One of `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, `"cancelled"` |
| tracking_number | string | No       | Shipment tracking number                                                    |

**Response** `200 OK`

```json
{
  "id": "string",
  "user_id": "string",
  "items": [
    {
      "product_id": "string",
      "quantity": "integer",
      "unit_price_cents": "integer"
    }
  ],
  "shipping_address": "string",
  "status": "string",
  "total_cents": "integer",
  "promo_code": "string | null",
  "gift_message": "string | null",
  "tracking_number": "string | null",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

**Example**

```bash
curl -X PATCH "https://api.datastack.example/orders/ord_001/status" \
  -H "Authorization: Bearer YOUR_TOKEN" \
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
