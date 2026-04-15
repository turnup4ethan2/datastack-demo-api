# DataStack API Reference

> **Last updated: April 2026** — This document is kept in sync automatically by Devin.

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

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Query Parameters**

| Parameter       | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| organization_id | string | Yes      | The organization to list users for   |

**Response** — `200 OK`

```json
[
  {
    "id": "usr_abc123",
    "email": "alice@example.com",
    "name": "Alice",
    "role": "admin",
    "organization_id": "org_xyz",
    "created_at": "2026-01-01T00:00:00Z"
  }
]
```

**Example**

```bash
curl -H "Authorization: Bearer <token>" \
  "https://api.datastack.io/users?organization_id=org_xyz"
```

---

### Create User

```
POST /users
```

Create a new user. Requires admin role on the organization.

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Request Body**

| Field           | Type   | Required | Description                                  |
|-----------------|--------|----------|----------------------------------------------|
| email           | string | Yes      | Email address (must be valid)                |
| name            | string | Yes      | Display name                                 |
| role            | string | No       | `"admin"`, `"member"`, or `"viewer"` (default: `"member"`) |
| organization_id | string | Yes      | Organization the user belongs to             |

**Response** — `201 Created`

```json
{
  "id": "usr_abc123",
  "email": "alice@example.com",
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
    "email": "alice@example.com",
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

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Yes      | The user ID |

**Response** — `200 OK`

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
curl -H "Authorization: Bearer <token>" \
  "https://api.datastack.io/users/usr_abc123"
```

---

### Delete User

```
DELETE /users/{user_id}
```

Permanently delete a user. Cannot delete your own account.

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Path Parameters**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Yes      | The user ID |

**Response** — `204 No Content`

No response body.

**Example**

```bash
curl -X DELETE -H "Authorization: Bearer <token>" \
  "https://api.datastack.io/users/usr_abc123"
```

---

## Products

### List Products

```
GET /products
```

List all products in the catalog. Optionally filter by tag.

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Query Parameters**

| Parameter | Type   | Required | Description              |
|-----------|--------|----------|--------------------------|
| tag       | string | No       | Filter products by tag   |

**Response** — `200 OK`

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
curl -H "Authorization: Bearer <token>" \
  "https://api.datastack.io/products?tag=featured"
```

---

### Create Product

```
POST /products
```

Create a new product in the catalog.

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Request Body**

| Field           | Type        | Required | Description                       |
|-----------------|-------------|----------|-----------------------------------|
| name            | string      | Yes      | Product name                      |
| description     | string      | Yes      | Product description               |
| price_cents     | integer     | Yes      | Price in cents (USD)              |
| sku             | string      | Yes      | Stock-keeping unit identifier     |
| inventory_count | integer     | No       | Initial inventory (default: `0`)  |
| tags            | string[]    | No       | List of tags (default: `[]`)      |

**Response** — `201 Created`

```json
{
  "id": "prod_001",
  "name": "Widget Pro",
  "description": "Our best-selling widget.",
  "price_cents": 4999,
  "sku": "WGT-PRO-001",
  "inventory_count": 0,
  "tags": [],
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

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Path Parameters**

| Parameter  | Type   | Required | Description    |
|------------|--------|----------|----------------|
| product_id | string | Yes      | The product ID |

**Response** — `200 OK`

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
curl -H "Authorization: Bearer <token>" \
  "https://api.datastack.io/products/prod_001"
```

---

## Orders

### Create Order

```
POST /orders
```

Place a new order. Inventory is reserved immediately; payment is captured asynchronously. Returns the order in `"pending"` status.

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Request Body**

| Field             | Type        | Required | Description                                  |
|-------------------|-------------|----------|----------------------------------------------|
| user_id           | string      | Yes      | ID of the user placing the order             |
| items             | OrderItem[] | Yes      | List of items (see below)                    |
| shipping_address  | string      | Yes      | Full shipping address                        |
| promo_code        | string      | No       | Promotional / discount code                  |
| priority_shipping | boolean     | No       | Enable priority shipping (default: `false`)  |
| gift_message      | string      | No       | Gift message to include with the order       |

**OrderItem**

| Field            | Type    | Required | Description                   |
|------------------|---------|----------|-------------------------------|
| product_id       | string  | Yes      | Product ID                    |
| quantity         | integer | Yes      | Number of units               |
| unit_price_cents | integer | Yes      | Price per unit in cents (USD) |

**Response** — `201 Created`

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
  "promo_code": null,
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
    "shipping_address": "123 Main St, San Francisco, CA 94105"
  }'
```

---

### Get Order

```
GET /orders/{order_id}
```

Fetch a single order by ID. Users can only fetch their own orders.

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Path Parameters**

| Parameter | Type   | Required | Description  |
|-----------|--------|----------|--------------|
| order_id  | string | Yes      | The order ID |

**Response** — `200 OK`

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

**Example**

```bash
curl -H "Authorization: Bearer <token>" \
  "https://api.datastack.io/orders/ord_001"
```

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

Update the status of an order. Only admins can transition to `"confirmed"`, `"shipped"`, or `"delivered"`. Users may cancel their own `"pending"` orders.

**Authentication**

| Header          | Format         | Required |
|-----------------|----------------|----------|
| Authorization   | Bearer \<token\> | Yes      |

**Path Parameters**

| Parameter | Type   | Required | Description  |
|-----------|--------|----------|--------------|
| order_id  | string | Yes      | The order ID |

**Request Body**

| Field           | Type   | Required | Description                                                                 |
|-----------------|--------|----------|-----------------------------------------------------------------------------|
| status          | string | Yes      | One of: `"pending"`, `"confirmed"`, `"shipped"`, `"delivered"`, `"cancelled"` |
| tracking_number | string | No       | Carrier tracking number (typically set when status is `"shipped"`)          |

**Response** — `200 OK`

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

**Example**

```bash
curl "https://api.datastack.io/health"
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
