# FastAPI Authentication

A modern, secure FastAPI application featuring JWT-based authentication, user management, and a product management system. Built with PostgreSQL, SQLAlchemy, and includes rate limiting for enhanced security.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication with configurable expiration
- 👥 **User Management** - User registration and authentication endpoints
- 📦 **Product Management** - CRUD operations for user-owned products
- 🛡️ **Rate Limiting** - Built-in rate limiting to prevent abuse
- 🐳 **Docker Support** - Complete containerization with Docker Compose
- 📊 **PostgreSQL Database** - Robust relational database with SQLAlchemy ORM
- ⚡ **Modern Python** - Built with Python 3.13+ and latest FastAPI features

## Prerequisites

- **Python**: 3.13 or higher
- **uv**: Modern Python package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Docker & Docker Compose**: For containerized deployment
- **PostgreSQL**: 17+ (if running without Docker)

## Installation

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd fastapi-authentication
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and configure the required variables:

   ```env
   # Generate a secure secret key
   SECRET_KEY=your-super-secret-key-here
   POSTGRES_PASSWORD=your-secure-password
   ```

3. **Start the application**

   ```bash
   docker-compose up --build
   ```

The application will be available at `http://localhost:8000`

### Option 2: Development with Docker Compose Watch

For active development with hot reloading and file watching:

1. **Clone and setup**

   ```bash
   git clone <repository-url>
   cd fastapi-authentication
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start development environment with file watching**

   ```bash
   # Using Docker Compose watch (recommended for development)
   docker compose watch

   # Or using the development helper scripts:
   # Windows PowerShell:
   .\dev.ps1 watch

   # Linux/macOS:
   ./dev.sh watch
   ```

The development setup includes:

- **Hot reloading** - Code changes trigger automatic server restart
- **File watching** - Changes sync immediately to the container
- **Development tools** - Optional pgAdmin and Adminer for database management
- **Enhanced logging** - Better debugging output

### Option 3: Local Development

1. **Clone and setup**

   ```bash
   git clone <repository-url>
   cd fastapi-authentication
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Set up PostgreSQL database**
   - Install PostgreSQL 17+
   - Create a database
   - Update `.env` with your database credentials

4. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**

   ```bash
   uv run fastapi dev app/main.py
   ```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `APP_NAME` | Application name | "FastAPI Authentication" | ✅ |
| `SECRET_KEY` | JWT signing key | Auto-generated | ✅ |
| `ALGORITHM` | JWT algorithm | HS256 | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | 15 | ❌ |
| `POSTGRES_HOST` | Database host | postgres | ✅ |
| `POSTGRES_PORT` | Database port | 5432 | ❌ |
| `POSTGRES_USER` | Database user | postgres | ✅ |
| `POSTGRES_PASSWORD` | Database password | - | ✅ |
| `POSTGRES_DB` | Database name | mydatabase | ✅ |

### Generating a Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## API Documentation

Once the application is running, you can access:

- **Interactive API Docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Docs (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token (rate limited: 3/minute)

### Users

- `GET /users/` - List all users (public)
- `POST /users/` - Create a new user (public)
- `GET /users/{user_id}` - Get specific user (public)
- `PUT /users/{user_id}` - Update user information (protected - self only)
- `DELETE /users/{user_id}` - Delete user account (protected - self only)

### Products (Protected)

- `GET /products/` - List user's products
- `POST /products/` - Create a new product
- `GET /products/{id}` - Get specific product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

## Authentication Flow

1. **Register a new user**

   ```bash
   curl -X POST "http://localhost:8000/auth/register" \
        -H "Content-Type: application/json" \
        -d '{"username": "testuser", "passowrd": "testpass123"}'
   ```

2. **Login to get access token**

   ```bash
   curl -X POST "http://localhost:8000/auth/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=testuser&password=testpass123"
   ```

3. **Use token for protected endpoints**

   ```bash
   curl -X GET "http://localhost:8000/products/" \
        -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

4. **User management examples**

   ```bash
   # Create a new user
   curl -X POST "http://localhost:8000/users/" \
        -H "Content-Type: application/json" \
        -d '{"username": "newuser", "password": "securepass123"}'

   # Get all users
   curl -X GET "http://localhost:8000/users/"

   # Update your own user information (requires authentication)
   curl -X PUT "http://localhost:8000/users/{your_user_id}" \
        -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"username": "updatedname"}'
   ```

## Project Structure

```md
fastapi-authentication/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and settings
│   ├── database.py          # Database connection and setup
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py          # API router configuration
│   │   ├── dependencies.py  # Shared dependencies (auth, database)
│   │   └── routes/
│   │       ├── auth.py      # Authentication endpoints
│   │       ├── users.py     # User management endpoints
│   │       └── products.py  # Product management endpoints
│   └── services/
│       └── auth.py          # Authentication business logic
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── pyproject.toml          # Python project configuration
├── uv.lock                 # Dependency lock file
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Development

### Development Helper Scripts

The project includes helper scripts to streamline development workflow:

**Windows (PowerShell):**

```powershell
.\dev.ps1 up          # Start development environment
.\dev.ps1 watch       # Start with file watching (hot reload)
.\dev.ps1 down        # Stop all services
.\dev.ps1 logs        # Show service logs
.\dev.ps1 shell       # Open shell in backend container
.\dev.ps1 db          # Open PostgreSQL shell
.\dev.ps1 tools       # Start with database admin tools
.\dev.ps1 clean       # Clean up containers and volumes
```

**Linux/macOS (Bash):**

```bash
./dev.sh up          # Start development environment
./dev.sh watch       # Start with file watching (hot reload)
./dev.sh down        # Stop all services
./dev.sh logs        # Show service logs
./dev.sh shell       # Open shell in backend container
./dev.sh db          # Open PostgreSQL shell
./dev.sh tools       # Start with database admin tools
./dev.sh clean       # Clean up containers and volumes
```

### Database Administration Tools

When using the `tools` profile, you get access to:

- **pgAdmin**: `http://localhost:5050` (<admin@example.com> / admin)
- **Adminer**: `http://localhost:8080` (lightweight database admin)

Start with tools:

```bash
docker compose --profile tools up
# or
.\dev.ps1 tools  # Windows
./dev.sh tools   # Linux/macOS
```

### File Watching and Hot Reload

The development setup supports Docker Compose watch for automatic reloading:

```bash
# Start with file watching
docker compose watch

# Changes to these trigger different actions:
# - ./app/* files -> sync to container (immediate)
# - pyproject.toml -> rebuild container
# - uv.lock -> rebuild container
# - Dockerfile -> rebuild container
```

### Running Tests

```bash
# In development container
docker compose exec backend python -m pytest

# Or using helper script
.\dev.ps1 test  # Windows
./dev.sh test   # Linux/macOS

# Local testing (if dependencies installed)
uv add --dev pytest pytest-asyncio httpx
uv run pytest
```

### Code Formatting

```bash
# In development container
docker compose exec backend black app/
docker compose exec backend isort app/

# Or using helper script
.\dev.ps1 format  # Windows
./dev.sh format   # Linux/macOS

# Local formatting (if tools installed)
uv add --dev black isort
uv run black .
uv run isort .
```

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Rate Limiting**: Protection against brute force attacks
- **Input Validation**: Pydantic schemas for request validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://localhost:8000/docs) when running locally
2. Review the [Issues](../../issues) section
3. Create a new issue with detailed information about your problem

---

**Built with ❤️ using FastAPI, SQLAlchemy, and PostgreSQL**
