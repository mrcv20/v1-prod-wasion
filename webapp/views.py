from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Note


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        category_issue = request.form.get('category')
        start_date = request.form.get('start_date')
        final_date = request.form.get('final_date')
        description = request.form.get('description')
        cause_issue = request.form.get('cause_issue')
        solution_issue = request.form.get('solution_issue')
        if len(description) < 1:
            flash("Note is too short", category='error')
        else:
            new_note = Note(cause_issue=cause_issue, solution_issue=solution_issue, category_issue=category_issue, description=description, final_date=final_date, start_date=start_date, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added", category='success')
    return render_template("home.html", user=current_user)
