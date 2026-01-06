from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from models.loan import Loan
from extensions import db

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/")
@login_required
def dashboard():
    loans = Loan.query.filter_by(user_id=current_user.id).all()
    return render_template("user/dashboard.html", loans=loans)

@user_bp.route("/apply", methods=["POST"])
@login_required
def apply_loan():
    loan = Loan(
        user_id=current_user.id,
        borrower=current_user.username,
        amount=request.form["amount"],
        tenure=request.form["tenure"]
    )
    db.session.add(loan)
    db.session.commit()
    return redirect("/user")
