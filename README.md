# Django Blog Application

A clean and beginner-friendly **Django Blog Application** built as a learning and portfolio project. This project demonstrates core Django concepts such as project structure, apps, models, views, templates, authentication, and GitHub version control.

---

## 🚀 Features

* User authentication (login & logout)
* Create, read, update, and delete blog posts (CRUD)
* Admin panel for content management
* Media upload support
* Template-based UI using Django templates
* Clean project structure with virtual environment support

---

## 🛠 Tech Stack

* **Backend:** Python, Django
* **Database:** SQLite (development)
* **Frontend:** HTML, CSS
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
myapp/
│── blog/          # Blog application
│── myapp/         # Project configuration
│── templates/     # HTML templates
│── media/         # Media files (ignored in Git)
│── manage.py
│── requirements.txt
│── .gitignore
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Dharaniga23/django-blog-app.git
cd django-blog-app
```

### 2️⃣ Create & activate virtual environment

```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations

```bash
python manage.py migrate
```

### 5️⃣ Run the development server

```bash
python manage.py runserver
```

Open browser and visit:

```
http://127.0.0.1:8000/
```

---

## 🔐 Admin Access (Optional)

Create a superuser to access Django admin:

```bash
python manage.py createsuperuser
```

Then visit:

```
http://127.0.0.1:8000/admin/
```

---

## 📌 Learning Outcomes

* Understood Django project & app architecture
* Implemented CRUD functionality
* Used virtual environments and dependency management
* Applied Git and GitHub for version control
* Followed best practices like `.gitignore` and `requirements.txt`

---

## 👩‍💻 Author

**Dharaniga S**
Aspiring Python & Django Developer

---

## 📄 License

This project is for educational purposes.
