"""Admin routes — lawyer management dashboard (admin-only)."""
import os
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, send_from_directory, current_app)
from flask_login import login_required
from app.auth.decorators import admin_required
from app.services.lawyer_service import (
    admin_list_lawyers, admin_get_lawyer,
    admin_create_lawyer, admin_update_lawyer, admin_delete_lawyer,
    get_specializations, get_cities,
)

admin_bp = Blueprint("admin", __name__)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@admin_bp.route("/")
@login_required
@admin_required
def index():
    return redirect(url_for("admin.lawyers"))


# ─── Lawyer List ──────────────────────────────────────────────────────────────

@admin_bp.route("/lawyers")
@login_required
@admin_required
def lawyers():
    search         = request.args.get("search", "")
    city           = request.args.get("city", "")
    specialization = request.args.get("specialization", "")

    lawyers_list    = admin_list_lawyers(search=search, city=city, specialization=specialization)
    specializations = get_specializations()
    cities          = get_cities()

    return render_template(
        "admin/lawyers.html",
        lawyers=lawyers_list,
        specializations=specializations,
        cities=cities,
        search=search,
        selected_city=city,
        selected_specialization=specialization,
    )


# ─── Add Lawyer ───────────────────────────────────────────────────────────────

@admin_bp.route("/lawyers/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_lawyer():
    if request.method == "POST":
        photo = request.files.get("photo")
        result = admin_create_lawyer(
            request.form.to_dict(),
            photo_file=photo if photo and photo.filename else None,
        )
        if result["success"]:
            flash("Lawyer added successfully.", "success")
            return redirect(url_for("admin.lawyers"))
        flash(f"Error: {result['error']}", "danger")

    return render_template("admin/lawyer_form.html", lawyer=None, action="add")


# ─── Edit Lawyer ──────────────────────────────────────────────────────────────

@admin_bp.route("/lawyers/<int:lawyer_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_lawyer(lawyer_id):
    lawyer = admin_get_lawyer(lawyer_id)
    if not lawyer:
        flash("Lawyer not found.", "danger")
        return redirect(url_for("admin.lawyers"))

    if request.method == "POST":
        photo = request.files.get("photo")
        result = admin_update_lawyer(
            lawyer_id,
            request.form.to_dict(),
            photo_file=photo if photo and photo.filename else None,
        )
        if result["success"]:
            flash("Lawyer updated successfully.", "success")
            return redirect(url_for("admin.lawyers"))
        flash(f"Error: {result['error']}", "danger")

    return render_template("admin/lawyer_form.html", lawyer=lawyer, action="edit")


# ─── Delete Lawyer ────────────────────────────────────────────────────────────

@admin_bp.route("/lawyers/<int:lawyer_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_lawyer(lawyer_id):
    result = admin_delete_lawyer(lawyer_id)
    flash("Lawyer deleted." if result["success"] else f"Error: {result['error']}",
          "success" if result["success"] else "danger")
    return redirect(url_for("admin.lawyers"))


# ─── Serve Lawyer Photos ──────────────────────────────────────────────────────

@admin_bp.route("/lawyer-photo/<filename>")
def lawyer_photo(filename):
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "lawyers")
    return send_from_directory(folder, filename)
