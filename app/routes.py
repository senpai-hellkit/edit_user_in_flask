from flask import render_template, url_for, redirect, request

from app import app, db
from app.forms import RegistrationForm, SearchByLastNameForm, EditUserForm
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/find_to_edit_user', methods=['GET', 'POST'])
def find_to_edit_user():
    form = SearchByLastNameForm()
    if form.validate_on_submit():
        users = User.query.filter_by(last_name=form.last_name.data).all()
        return render_template('find_to_edit_user.html', form=form, users=users)
    return render_template('find_to_edit_user.html', form=form)


@app.route('/edit_user/<int:_id>', methods=['GET', 'POST'])
def edit_user(_id):
    user = User.query.filter_by(id=_id).first()
    form = EditUserForm()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
    return render_template('edit_user.html', form=form, user=user)
