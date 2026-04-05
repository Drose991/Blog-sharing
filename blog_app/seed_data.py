from blog_app.models import Blog, Category, Comment, User

SAMPLE_USERS = [
    {"username": "ali", "email": "ali@mail.com"},
    {"username": "ayse", "email": "ayse@mail.com"},
    {"username": "mehmet", "email": "mehmet@mail.com"},
    {"username": "zeynep", "email": "zeynep@mail.com"},
    {"username": "can", "email": "can@mail.com"},
    {"username": "elif", "email": "elif@mail.com"},
    {"username": "mert", "email": "mert@mail.com"},
    {"username": "sena", "email": "sena@mail.com"},
    {"username": "burak", "email": "burak@mail.com"},
    {"username": "derya", "email": "derya@mail.com"},
]

SAMPLE_CATEGORIES = [
    "Technology",
    "Education",
    "Travel",
    "Health",
    "Sports",
    "Music",
    "Science",
    "Food",
    "Lifestyle",
    "Business",
]

SAMPLE_BLOGS = [
    {"user_index": 0, "category_index": 0, "title": "Flask Basics", "content": "Introduction to Flask framework."},
    {"user_index": 1, "category_index": 1, "title": "Study Tips", "content": "Useful tips for studying efficiently."},
    {"user_index": 2, "category_index": 2, "title": "Trip to Norway", "content": "My travel experience in Norway."},
    {"user_index": 3, "category_index": 3, "title": "Healthy Living", "content": "How to stay healthy every day."},
    {"user_index": 4, "category_index": 4, "title": "Football News", "content": "Latest football updates."},
    {"user_index": 5, "category_index": 5, "title": "Learning Guitar", "content": "Beginner guide for guitar."},
    {"user_index": 6, "category_index": 6, "title": "Space Discoveries", "content": "Recent discoveries in space."},
    {"user_index": 7, "category_index": 7, "title": "Best Pasta Recipe", "content": "Easy and delicious pasta recipe."},
    {"user_index": 8, "category_index": 8, "title": "Daily Routine", "content": "A productive daily routine."},
    {"user_index": 9, "category_index": 9, "title": "Startup Ideas", "content": "Simple startup ideas for students."},
]

SAMPLE_COMMENTS = [
    {"blog_index": 0, "user_index": 1, "content": "Great post!"},
    {"blog_index": 1, "user_index": 2, "content": "Very helpful, thanks."},
    {"blog_index": 2, "user_index": 3, "content": "Nice travel story."},
    {"blog_index": 3, "user_index": 4, "content": "Good advice."},
    {"blog_index": 4, "user_index": 5, "content": "Interesting update."},
    {"blog_index": 5, "user_index": 6, "content": "I want to learn too."},
    {"blog_index": 6, "user_index": 7, "content": "Amazing topic."},
    {"blog_index": 7, "user_index": 8, "content": "Looks delicious."},
    {"blog_index": 8, "user_index": 9, "content": "Very relatable."},
    {"blog_index": 9, "user_index": 0, "content": "Nice business ideas."},
]


def seed_database(session):
    if session.query(User.id).first() is not None:
        return

    users = [User(**user_data) for user_data in SAMPLE_USERS]
    categories = [Category(name=category_name) for category_name in SAMPLE_CATEGORIES]

    session.add_all(users)
    session.add_all(categories)
    session.flush()

    blogs = [
        Blog(
            user_id=users[blog_data["user_index"]].id,
            category_id=categories[blog_data["category_index"]].id,
            title=blog_data["title"],
            content=blog_data["content"],
        )
        for blog_data in SAMPLE_BLOGS
    ]
    session.add_all(blogs)
    session.flush()

    comments = [
        Comment(
            blog_id=blogs[comment_data["blog_index"]].id,
            user_id=users[comment_data["user_index"]].id,
            content=comment_data["content"],
        )
        for comment_data in SAMPLE_COMMENTS
    ]
    session.add_all(comments)
    session.commit()
