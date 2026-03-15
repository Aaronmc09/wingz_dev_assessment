# Wingz Dev Assessment

A RESTful API built with Django REST Framework for managing ride information.

## Prerequisites

- Python 3.10+

## Setup

1. **Clone the repository**

```bash
git clone git@github.com:Aaronmc09/wingz_dev_assessment.git
cd wingz_dev_assessment
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py migrate
```

5. **Load sample data**

```bash
python manage.py loaddata sample_data
```

6. **Run the development server**

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## Test Credentials

After loading the sample data, you can authenticate with:

| Email | Password | Role |
|---|---|---|
| `chris@example.com` | `password123` | admin |

Only users with the `admin` role can access the API endpoints.

## Authentication

The API uses JWT authentication. To obtain a token:

```
POST /api/token/
Content-Type: application/json

{
  "email": "chris@example.com",
  "password": "password123"
}
```

Include the access token in subsequent requests:

```
Authorization: Bearer <access_token>
```

To refresh an expired token:

```
POST /api/token/refresh/

{
  "refresh": "<refresh_token>"
}
```

## API Endpoints

### Rides

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/rides/` | List rides with pagination |

**Query Parameters:**

| Parameter | Description | Example |
|---|---|---|
| `status` | Filter by ride status | `?status=dropoff` |
| `rider_email` | Filter by rider's email | `?rider_email=randy@example.com` |
| `sort_by` | Sort by `pickup_time` or `distance` | `?sort_by=pickup_time` |
| `order` | Sort order: `asc` (default) or `desc` | `?order=desc` |
| `latitude` | Required when `sort_by=distance` | `?latitude=37.78` |
| `longitude` | Required when `sort_by=distance` | `?longitude=-122.42` |

**Example:**

```
GET /api/rides/?status=dropoff&sort_by=pickup_time&order=desc
```

## API Collections

Pre-configured API collection files are available in the `docs/` folder for convenient testing:

- **Bruno** — import the collection into [Bruno](https://www.usebruno.com/)
- **Postman** — import the collection into [Postman](https://www.postman.com/)

## Design Decisions

### Cursor Pagination

The API uses `CursorPagination` instead of the more common `PageNumberPagination`. Cursor pagination uses keyset-based navigation rather than SQL `OFFSET`, which means consistent performance regardless of how deep into the results you paginate. The trade-off is that clients can only navigate forward/backward, not jump to arbitrary pages.

### Distance Sorting

When sorting by distance, the API computes Euclidean distance at the database level using an annotation. A bounding-box pre-filter (~0.5 degrees / ~55km) narrows down candidate rows before computing distances, allowing the database to use indexes on latitude/longitude columns rather than scanning the full table.

## Bonus SQL

For reporting purposes, the following raw SQL returns the count of trips that took more than 1 hour from Pickup to Dropoff, grouped by month and driver:

```sql
SELECT
    strftime('%Y-%m', pickup_event.created_at) AS month,
    u.first_name || ' ' || u.last_name AS driver,
    COUNT(*) AS "count_of_trips_gt_1hr"
FROM rides_ride r
JOIN users_user u ON u.id_user = r.id_driver_id
JOIN rides_rideevent pickup_event
    ON pickup_event.id_ride = r.id_ride
    AND pickup_event.description = 'Status changed to pickup'
JOIN rides_rideevent dropoff_event
    ON dropoff_event.id_ride = r.id_ride
    AND dropoff_event.description = 'Status changed to dropoff'
WHERE (julianday(dropoff_event.created_at) - julianday(pickup_event.created_at)) * 24 > 1
GROUP BY month, driver
ORDER BY month, driver;
```

> **Note:** This query uses SQLite functions (`strftime`, `julianday`). For PostgreSQL, replace `strftime('%Y-%m', ...)` with `to_char(..., 'YYYY-MM')` and the time difference with `EXTRACT(EPOCH FROM dropoff_event.created_at - pickup_event.created_at) / 3600 > 1`.
