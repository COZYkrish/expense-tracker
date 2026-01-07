from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models.loan import Loan
from extensions import db

user_bp = Blueprint("user", __name__, url_prefix="/user")


# ===============================
# USER DASHBOARD
# ===============================
@user_bp.route("/dashboard")
@login_required
def dashboard():
    loans = Loan.query.filter_by(user_id=current_user.id).all()
    return render_template("user/dashboard.html", loans=loans)


# Optional: redirect /user → /user/dashboard
@user_bp.route("/")
@login_required
def dashboard_redirect():
    return redirect(url_for("user.dashboard"))


# ===============================
# APPLY FOR LOAN
# ===============================
@user_bp.route("/apply", methods=["POST"])
@login_required
def apply_loan():
    loan = Loan(
        user_id=current_user.id,
        borrower=current_user.username,
        amount=request.form["amount"],
        tenure=request.form["tenure"],
        status="Pending"
    )
    db.session.add(loan)
    db.session.commit()

    return redirect(url_for("user.dashboard"))


# ===============================
# USER LOANS API
# ===============================
@user_bp.route("/loans")
@login_required
def user_loans_api():
    loans = Loan.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            "id": loan.id,
            "amount": loan.amount,
            "tenure": loan.tenure,
            "status": loan.status
        }
        for loan in loans
    ])
