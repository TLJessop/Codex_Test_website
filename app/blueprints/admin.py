from functools import wraps

from flask import Blueprint, redirect, render_template, request, session, url_for

from app.models import CommissionSubmission, FeaturedImage, GalleryImage, User, db

admin_bp = Blueprint("admin", __name__)


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_user_id"):
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)

    return wrapped


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["admin_user_id"] = user.id
            return redirect(url_for("admin.dashboard"))
        error = "Invalid username or password."
    return render_template("admin/login.html", error=error)


@admin_bp.route("/logout", methods=["POST"])
@admin_required
def logout():
    session.pop("admin_user_id", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@admin_required
def dashboard():
    gallery_count = GalleryImage.query.count()
    featured_count = FeaturedImage.query.count()
    commission_count = CommissionSubmission.query.count()
    return render_template(
        "admin/dashboard.html",
        gallery_count=gallery_count,
        featured_count=featured_count,
        commission_count=commission_count,
    )


@admin_bp.route("/gallery")
@admin_required
def manage_gallery():
    images = GalleryImage.query.order_by(GalleryImage.position.asc()).all()
    return render_template("admin/gallery.html", images=images)


@admin_bp.route("/gallery/add", methods=["POST"])
@admin_required
def add_gallery_image():
    title = request.form.get("title", "").strip()
    filename = request.form.get("filename", "").strip()
    description = request.form.get("description", "").strip()
    if title and filename:
        new_image = GalleryImage(
            title=title,
            filename=filename,
            description=description or None,
            position=GalleryImage.query.count(),
        )
        db.session.add(new_image)
        db.session.commit()
    return redirect(url_for("admin.manage_gallery"))


@admin_bp.route("/gallery/reorder", methods=["POST"])
@admin_required
def reorder_gallery():
    for image in GalleryImage.query.all():
        position_value = request.form.get(f"position_{image.id}")
        if position_value is not None and position_value.isdigit():
            image.position = int(position_value)
    db.session.commit()
    return redirect(url_for("admin.manage_gallery"))


@admin_bp.route("/gallery/<int:image_id>/delete", methods=["POST"])
@admin_required
def delete_gallery_image(image_id):
    image = GalleryImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for("admin.manage_gallery"))


@admin_bp.route("/featured")
@admin_required
def manage_featured():
    images = FeaturedImage.query.order_by(FeaturedImage.position.asc()).all()
    return render_template("admin/featured.html", images=images)


@admin_bp.route("/featured/add", methods=["POST"])
@admin_required
def add_featured_image():
    title = request.form.get("title", "").strip()
    filename = request.form.get("filename", "").strip()
    description = request.form.get("description", "").strip()
    if title and filename:
        new_image = FeaturedImage(
            title=title,
            filename=filename,
            description=description or None,
            position=FeaturedImage.query.count(),
        )
        db.session.add(new_image)
        db.session.commit()
    return redirect(url_for("admin.manage_featured"))


@admin_bp.route("/featured/reorder", methods=["POST"])
@admin_required
def reorder_featured():
    for image in FeaturedImage.query.all():
        position_value = request.form.get(f"position_{image.id}")
        if position_value is not None and position_value.isdigit():
            image.position = int(position_value)
    db.session.commit()
    return redirect(url_for("admin.manage_featured"))


@admin_bp.route("/featured/<int:image_id>/delete", methods=["POST"])
@admin_required
def delete_featured_image(image_id):
    image = FeaturedImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for("admin.manage_featured"))


@admin_bp.route("/commissions")
@admin_required
def view_commissions():
    submissions = CommissionSubmission.query.order_by(
        CommissionSubmission.created_at.desc()
    ).all()
    return render_template("admin/commissions.html", submissions=submissions)
