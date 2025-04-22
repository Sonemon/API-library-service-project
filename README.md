# Library service API

This service was created to consolidate knowledge on DRF, Docker, as well as to get new ones, such as binding a telegram bot for notifications about actions inside the service. In the future it is planned to add requirements and try to work with payments.

## 🚀 Features

- JWT authentication
- Admin vs Read-Only permissions
- Swagger API documentation
- Custom validations
- PostgreSQL with persistent volume
- Dockerized deployment

## 🛠️ Technology Stack

- Python 3.12
- Django & Django REST Framework
- PostgreSQL 16
- Docker & Docker Compose
- JWT (via SimpleJWT)
- Telegram Bot support

---

## 📦 How to Run the Project with Docker Compose
### 0. Python and Docker must be installed.
### 1. Clone the Repository

```bash
git clone https://github.com/Sonemon/API-library-service-project
```

### 2. Create .env file from .env-sample (You'll need to create a Telegram bot via @botFather and a channel to add it to and give it admin privileges)

### 3. Build and Run
```bash
docker-compose up --build
```
### Docker Compose will:
- Build the Django app image
- Start PostgreSQL
- Wait until the database is ready
- Run migrations
- Start the Django development server

### 4. Create Superuser 👤
After running the containers, open a new terminal and run:
```bash
docker-compose exec app python manage.py createsuperuser
```
Then follow the prompts to set up your admin account.

## 📚 API Documentation
Swagger documentation is available at:
```html
http://localhost:8001/api/swagger
```
## 💾 Database Persistence
PostgreSQL data is stored in a Docker volume named lib_db. This means your data will persist across container restarts.