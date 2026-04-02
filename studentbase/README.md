# StudentByte — Student Management System

A full-stack Student Management System built with **Flask** + **MongoDB**, deployable to **Vercel**.

---

## 📁 Folder Structure

```
studentbyte/
├── app.py                  ← Flask backend (API routes)
├── requirements.txt        ← Python dependencies
├── vercel.json             ← Vercel deployment config
├── templates/
│   └── index.html          ← Main HTML page
└── static/
    ├── css/
    │   └── style.css       ← Stylesheet
    └── js/
        └── main.js         ← Frontend JavaScript
```

---

## 🚀 Local Setup

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB locally
Make sure MongoDB is running on your machine:
```bash
mongod
```
Or use [MongoDB Compass](https://www.mongodb.com/products/compass) for a GUI.

### 3. Run Flask
```bash
python app.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## ☁️ Deploy to Vercel

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/studentbyte.git
git push -u origin main
```

### 2. Connect to Vercel
- Go to [vercel.com](https://vercel.com) → New Project → Import from GitHub
- Select your repo

### 3. Add Environment Variable on Vercel
In Vercel project settings → **Environment Variables**:
```
MONGO_URI = mongodb+srv://<user>:<password>@cluster.mongodb.net/
```
Use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (free tier) for cloud MongoDB.

### 4. Deploy
Vercel will auto-detect the `vercel.json` config and deploy your Flask app.

---

## 🛠 Features

| Panel | Description |
|-------|-------------|
| **Student Registration** | Add/Edit students with name, roll, phone, email, course, department, notes |
| **Student Records** | View Active or All students, delete (soft) any record |
| **DBMS Console** | Run SQL-style commands (SELECT, DROP, TRUNCATE, CREATE, ALTER, GRANT, REVOKE) |

---

## 📦 Tech Stack

- **Backend**: Python + Flask
- **Database**: MongoDB (via PyMongo)
- **Frontend**: Vanilla HTML + CSS + JavaScript
- **Deployment**: Vercel
