from flask import Flask,render_template,request,redirect,session
import sqlite3
app=Flask(__name__)
app.secret_key="secret"
def get_db():
    return sqlite3.connect("database.db")
@app.route("/")
def home():
    db=get_db()
    posts=db.execute("""
    SELECT posts.id,posts.content,posts.created_at,users.username,posts.user_id
    FROM posts
    JOIN users ON posts.user_id=users.id
    ORDER BY posts.created_at DESC
    """).fetchall()
    db.close()
    return render_template("index.html",posts=posts)
@app.route("/delete/<int:post_id>",methods=["POST"])
def delete(post_id):
    db=get_db()
    db.execute(
        "DELETE FROM posts WHERE id=? AND user_id=?",
        (post_id,session["user_id"])
    )
    db.commit()
    db.close()
    return redirect("/")
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        db=get_db()
        db.execute(
            "INSERT INTO users(username,password)VALUES(?,?)",
            (username,password)
        )
        db.commit()
        db.close()
        return redirect("/login")
    return render_template("register.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        db=get_db()
        user=db.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username,password)
        ).fetchone()
        db.close()
        if user:
            session["user_id"]=user[0]
            return redirect("/")
    return render_template("login.html")
@app.route("/post",methods=["POST"])
def post():
    if "user_id" not in session:
        return redirect("/login")
    text=request.form["content"]
    db=get_db()
    db.execute(
        "INSERT INTO posts(content,user_id)VALUES(?,?)",
        (text,session["user_id"])
    )
    db.commit()
    db.close()
    return redirect("/")
app.run(debug=True)