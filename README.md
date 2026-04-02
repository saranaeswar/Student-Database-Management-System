Student Management System

A full-stack Student Management System built with **Flask** + **MongoDB**, deployable to **Vercel**.

---

## 📁 Folder Structure

```
.
├── api/
│   ├── app.py              ← Flask backend (API routes) with Vercel handler
│   ├── templates/
│   │   └── index.html      ← Main HTML page
│   └── static/
│       ├── css/
│       │   └── style.css   ← Stylesheet
│       └── js/
│           └── main.js     ← Frontend JavaScript
├── requirements.txt        ← Python dependencies
├── vercel.json             ← Vercel deployment config
└── README.md               ← This file
```

---

## 🚀 Local Setup

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up PostgreSQL (optional for local)
For local development, you can use SQLite (default) or set up PostgreSQL.

If using PostgreSQL locally:
- Install PostgreSQL.
- Create a database.
- Set `DATABASE_URL` to your local PostgreSQL URL.

### 3. Run Flask
```bash
python api/app.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## ☁️ Deploy to Railway

### 1. Push to GitHub
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### 2. Connect to Railway
- Go to [Railway.app](https://railway.app) and sign in.
- Click "New Project" > "Deploy from GitHub repo".
- Select your `student-management-system` repo.
- Railway will auto-detect Python and deploy.

### 3. Set Up Database
- In Railway dashboard, go to your project > "Variables".
- Railway provides a `DATABASE_URL` automatically for the PostgreSQL database.
- No need to set it manually—Railway handles it.

### 4. Deploy
- Railway deploys automatically on push.
- Your app will be live with a Railway URL.

### Environment Variables
Railway sets `DATABASE_URL` automatically. If you need custom vars, add them in the Variables tab.

---

## 📋 Features

- ✅ Add new students
- ✅ View all students (filter by active/inactive)
- ✅ Update student details
- ✅ Delete students
- ✅ Responsive UI with Bootstrap

---

## 🔌 API Endpoints

| Method | Endpoint          | Description              |
|--------|-------------------|--------------------------|
| GET    | `/api/students`   | Get all students         |
| POST   | `/api/students`   | Add a new student        |
| PUT    | `/api/students/<id>` | Update a student         |
| DELETE | `/api/students/<id>` | Delete a student         |

**Query Params for GET:**
- `filter=active` → Show only active students
- `filter=all` → Show all students

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Railway
- **ORM:** SQLAlchemy
- **Styling:** Bootstrap

---

## 📝 Notes

- Uses environment variables for secure DB connection.
- Data is stored in PostgreSQL with fields: id, name, roll, phone, email, course, department, notes, status, created_at.
- For local dev, defaults to SQLite. Set `DATABASE_URL` for PostgreSQL.
- Railway provides the database automatically in production.

---

Enjoy your Student Management System! 🎓
