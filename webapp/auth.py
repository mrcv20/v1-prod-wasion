from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        FirstName = request.form.get('FirstName')
        password = request.form.get('password')

        # procurando pelo id do usuario o e checando a senha hasheada
        user = User.query.filter_by(FirstName=FirstName).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logado com sucesso!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Senha incorreta, tente novamente.", category='error')
        else:
            flash('Login não existe.', category='error')        
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        FirstName = request.form.get('FirstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user2 = User.query.filter_by(email=email).first()
        user = User.query.filter_by(FirstName=FirstName).first()
        if user:    
            flash('Login já existe.', category='error')
        elif user2:
            flash('Email já existe.', category='error')
        elif len(email) < 4:
            flash('Email precisa ter mais de 4 caracteres.', category='error')
        elif len(FirstName) < 2:
            flash('Nome precisa ter mais de 1 caractere.', category='error')
        elif password1 != password2:
            flash('Senhas não coincidem.', category='error')
        elif len(password1) < 7:
            flash('Senha precisa de pelo menos 7 digitos', category='error')
        else:
            new_user = User(email=email, FirstName=FirstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)
