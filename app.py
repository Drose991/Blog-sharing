from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)

    blogs = relationship("Blog", back_populates="user", cascade="all, delete")
    comments = relationship("Comment", back_populates="user", cascade="all, delete")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    blogs = relationship("Blog", back_populates="category", cascade="all, delete")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="blogs")
    category = relationship("Category", back_populates="blogs")
    comments = relationship("Comment", back_populates="blog", cascade="all, delete")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    blog = relationship("Blog", back_populates="comments")
    user = relationship("User", back_populates="comments")


@app.route("/")
def index():
    session = SessionLocal()

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
            Blog.created_at
        )
        .join(User, Blog.user_id == User.id)
        .join(Category, Blog.category_id == Category.id)
        .order_by(Blog.id)
        .all()
    )

    session.close()

    return render_template(
        "index.html",
        users=users,
        categories=categories,
        blogs=blogs,
        join_results=join_results
    )


@app.route("/add", methods=["POST"])
def add_blog():
    session = SessionLocal()

    title = request.form["title"]
    content = request.form["content"]
    user_id = int(request.form["user_id"])
    category_id = int(request.form["category_id"])

    new_blog = Blog(
        title=title,
        content=content,
        user_id=user_id,
        category_id=category_id
    )

    session.add(new_blog)
    session.commit()
    session.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:blog_id>", methods=["POST"])
def delete_blog(blog_id):
    session = SessionLocal()

    blog = session.query(Blog).filter_by(id=blog_id).first()
    if blog:
        session.delete(blog)
        session.commit()

    session.close()
    return redirect(url_for("index"))


@app.route("/edit/<int:blog_id>", methods=["GET", "POST"])
def edit_blog(blog_id):
    session = SessionLocal()

    blog = session.query(Blog).filter_by(id=blog_id).first()
    users = session.query(User).order_by(User.id).all()
    categories = session.query(Category).order_by(Category.id).all()

    if request.method == "POST":
        blog.title = request.form["title"]
        blog.content = request.form["content"]
        blog.user_id = int(request.form["user_id"])
        blog.category_id = int(request.form["category_id"])

        session.commit()
        session.close()
        return redirect(url_for("index"))

    response = render_template(
        "edit.html",
        blog=blog,
        users=users,
        categories=categories
    )
    session.close()
    return response


if __name__ == "__main__":
    app.run(debug=True)
