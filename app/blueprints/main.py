from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/gallery")
def gallery():
    return render_template("gallery.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/commissions")
def commissions():
    return render_template("commissions.html")
