# Supplement Tracker

> **Note**: This application was developed in collaboration with Cody, an AI coding assistant from Sourcegraph.

A simple web application for tracking supplement intake. This MVP allows users to record, view, edit, and delete their supplement intake records.

## Features

- User Authentication: Secure login and registration system
- Record Management: Add, edit, and delete supplement intake records
- Personal Dashboard: View your supplement history in a clean, organized interface
- Responsive Design: Works seamlessly on desktop and mobile devices

## Technology Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (development)
- Authentication: Django's built-in authentication system

## Live Demo

You can access the live version of Supplement Tracker at: [your-deployment-url.com](https://your-deployment-url.com)

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

## Project Status

This project is currently in MVP (Minimum Viable Product) stage:

- **Development Status**: Early development, suitable for testing
- **Security Status**: Basic authentication implemented, but not yet audited for production use
- **Known Issues**:
  - Form validation needs improvement
  - No CSRF protection for API endpoints
  - Session management could be enhanced
  - No rate limiting implemented
  - Password reset functionality not implemented

## License

This project is licensed under the MIT License - see the LICENSE file for details.
