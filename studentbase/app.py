from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from datetime import datetime
import os
import re

app = Flask(__name__)

# MongoDB Atlas Connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://saranaeswar42_db_user:kcD43IEiBS5xq0lu@cluster0.amoyj5y.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["studentbyte"]
students_col = db["students"]

def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/students", methods=["GET"])
def get_students():
    filter_type = request.args.get("filter", "all")
    query = {"status": "active"} if filter_type == "active" else {}
    docs = [serialize(d) for d in students_col.find(query).sort("created_at", -1)]
    return jsonify(docs)

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    data["status"] = "active"
    data["created_at"] = datetime.utcnow().isoformat()
    result = students_col.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return jsonify({"success": True, "student": data}), 201

@app.route("/api/students/<id>", methods=["PUT"])
def update_student(id):
    data = request.json
    data.pop("_id", None)
    students_col.update_one({"_id": ObjectId(id)}, {"$set": data})
    updated = serialize(students_col.find_one({"_id": ObjectId(id)}))
    return jsonify({"success": True, "student": updated})

@app.route("/api/students/<id>", methods=["DELETE"])
def delete_student(id):
    students_col.delete_one({"_id": ObjectId(id)})
    return jsonify({"success": True})

@app.route("/api/dbms", methods=["POST"])
def dbms_console():
    sql = request.json.get("sql", "").strip().rstrip(";")
    sql_upper = sql.upper().strip()
    result_msg = ""
    rows = []

    try:

        # CREATE
        if sql_upper.startswith("CREATE"):
            if "students" not in db.list_collection_names():
                db.create_collection("students")
            result_msg = "✅ CREATE: Collection 'students' is ready."

        # ALTER
        elif sql_upper.startswith("ALTER"):
            parts = sql.split()
            if "ADD" in sql_upper and "COLUMN" in sql_upper:
                if len(parts) >= 6:
                    field   = parts[5]
                    default = parts[6] if len(parts) > 6 else ""
                    count   = students_col.update_many({}, {"$set": {field: default}}).modified_count
                    result_msg = f"✅ ALTER ADD COLUMN: Added field '{field}' with default '{default}' to {count} record(s)."
                else:
                    result_msg = "ℹ️ Syntax: ALTER TABLE students ADD COLUMN <fieldname> <defaultvalue>"
            elif "DROP" in sql_upper and "COLUMN" in sql_upper:
                if len(parts) >= 6:
                    field = parts[5]
                    count = students_col.update_many({}, {"$unset": {field: ""}}).modified_count
                    result_msg = f"✅ ALTER DROP COLUMN: Removed field '{field}' from {count} record(s)."
                else:
                    result_msg = "ℹ️ Syntax: ALTER TABLE students DROP COLUMN <fieldname>"
            elif "RENAME" in sql_upper and "TO" in sql_upper:
                new_name = parts[-1]
                students_col.rename(new_name)
                result_msg = f"✅ ALTER RENAME: Collection renamed to '{new_name}'."
            else:
                result_msg = (
                    "ℹ️ ALTER supported syntax:\n"
                    "  ALTER TABLE students ADD COLUMN <field> <default>\n"
                    "  ALTER TABLE students DROP COLUMN <field>\n"
                    "  ALTER TABLE students RENAME TO <newname>"
                )

        # DROP
        elif sql_upper.startswith("DROP"):
            students_col.drop()
            result_msg = "⚠️ DROP: Collection 'students' has been dropped. All records deleted."

        # TRUNCATE
        elif sql_upper.startswith("TRUNCATE"):
            count = students_col.count_documents({})
            students_col.delete_many({})
            result_msg = f"⚠️ TRUNCATE: Removed all {count} record(s). Collection still exists."

        # RENAME
        elif sql_upper.startswith("RENAME"):
            parts = sql.split()
            if len(parts) >= 4 and "TO" in sql_upper:
                new_name = parts[-1]
                students_col.rename(new_name)
                result_msg = f"✅ RENAME: Collection renamed to '{new_name}'."
            else:
                result_msg = "ℹ️ Syntax: RENAME TABLE students TO <newname>"

        # COMMENT
        elif sql_upper.startswith("COMMENT"):
            result_msg = "ℹ️ COMMENT: MongoDB does not support native table comments. Comment noted."

        # SELECT
        elif sql_upper.startswith("SELECT"):
            query = {}
            limit = 0

            limit_match = re.search(r'LIMIT\s+(\d+)', sql, re.IGNORECASE)
            if limit_match:
                limit = int(limit_match.group(1))
                sql_no_limit = sql[:limit_match.start()].strip()
            else:
                sql_no_limit = sql

            where_match = re.search(r'WHERE\s+(.+)', sql_no_limit, re.IGNORECASE)
            if where_match:
                where_part = where_match.group(1).strip()
                if "=" in where_part:
                    k, v = where_part.split("=", 1)
                    query = {k.strip(): v.strip().strip("'\"")}

            cursor = students_col.find(query)
            if limit:
                cursor = cursor.limit(limit)

            docs = [serialize(d) for d in cursor]
            rows = docs
            result_msg = f"✅ SELECT: Returned {len(docs)} record(s)."

        # INSERT
        elif sql_upper.startswith("INSERT"):
            try:
                match = re.search(r'\(([^)]+)\)\s+VALUES\s*\(([^)]+)\)', sql, re.IGNORECASE)
                if not match:
                    raise ValueError("Could not parse INSERT syntax.")
                cols = [c.strip() for c in match.group(1).split(",")]
                vals = [v.strip().strip("'\"") for v in match.group(2).split(",")]
                doc  = dict(zip(cols, vals))
                doc["status"]     = "active"
                doc["created_at"] = datetime.utcnow().isoformat()
                students_col.insert_one(doc)
                result_msg = f"✅ INSERT: 1 record inserted with fields: {', '.join(cols)}."
            except Exception as e:
                result_msg = f"❌ INSERT failed: {e}\nSyntax: INSERT INTO students (name, roll) VALUES ('John', 'CS001')"

        # UPDATE
        elif sql_upper.startswith("UPDATE"):
            try:
                query      = {}
                update_doc = {}
                set_match = re.search(r'SET\s+(.+?)(?:\s+WHERE\s+(.+))?$', sql, re.IGNORECASE)
                if not set_match:
                    raise ValueError("Could not parse UPDATE syntax.")
                set_raw   = set_match.group(1).strip()
                where_raw = set_match.group(2).strip() if set_match.group(2) else ""
                for pair in set_raw.split(","):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        update_doc[k.strip()] = v.strip().strip("'\"")
                if where_raw and "=" in where_raw:
                    k, v = where_raw.split("=", 1)
                    query = {k.strip(): v.strip().strip("'\"")}
                if not update_doc:
                    raise ValueError("No SET fields found.")
                count = students_col.update_many(query, {"$set": update_doc}).modified_count
                result_msg = f"✅ UPDATE: {count} record(s) updated."
            except Exception as e:
                result_msg = f"❌ UPDATE failed: {e}\nSyntax: UPDATE students SET name='John' WHERE roll='CS001'"

        # DELETE
        elif sql_upper.startswith("DELETE"):
            try:
                query = {}
                where_match = re.search(r'WHERE\s+(.+)', sql, re.IGNORECASE)
                if where_match:
                    where_part = where_match.group(1).strip()
                    if "=" in where_part:
                        k, v  = where_part.split("=", 1)
                        query = {k.strip(): v.strip().strip("'\"")}
                count = students_col.delete_many(query).deleted_count
                result_msg = f"✅ DELETE: {count} record(s) permanently deleted."
            except Exception as e:
                result_msg = f"❌ DELETE failed: {e}\nSyntax: DELETE FROM students WHERE roll='CS001'"

        # MERGE
        elif sql_upper.startswith("MERGE"):
            try:
                match = re.search(r'\(([^)]+)\)\s+VALUES\s*\(([^)]+)\)', sql, re.IGNORECASE)
                if not match:
                    raise ValueError("Could not parse MERGE syntax.")
                cols = [c.strip() for c in match.group(1).split(",")]
                vals = [v.strip().strip("'\"") for v in match.group(2).split(",")]
                doc  = dict(zip(cols, vals))
                doc["status"]     = "active"
                doc["created_at"] = datetime.utcnow().isoformat()
                key  = {"roll": doc.get("roll", "")}
                students_col.update_one(key, {"$set": doc}, upsert=True)
                result_msg = f"✅ MERGE: Record with roll '{doc.get('roll','')}' inserted or updated."
            except Exception as e:
                result_msg = f"❌ MERGE failed: {e}\nSyntax: MERGE INTO students (name, roll) VALUES ('John', 'CS001')"

        # GRANT
        elif sql_upper.startswith("GRANT"):
            parts = sql.split()
            priv  = parts[1] if len(parts) > 1 else "privilege"
            user  = parts[-1] if len(parts) > 3 else "user"
            result_msg = (
                f"✅ GRANT: '{priv}' privilege granted to '{user}'.\n"
                f"ℹ️ To apply in MongoDB:\n"
                f"   db.createUser({{ user: '{user}', pwd: 'password', roles: [{{ role: 'read', db: 'studentbyte' }}] }})"
            )

        # REVOKE
        elif sql_upper.startswith("REVOKE"):
            parts = sql.split()
            priv  = parts[1] if len(parts) > 1 else "privilege"
            user  = parts[-1] if len(parts) > 3 else "user"
            result_msg = (
                f"✅ REVOKE: '{priv}' privilege revoked from '{user}'.\n"
                f"ℹ️ To apply in MongoDB:\n"
                f"   db.revokeRolesFromUser('{user}', [{{ role: 'read', db: 'studentbyte' }}])"
            )

        # SHOW
        elif sql_upper.startswith("SHOW"):
            cols = db.list_collection_names()
            result_msg = f"✅ SHOW: Collections → {', '.join(cols) if cols else 'none'}"

        else:
            result_msg = (
                "❌ Unsupported command.\n\n"
                "DDL : CREATE, ALTER, DROP, TRUNCATE, RENAME, COMMENT\n"
                "DML : SELECT, INSERT, UPDATE, DELETE, MERGE\n"
                "DCL : GRANT, REVOKE"
            )

    except Exception as e:
        result_msg = f"❌ Error: {str(e)}"

    return jsonify({"message": result_msg, "rows": rows})


if __name__ == "__main__":
    app.run(debug=True)
