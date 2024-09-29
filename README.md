# Fund Management System API

## Overview
This is a backend service for managing investment funds. The API provides functionality for retrieving, creating, updating, and deleting funds, as well as managing associated data such as fund managers. The backend is built using Python and Flask, with data persistence implemented using SQLite.

## Features
- Retrieve a list of funds.
- Create a new funds.
- Retrive details of a specific fund.
- Update the performance of a fund.
- Delete a fund.
- Data persistence using SQLite.

## Technologies Used
- Python
- Flask
- SQLite
- SQLAlchemy
- Postman (for testing)

## Installation
Clone the repository:

```bash
git clone <repository_url>
cd fund-management-system
```

Run the application:
```bash
python app.py
```

## Endpoints
Retrieve All Funds
- URL: /funds
- Method: GET
- Response: Returns a list of all funds with their details.
```json
[
  {
    "fund_id": 1,
    "name": "Tech Fund 1",
    "manager_name": "Bob",
    "description": "A technology investment fund.",
    "nav": 2000.0,
    "date_of_creation": "2024-09-29",
    "performance": 1.5
  },
  {
    "fund_id": 2,
    "name": "Health Fund 2",
    "manager_name": "Alice",
    "description": "A healthcare investment fund.",
    "nav": 500000.0,
    "date_of_creation": "2024-09-29",
    "performance": 5.5
  }
]
```

Create a new Fund
- URL: /funds
- Method: POST
- Request
```json
{
    "name": "New Fund",
    "manager_name": "Manager C",
    "description": "This is a new fund",
    "nav": 500000,
    "date_of_creation": "2024-09-29",
    "performance": 3.5
}
```
- Response:
```json
{
    "message": "Fund created successfully",
    "fund_id": 3
}
```

Retrieve Fund by ID
- URL: /funds/{id}
- Method: GET
- Request
```json
{
    "fund_id": 1,
    "name": "Tech Fund 1",
    "manager_name": "Bob",
    "description": "A technology investment fund.",
    "nav": 2000.0,
    "date_of_creation": "2024-09-29",
    "performance": 1.5
}
```

Update Fund performance
- URL: /funds/{id}
- Method: PUT
- Request
```json
{
    "performance": 6
}
```
- Response:
```json
{
    "message": "Fund updated successfully"
}
```

Delete a Fund
- URL: /funds/{id}
- Method: DELETE
- Response
```json
{
    "message": "Fund deleted successfully"
}
```

## Database Schema
The system uses an SQLite database to store fund and manager data. Below is the schema used:

```sql
CREATE TABLE InvestmentFund (
    fund_id INTEGER PRIMARY KEY,
    name TEXT,
    manager_name TEXT,
    description TEXT,
    nav REAL,
    date_of_creation DATE,
    performance REAL
);
```

## Testing
You can run the test cases by executing the following command:

``` bash
python -m unittest tests.py
```
Test Coverage
1. Create a new fund with valid data
2. Create a fund with missing required fields
3. Create a fund with invalid data types
4. Retrieving a specific fund
5. Update a fund's performance
6. Update a fund with invalid performance data
7. Delete a fund
8. Retrieve a non-existent fund
9. Delete a non-existent fund
10. Update fund performance and nav



## Error Handling
The API handles the following errors:
- 400 Bad Request: Invalid input data.
- 404 Not Found: Resource not found.
- 500 Internal Server Error: Unexpected server errors.

