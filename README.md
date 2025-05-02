# 📦 Receipt Processor API – Setup & Run Instructions (Dockerized Django)

These instructions will help you clone, build, and run the Fetch Rewards receipt processor API challenge using Docker and Django.

---

## ✅ 1. Prerequisites

Make sure you have the following installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop)

---

## 📁 2. Project Structure (Key Files)

```
receipt_processor/
├── core/                  # Django project folder
├── receipts/              # Django app (API logic)
├── manage.py
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker build instructions
├── docker-compose.yml     # Compose setup for running container
├── pytest.ini             # Pytest config
└── db.sqlite3             # Local SQLite DB (auto-generated)
```

---

## 🐳 3. Run the App with Docker

### Step A: Clone the repository

```bash
git clone https://github.com/ArchieJude/receipt-processor.git
cd receipt_processor
```

### Step B: Build and start the container

```bash
docker compose up --build
```

- This builds the image and starts the Django dev server at **http://localhost:8000/**

---

## 🌐 4. Access the API

Visit: [http://localhost:8000/receipts/process](http://localhost:8000/receipts/process)


You can use the DRF browsable interface or tools like Postman/cURL.

---

## 🧪 5. Running Tests

Run the full test suite:

```bash
docker compose run web pytest
```

---

## 🛠 6. API Endpoints

### POST `/receipts/process`
- Accepts receipt JSON
- Returns: `{ "id": "<uuid>" }`

**Example:**
```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },
    { "shortDescription": "Emils Cheese Pizza", "price": "12.25" }
  ],
  "total": "18.74"
}
```

### GET `/receipts/{id}/points`
- Returns: `{ "points": 28 }`
- Returns 404 if ID not found

---

## ⚠️ 7. Troubleshooting

- **DisallowedHost Error:**
  - Edit `core/settings.py`: 
    ```python
    ALLOWED_HOSTS = ["0.0.0.0", "localhost", "127.0.0.1"]
    ```

- **docker-compose not found:**
  - Use the newer command:
    ```bash
    docker compose up
    ```

---

## 🔧 8. Development Notes

- Uses in-memory receipt store (no database persistence)
- Built with:
  - Django 4.2.x
  - Django REST Framework 3.16.0
  - Python 3.9
- Matches Fetch Rewards [API Spec](https://github.com/fetch-rewards/receipt-processor-challenge/blob/main/api.yml)


