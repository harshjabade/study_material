# 📚 StudyHub - Online Study Material Sharing System

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://study-material-p123.onrender.com/)
[![Django](https://img.shields.io/badge/Framework-Django-092e20)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**StudyHub** is a clean, modern, and powerful web application designed for students and educators to share, download, and organize study materials seamlessly. Built with Django and modern web technologies, it offers a premium user experience for academic collaboration.

## 🚀 Live Demo
Access the live application here: **[study-material-p123.onrender.com](https://study-material-p123.onrender.com/)**

---

## ✨ Features

- **📂 Material Management**: Upload, view, and download study materials across various subjects.
- **🔍 Smart Categories**: Organize notes by categories (ML, Networks, DBMS, etc.).
- **🔥 Popular Content**: Highlighting trending and most downloaded study materials.
- **💬 Community Interaction**: Rate and track downloads for materials.
- **🔐 Secure Authentication**: Full user registration and login system.
- **📱 Responsive Design**: Fully optimized for mobile, tablet, and desktop viewing.
- **🎨 Premium UI**: Modern dark-themed glassmorphism aesthetic.

---

## 🛠️ Tech Stack

- **Backend**: Python, Django 5.2+
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
- **Database**: PostgreSQL (Production), SQLite/MySQL (Development)
- **Deployment**: Render, Gunicorn, WhiteNoise
- **Version Control**: Git & GitHub

---

## 💻 Local Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/harshjabade/study_material.git
   cd study_material
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables:**
   Create a `.env` file in the root directory (based on `.env.example`):
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the server:**
   ```bash
   python manage.py runserver
   ```

Access the site at `http://127.0.0.1:8000/`.

---

## ☁️ Deployment

This project is optimized for deployment on **Render** or **Railway**.

### Deployment Checklist:
- Ensure `ALLOWED_HOSTS` includes your domain in `settings.py`.
- `DEBUG` should be set to `False` in production.
- Use `WhiteNoise` (configured) for serving static files.
- Configuration files included: `Procfile`, `runtime.txt`, `build.sh`.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed with ❤️ by [Harsh Jabade](https://github.com/harshjabade)**
