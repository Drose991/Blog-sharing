from flask import abort, redirect, render_template, request, url_for
from sqlalchemy.orm import joinedload

from blog_app.database import SessionLocal
from blog_app.models import Blog, Category, User


def register_routes(app):
    @app.route("/")
    def index():
        with SessionLocal() as session:
            users = session.query(User).order_by(User.id).all()
            categories = session.query(Category).order_by(Category.id).all()
            blogs = (
                session.query(Blog)
                .options(joinedload(Blog.user), joinedload(Blog.category))
                .order_by(Blog.id)
                .all()
            )
            join_results = (
                session.query(
                    Blog.id,
                    Blog.title,
                    User.username,
                    Category.name,
                    Blog.created_at,
                )
                .join(User, Blog.user_id == User.id)
                .join(Category, Blog.category_id == Category.id)
                .order_by(Blog.id)
                .all()
            )

        return render_template(
            "index.html",
            users=users,
            categories=categories,
            blogs=blogs,
            join_results=join_results,
        )

    @app.route("/add", methods=["POST"])
    def add_blog():
        with SessionLocal() as session:
            new_blog = Blog(
                title=request.form["title"],
                content=request.form["content"],
                user_id=int(request.form["user_id"]),
                category_id=int(request.form["category_id"]),
            )
            session.add(new_blog)
            session.commit()

        return redirect(url_for("index"))

    @app.route("/delete/<int:blog_id>", methods=["POST"])
    def delete_blog(blog_id):
        with SessionLocal() as session:
            blog = session.get(Blog, blog_id)
            if blog is not None:
                session.delete(blog)
                session.commit()

        return redirect(url_for("index"))

    @app.route("/edit/<int:blog_id>", methods=["GET", "POST"])
    def edit_blog(blog_id):
        with SessionLocal() as session:
            blog = session.get(Blog, blog_id)
            if blog is None:
                abort(404)

            users = session.query(User).order_by(User.id).all()
            categories = session.query(Category).order_by(Category.id).all()

            if request.method == "POST":
                blog.title = request.form["title"]
                blog.content = request.form["content"]
                blog.user_id = int(request.form["user_id"])
                blog.category_id = int(request.form["category_id"])
                session.commit()
                return redirect(url_for("index"))

            return render_template(
                "edit.html",
                blog=blog,
                users=users,
                categories=categories,
            )
