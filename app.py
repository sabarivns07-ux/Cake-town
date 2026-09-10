
from flask import Flask, request, jsonify, render_template, session
import sqlite3, os, time

app = Flask(__name__)
app.secret_key = "cake-town-stage7-demo-key"
DB = "cake_town.db"

ADMIN_USER = "Cake Town"
ADMIN_PASS = "mohan"

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con=db()
    con.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_no TEXT, customer_name TEXT, phone TEXT,
        items TEXT, total REAL, status TEXT DEFAULT 'NEW',
        created_at REAL
    )""")
    con.commit(); con.close()

@app.route("/")
def customer():
    return render_template("customer.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.post("/api/admin/login")
def login():
    data=request.get_json() or {}
    if data.get("username")==ADMIN_USER and data.get("password")==ADMIN_PASS:
        session["admin"]=True
        return jsonify(ok=True)
    return jsonify(ok=False, error="Invalid username or password"),401

@app.post("/api/admin/logout")
def logout():
    session.clear()
    return jsonify(ok=True)

@app.get("/api/admin/check")
def check():
    return jsonify(logged_in=bool(session.get("admin")))

@app.post("/api/orders")
def create_order():
    data=request.get_json() or {}
    required=["table_no","customer_name","phone","items","total"]
    if not all(data.get(k) for k in required):
        return jsonify(error="Please fill all order details"),400
    con=db()
    cur=con.execute("""INSERT INTO orders
        (table_no,customer_name,phone,items,total,status,created_at)
        VALUES(?,?,?,?,?,'NEW',?)""",
        (data["table_no"],data["customer_name"],data["phone"],
         data["items"],float(data["total"]),time.time()))
    con.commit(); oid=cur.lastrowid; con.close()
    return jsonify(ok=True, order_id=oid)

@app.get("/api/orders")
def orders():
    if not session.get("admin"):
        return jsonify(error="Login required"),401
    con=db(); rows=con.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])

@app.get("/api/orders/<int:oid>")
def order_status(oid):
    con=db(); r=con.execute("SELECT * FROM orders WHERE id=?",(oid,)).fetchone()
    con.close()
    if not r: return jsonify(error="Order not found"),404
    return jsonify(dict(r))

@app.post("/api/orders/<int:oid>/status")
def update_status(oid):
    if not session.get("admin"):
        return jsonify(error="Login required"),401
    status=(request.get_json() or {}).get("status")
    allowed={"NEW","ACCEPTED","PREPARING","READY","DELIVERED","CANCELLED"}
    if status not in allowed: return jsonify(error="Invalid status"),400
    con=db(); con.execute("UPDATE orders SET status=? WHERE id=?",(status,oid))
    con.commit(); con.close()
    return jsonify(ok=True)

init_db()
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
