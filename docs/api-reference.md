# DataStack API Reference

> **Last updated: September 2025** — This document is maintained manually. Some sections may be out of date.

## Authentication

All API requests require an API key passed as a query parameter:

```
GET /users?api_key=YOUR_API_KEY
```

---

## Users

### List Users

```
GET /users
```

Returns a list of all users in your account.

**Query Parameters**

| Parameter | Type   | Required | Description      |
|-----------|--------|----------|------------------|
| api_key   | string | Yes      | Your API key     |

**Response**

```json
[
  {
    "id": "usr_abc123",
    "email": "alice@example.com",
    "name": "Alice"
  }
]
```

---

### Create User

```
POST /users
```

Creates a new user.

**Request Body**

```json
{
  "email": "string",
  "name": "string"
}
```

> ⚠️ Note: The `role` and `organization_id` fields are not documented here but may be required.

**Response**

```json
{
  "id": "usr_abc123",
  "email": "alice@example.com",
  "name": "Alice"
}
```

---

### Get User

```
GET /users/{id}
```

Fetches a user by their ID.

**Response**

```json
{
  "id": "usr_abc123",
  "email": "alice@example.com",
  "name": "Alice"
}
```

---

## Products

### List Products

```
GET /products
```

Returns all products in the catalog.

**Query Parameters**

| Parameter | Type   | Required | Description  |
|-----------|--------|----------|--------------|
| api_key   | string | Yes      | Your API key |

**Response**

```json
[
  {
    "id": "prod_001",
    "name": "Widget Pro",
    "price": 49.99
  }
]
```

> ⚠️ Note: `price` is listed as a float here but the actual API may return `price_cents` as an integer.

---

### Create Product

```
POST /products
```

Adds a product to the catalog.

**Request Body**

```json
{
  "name": "string",
  "description": "string",
  "price": 49.99
}
```

**Response**

```json
{
  "id": "prod_001",
  "name": "Widget Pro",
  "description": "Our best widget.",
  "price": 49.99
}
```

---

### Get Product

```
GET /products/{id}
```

Fetches a product by ID.

**Response**

```json
{
  "id": "prod_001",
  "name": "Widget Pro",
  "price": 49.99
}
```

---

## Orders

*This section is coming soon. Order management endpoints are not yet available.*

---

## Error Codes

| Code | Meaning               |
|------|-----------------------|
| 400  | Bad request           |
| 401  | Invalid API key       |
| 404  | Resource not found    |
| 500  | Internal server error |
