**🏦 Full-Stack Banking App**

A banking application built with FastAPI, SQLAlchemy, MySQL, HTMX, and TailwindCSS.
This project demonstrates how to design and build a real-world full-stack system — covering authentication, accounts, transactions, and a modern frontend experience without heavy JavaScript frameworks.


---------------------------------------------------------------------
**Features**

🔐 Authentication: Register, login, JWT-based sessions

👤 User Management: Create and manage users

💳 Accounts: Create accounts, check balances

💸 Transactions: Deposit, withdraw, transfer money

📊 Dashboard: User-specific view of accounts and recent activity

🎨 Frontend: HTMX + TailwindCSS for modern, interactive UI

🗄️ Database: MySQL with SQLAlchemy ORM

🛠️ Tech Stack


----------------------------------------------------------------------
Backend → FastAPI, SQLAlchemy, Pydantic

Frontend → HTMX, TailwindCSS, Jinja2 templates

Database → MySQL

Auth → JWT (JSON Web Tokens), OAuth2

Server → Uvicorn


-----------------------------------------------------------------------
📂 Project Structure
app/
 ├── api/         # Routers: auth, users, accounts, transactions, pages
 ├── core/        # Security, database setup
 ├── models/      # SQLAlchemy models
 ├── schemas/     # Pydantic schemas
 ├── templates/   # Jinja2 + HTMX templates
 ├── static/      # CSS/JS files
 └── main.py      # Application entry point


------------------------------------------------------------------------
**🚀 Getting Started**
1. Clone the repo
git clone https://github.com/Vamshireddy495/banking_rep
cd banking-app

2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Setup database

Create a MySQL database (e.g., banking_app).

Update your DB URL in app/core/database.py.

5. Run migrations / create tables
python create_tables.py

6. Start the server
uvicorn app.main:app --reload

7. Visit the app

---------------------------------------------------------------------
**The best way to test your api's is by using swagger.**
Swagger Docs: http://127.0.0.1:8000/docs


**Contribution**

Feel free to fork, raise issues, or submit PRs. Suggestions and improvements are always welcome!
