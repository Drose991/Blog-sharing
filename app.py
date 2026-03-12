from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, username FROM users ORDER BY id;")
    users = cur.fetchall()

    cur.execute("SELECT id, name FROM categories ORDER BY id;")
    categories = cur.fetchall()

    cur.execute("""
        SELECT 
            b.id,
            b.title,
            b.content,
            u.username,
            c.name,
            b.created_at
        FROM blogs b
        JOIN users u ON b.user_id = u.id
        JOIN categories c ON b.category_id = c.id
        ORDER BY b.id;
    """)
    blogs = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        users=users,
        categories=categories,
        blogs=blogs
    )


@app.route("/add", methods=["POST"])
def add_blog():
    title = request.form["title"]
    content = request.form["content"]
    user_id = request.form["user_id"]
    category_id = request.form["category_id"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO blogs (title, content, user_id, category_id)
        VALUES (%s, %s, %s, %s)
    """, (title, content, user_id, category_id))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:blog_id>", methods=["POST"])
def delete_blog(blog_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM blogs WHERE id = %s", (blog_id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("index"))


@app.route("/edit/<int:blog_id>", methods=["GET", "POST"])
def edit_blog(blog_id):
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        user_id = request.form["user_id"]
        category_id = request.form["category_id"]

        cur.execute("""
            UPDATE blogs
            SET title = %s, content = %s, user_id = %s, category_id = %s
            WHERE id = %s
        """, (title, content, user_id, category_id, blog_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    cur.execute("SELECT id, username FROM users ORDER BY id;")
    users = cur.fetchall()

    cur.execute("SELECT id, name FROM categories ORDER BY id;")
    categories = cur.fetchall()

    cur.execute("""
        SELECT id, title, content, user_id, category_id
        FROM blogs
        WHERE id = %s
    """, (blog_id,))
    blog = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "edit.html",
        blog=blog,
        users=users,
        categories=categories
    )


if __name__ == "__main__":
    app.run(debug=True)
