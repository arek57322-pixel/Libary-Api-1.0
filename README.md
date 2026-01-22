
Практика Keepsolid 2026

---

## Функціонал

### Авторизація
- `POST /auth/register` — реєстрація
- `POST /auth/login` — логін (JWT)

### Користувач
- `GET /users/me` — дані поточного користувача (потрібен токен)

### Книги
- `GET /books/` — список книг (без логіну)
- `GET /books/{book_id}` — книга по id (без логіну)
- `POST /books/` — додати книгу (admin)
- `DELETE /books/{book_id}` — видалити книгу (admin)
- `GET /books/export/csv` — експорт CSV (admin)

### Favorites
- `GET /favorites/` — мої favorites (логін)
- `POST /favorites/{book_id}` — додати в favorites (логін)
- `DELETE /favorites/{book_id}` — видалити з favorites (логін)

---

## Встановлення

```bash
git clone https://github.com/arek57322-pixel/Libary-Api-1.0.git
cd Libary-Api-1.0
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

## SQL
CREATE DATABASE library_db; 

postgresql://library_user:library_pass@localhost:5432/library_db
uvicorn app.main:app --reload

## Змiна ролi
python -m app.cli set-role --email test@mail.com --role admin
python -m app.cli set-role --email test@mail.com --role client





