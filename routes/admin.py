from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models.loan import Loan
from extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@login_required
def dashboard():
    if current_user.role != "admin":
        return "Unauthorized", 403

    loans = Loan.query.all()
    return render_template("admin/dashboard.html", loans=loans)


@admin_bp.route("/update-status/<int:loan_id>/<status>", methods=["POST"])
@login_required
def update_status(loan_id, status):
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    loan = Loan.query.get_or_404(loan_id)

    if status not in ["Approved", "Rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    loan.status = status
    db.session.commit()

    return jsonify({
        "success": True,
        "loan_id": loan.id,
        "status": loan.status
    })
