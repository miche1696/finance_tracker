# Finance Tracker

A comprehensive Django-based web application for tracking personal finances and expenses with advanced filtering, visualization, and calendar views.

## Features

### Core Functionality
- **Expense Tracking**: Add, view, and manage personal expenses
- **User Authentication**: Secure login/logout system with protected views
- **Data Filtering**: Advanced filtering by date range, category, and amount
- **Visual Analytics**: Interactive charts showing expenses by category
- **Calendar View**: Monthly calendar display with daily expense totals
- **Responsive Design**: Bootstrap-based UI that works on all devices

### Expense Management
- **Expense Categories**: Organize expenses by custom categories
- **Subcategories**: Further organize expenses with subcategories
- **Vendor Tracking**: Record store/vendor information for each expense
- **Amount Tracking**: Precise decimal-based amount tracking
- **Date Management**: Full date tracking for all expenses
- **Notes**: Optional notes field for additional details

### Advanced Features
- **Smart Filtering**: Filter expenses by:
  - Date ranges (from/to dates)
  - Category (case-insensitive partial matching)
  - Amount ranges (minimum/maximum amounts)
- **Data Visualization**: 
  - Bar charts showing total expenses by category
  - JSON API endpoints for chart data
- **Calendar Integration**: 
  - Monthly calendar view with daily expense totals
  - Navigation between months
  - Visual representation of spending patterns

### Data Management
- **Import System**: Management command for importing expenses from external sources
- **Data Export**: Built-in support for data export and reporting
- **Database Optimization**: Efficient queries with proper indexing

## Technology Stack

- **Backend**: Django 5.2.4 (Python)
- **Database**: SQLite (development), PostgreSQL ready (production)
- **Frontend**: Django Templates with Bootstrap 5
- **Charts**: Chart.js for data visualization
- **Filtering**: django-filter for advanced filtering
- **Authentication**: Django's built-in authentication system

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/miche1696/finance_tracker.git
cd finance_tracker
```

2. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Open your browser and navigate to `http://127.0.0.1:8000/`

### First Steps

1. **Login**: Navigate to `/login/` to access the application
2. **Add Expenses**: Use the "Add" link to create your first expense
3. **View List**: See all expenses with filtering options
4. **Explore Charts**: View spending patterns by category
5. **Check Calendar**: See daily expense totals in calendar format

## Project Structure

```
finance_tracker/
├── finance_tracker/          # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   ├── asgi.py
│   └── wsgi.py
├── expenses/                # Main expenses app
│   ├── __init__.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py
│   ├── models.py            # Expense model definition
│   ├── views.py             # View classes and functions
│   ├── urls.py              # App URL routing
│   ├── filters.py           # Expense filtering
│   ├── utils.py             # Calendar utility functions
│   ├── management/          # Custom management commands
│   │   └── commands/
│   │       └── import_expenses.py
│   ├── migrations/          # Database migrations
│   └── templates/           # HTML templates
│       └── expenses/
│           ├── base.html    # Base template with navigation
│           ├── expense_list.html    # Expense list with filters
│           ├── expense_form.html    # Add/edit expense form
│           ├── chart.html           # Chart visualization
│           └── calendar.html        # Calendar view
├── templates/               # Project-level templates
│   └── registration/
│       └── login.html       # Login template
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Endpoints

### Authentication
- `GET/POST /login/` - User login
- `GET /logout/` - User logout

### Expenses
- `GET /expenses/` - List all expenses with filtering
- `GET /expenses/add/` - Add new expense form
- `POST /expenses/add/` - Create new expense
- `GET /expenses/chart/` - Chart visualization page
- `GET /expenses/chart-data/` - JSON data for charts
- `GET /expenses/calendar/` - Calendar view
- `GET /expenses/calendar/?year=2024&month=3` - Specific month calendar

## Usage Examples

### Filtering Expenses
- Filter by date range: Add date parameters to the list view
- Filter by category: Use the category filter with partial matching
- Filter by amount: Set minimum and maximum amount ranges

### Calendar Navigation
- Navigate between months using URL parameters
- Example: `/expenses/calendar/?year=2024&month=3` for March 2024
- View daily expense totals directly in the calendar

### Chart Visualization
- View spending patterns by category
- Interactive bar charts with Chart.js
- Real-time data from the database

## Development

### Adding New Features
1. Create new models in `expenses/models.py`
2. Add views in `expenses/views.py`
3. Update URL patterns in `expenses/urls.py`
4. Create templates in `expenses/templates/expenses/`
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Custom Management Commands
The project includes a custom management command for importing expenses:
```bash
python manage.py import_expenses
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Michele** - [miche1696](https://github.com/miche1696)

## Acknowledgments

- Django framework and community
- Bootstrap for responsive design
- Chart.js for data visualization
- django-filter for advanced filtering capabilities
