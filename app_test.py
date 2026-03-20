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
    SELECT posts.id,posts.content,posts.created_at,users.username,posts.user_id,posts.likes
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
        if not user:
            return redirect("/register")
    return render_template("login.html")
@app.route("/like/<int:post_id>",methods=["POST"])
def like(post_id):
    if "user_id" not in session:
        return redirect("/register")
    user_id=session["user_id"]
    db=get_db()
    existing=db.execute(
        "SELECT * FROM likes WHERE user_id=? AND post_id=?",
        (user_id,post_id)
    ).fetchone()
    if existing:
        db.execute(
            "DELETE FROM likes WHERE user_id=? AND post_id=?",
            (user_id,post_id)
        )
        db.execute(
            "UPDATE posts SET likes=likes-1 WHERE id=?",
            (post_id,)
        )
    if not existing:
        db.execute(
            "INSERT INTO likes (user_id,post_id)VALUES (?,?)",
            (user_id,post_id)
        )
        db.execute(
            "UPDATE posts SET likes=likes+1 WHERE id=?",
            (post_id,)
        )
    db.commit()
    db.close()
    return redirect("/")
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