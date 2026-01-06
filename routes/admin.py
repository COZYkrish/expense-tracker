from flask import Blueprint, render_template, redirect
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

@admin_bp.route("/approve/<int:loan_id>")
@login_required
def approve(loan_id):
    loan = Loan.query.get(loan_id)
    loan.status = "Approved"
    db.session.commit()
    return redirect("/admin")

@admin_bp.route("/reject/<int:loan_id>")
@login_required
def reject(loan_id):
    loan = Loan.query.get(loan_id)
    loan.status = "Rejected"
    db.session.commit()
    return redirect("/admin")
