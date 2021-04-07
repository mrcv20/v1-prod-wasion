from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Note
import pygal


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
    

@views.route('/graphics')
@login_required 
def graphics():
    try:
        graph = pygal.Line()
        graph.title = '% Change Coolness of programming lanaguaes over time.'
        graph.x_labels = ['2011', '2012', '2013', '2014','2015', '2016']
        graph.add('Python', [11, 17, 51, 325, 356, 900])
        graph.add('Java', [12, 16, 75, 325, 652, 750])
        graph.add('C++', [13, 15, 42, 333, 846, 800])
        graph.add('All others combined', [6, 54, 70, 150, 300, 700])
        graph_data = graph.render_data_uri()
        return render_template('graphics.html', graph_data=graph_data, user=current_user)
    except Exception as e:
        return(str(e))


@views.route('/data')
@login_required
def data():
    try:
        all_data = Note.query.all()
        return render_template('data.html', data=all_data, pageTitle='teste', user=current_user)
    except Exception as e:
        return(str(e))