# Supplement Tracker

A simple web application for tracking supplement intake. This MVP allows users to record, view, edit, and delete their supplement intake records.

## Features

- User Authentication: Secure login and registration system
- Record Management: Add, edit, and delete supplement intake records
- Personal Dashboard: View your supplement history in a clean, organized interface
- Responsive Design: Works seamlessly on desktop and mobile devices

## Technology Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (development), PostgreSQL (production-ready)
- Authentication: Django's built-in authentication system

## Getting Started

### Prerequisites

- Python 3.8+
- pip or poetry

### Installation

1. Clone the repository

```
git clone https://github.com/yourusername/supplement-tracker.git
cd supplement-tracker
```

2. Install dependencies

```
## Using pip
pip install -r requirements.txt

# Using poetry
poetry install
```

3. Run migrations

```
python manage.py migrate
```

4. Start the development server

```
python manage.py runserver
```

5. Visit http://127.0.0.1:8000/ in your browser

## Usage

1. Register for a new account or login with existing credentials
2. Add supplement intake records with name, date/time, and amount
3. View your history of supplement intake
4. Edit or delete records as needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.
