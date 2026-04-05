# Blog Sharing

Blog Sharing is a simple Flask CRUD application for creating, editing, listing, and deleting blog posts.

## Stack

- Flask
- SQLAlchemy
- SQLite
- Jinja2 templates

## What Changed

- No PostgreSQL setup is required.
- The app uses a local SQLite database file named `blog.db`.
- Tables are created automatically on first run.
- Sample users, categories, blogs, and comments are inserted automatically on first run.

## Requirements

- Python 3.10 or newer
- `pip`

## Quick Start

### Windows PowerShell

```powershell
cd c:\Users\yilma\repos\Blog-sharing
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Optional Configuration

By default the app stores data in `blog.db` inside the project folder. If you want to change the database path, copy `.env.example` to `.env` and set `DATABASE_URL`.

Example:

```env
DATABASE_URL=sqlite:///blog.db
```

## Resetting the Database

If you want a clean database with the sample data again:

1. Stop the app.
2. Delete `blog.db`.
3. Run `python app.py` again.

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
`-- blog_app/
    |-- __init__.py
    |-- database.py
    |-- models.py
    |-- routes.py
    |-- seed_data.py
    |-- templates/
    |   |-- index.html
    |   `-- edit.html
    `-- static/
        `-- style.css
```

## Notes

- SQLite ships with Python, so there is no separate database installation step.
- The first run creates the database automatically.
- The sample data is only inserted when the database is empty.

## License

This project is licensed under the [MIT License](MIT-License.txt).
