# PreSkool — School Management System

Django school management app 

---

## Installation

```bash
git clone https://github.com/belfaquih-farah/projet-fin-module-Python.git
cd projet-fin-module-Python

python -m venv monenv
monenv\Scripts\activate

pip install djang
python -m pip install Pillow
pip install -r requirements.txt

py manage.py makemigrations
python manage.py migrate
py manage.py createsuperuser
python manage.py seed_db
python manage.py runserver
```

Open `http://127.0.0.1:8000`

---

## Test accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | ikram@admin.com | admin123 |
| Teacher | Belfaquih@school.ma | 12345 |
| Student | saloua@school.ma | 222 |
 usually the password for both teacher and student is their ID
---

## Demo

[Watch the demo video](https://drive.google.com/drive/folders/1wvm4cHouqxHXY1xsMcS04mv2vjV9wsjG?usp=sharing)
