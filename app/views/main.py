from flask import Blueprint, render_template, g, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user

from app import db
from app.models import Word
from app.utils import get_or_create

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")


@main.route("/new/<word_class:word_class>", methods=["GET", "POST"])
@login_required
def create_word(word_class):
    form = word_class.form()

    if form.validate_on_submit():
        word, created = get_or_create(word_class, dictionary=g.user.dictionary,
                                      **{key: value for key, value in form.data.items() if key != "next"})
        if created:
            db.session.add(word)
            db.session.commit()
            flash("Successfully created word!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("An identical word already exists.", "error")

    return render_template("form.html", title="New Word", form=form)


@main.route("/delete/<int:id>")
@login_required
def delete_word(id):
    word = Word.query.filter_by(id=id, dictionary=g.user.dictionary).first_or_404()
    db.session.delete(word)
    db.session.commit()
    flash("Deleted word.", "warning")

    return redirect(url_for("main.index"))


@main.route("/login")
def login():
    if g.user.is_authenticated:
        return redirect(url_for("main.index"))

    return render_template("login.html", title="Log In")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.before_request
def before_request():
    g.user = current_user
    g.word_classes = [word_class.__mapper_args__["polymorphic_identity"] for word_class in Word.__subclasses__()]
    g.db = db