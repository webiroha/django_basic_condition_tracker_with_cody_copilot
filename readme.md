# Supplement Tracker

> **Note**: This application was developed in collaboration with Cody, an AI coding assistant from Sourcegraph and GitHub Copilot. (Cody designed UI/UX)

A simple web application for tracking supplement intake. This MVP allows users to record, view, edit, and delete their supplement intake records.

## Features

- User Authentication: Secure login and registration system
- Record Management: Add, edit, and delete supplement intake records
- Personal Dashboard: View your supplement history in a clean, organized interface
- Responsive Design: Works seamlessly on desktop and mobile devices

## Technology Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Cache: File-based (Production), Memcached (Development)
- Authentication: Django's built-in authentication system

## Live Demo

You can access the live version of Supplement Tracker at: [webiroha.pythonanywhere.com](https://webiroha.pythonanywhere.com/)

## Getting Started

### Prerequisites

- Python 3.8+
- pip or poetry

### Installation

1. Clone the repository

```
git clone git@github.com:webiroha/django-basic-condition-tracker-with-cody.git
cd django-basic-condition-tracker-with-cody
```

2. Install dependencies

```
## Using pip
pip install -r requirements.txt

# Using poetry
poetry install
```

3. Create and configure `.env` file

```bash
# Create .env file
touch .env
chmod 600 .env

# Add required environment variables
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app
```

4. Run migrations

```
python manage.py migrate
```

5. Start the development server

```

python manage.py runserver

```

6. Visit http://127.0.0.1:8000/ in your browser

## Deployment

This project is configured for deployment on PythonAnywhere

## Usage

1. Register for a new account or login with existing credentials
2. Add supplement intake records with name, date/time, and amount
3. View your history of supplement intake
4. Edit or delete records as needed

## Project Status

This MVP (Minimum Viable Product) is a portfolio project using SQLite as the database. While SQLite is not recommended for large-scale production applications, it is perfectly suitable for this demonstration project that showcases:

Current features implemented:

- ✅ User authentication
- ✅ Rate limiting
- ✅ Security headers
- ✅ File-based caching
- ✅ Custom error pages
- ✅ Environment variable validation
- ✅ Content Security Policy
- ✅ Permissions Policy

### Security Features

- Rate limiting implemented
- CSRF protection enabled
- PBKDF2 password hashing
- Security headers configured
- Environment variable validation
- Custom error pages
- Basic logging system

## License

This project is licensed under the MIT License - see the LICENSE file for details.
