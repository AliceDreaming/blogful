from flask import render_template

from blog import app
from .database import session
from .models import Entry
from flask import request, redirect, url_for
from flask.ext.login import login_required
from flask.ext.login import current_user
import mistune

PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) / PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )
 
@app.route("/post/<int:post_id>")
def view_post(post_id=0):
    entry = session.query(Entry).filter(Entry.id == post_id).first()
    return render_template("post.html", post=entry)

@app.route("/post/<int:post_id>/edit", methods=["GET"])
def edit_post_get(post_id):
    entry = session.query(Entry).filter(Entry.id == post_id).first()
    return render_template("edit_entry.html", post = entry)

@app.route("/post/<int:post_id>/edit", methods=["POST"])
def edit_entry_post(post_id):
    entry = session.query(Entry).filter(Entry.id == post_id).first()
    entry.title = request.form["title"]
    entry.content = request.form["content"]
    session.commit()
    return redirect(url_for("view_post", post_id=post_id))

@app.route("/post/<int:post_id>/delete", methods=["GET"])
def delete_entry(post_id):
    entry = session.query(Entry).filter(Entry.id == post_id).first()
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))

@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")

@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from .models import User

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))