# Student-DataBase — Student Management System

A full-stack Student Management System built with **Flask** + **MongoDB Atlas**, deployed on **Vercel** and **Render**.

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

\```bash
pip install -r requirements.txt
\```

### 2. Run Flask

\```bash
python app.py
\```

Open your browser at: **http://127.0.0.1:5000**

---

## ☁️ Deploy to Vercel

### 1. Push to GitHub

\```bash
git add .
git commit -m "your message"
git push origin main
\```

### 2. Connect to Vercel

- Go to [vercel.com](https://vercel.com) and sign in with GitHub
- Click **Add New Project**
- Select your repository and click **Import**

### 3. Add Environment Variable

| Key | Value |
|-----|-------|
| `MONGO_URI` | your MongoDB Atlas connection string |

### 4. Deploy

- Click **Deploy**
- Vercel gives you a live link instantly!

🌐 **Live URL:** https://student-database-management-system-two.vercel.app/

## 📋 Features

- ✅ Register new students with full details
- ✅ View all students (Active / All tabs)
- ✅ Edit and update student records
- ✅ Delete students permanently
- ✅ Built-in DBMS Console (DDL, DML, DCL commands)
- ✅ SQL Syntax Sidebar Cheatsheet with auto-fill
- ✅ Auto-refresh after write operations

---

## 🖥️ DBMS Console Commands

| Category | Commands |
|----------|----------|
| **DDL** | CREATE, ALTER, DROP, TRUNCATE, RENAME, COMMENT |
| **DML** | SELECT, INSERT, UPDATE, DELETE, MERGE |
| **DCL** | GRANT, REVOKE |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students` | Get all students |
| POST | `/api/students` | Add a new student |
| PUT | `/api/students/<id>` | Update a student |
| DELETE | `/api/students/<id>` | Delete a student |
| POST | `/api/sql` | Run SQL commands |

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** MongoDB Atlas
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render / Vercel

---

## 📝 Notes

- MongoDB Atlas must have `0.0.0.0/0` in Network Access for cloud deployment
- Set `MONGO_URI` as an environment variable in Render
- Data is stored in MongoDB with fields: name, roll, phone, email, course, department, notes, status, created_at

---

Developed by **Saranaeswar** | CSBS (Batch 2024–2028) 🎓
