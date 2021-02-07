from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import AddCategoryForm, DeleteCategoryForm
from app.models import Categories, Questions, Answers


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Home')


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        flash('Category added {} Category id {}'.format(
            form.name.data, form.id.data))
        note = Categories(category_id=form.id.data,
                          category_name=form.name.data)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_category.html', title='Add category',
                           form=form)


@app.route('/delete_category', methods=['GET', 'POST'])
def delete_category():
    form =DeleteCategoryForm()
    if form.validate_on_submit():
        flash('Category deleted {}'.format(
            form.name.data))
        db.session.query(Categories).filter_by\
            (category_name=form.name.data).delete()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete_category.html', title='Delete category',
                           form=form)


@app.route('/all_categories')
def all_categories():
    list_categories = db.session.query(Categories).all()
    return render_template('all_categories.html', title='ALL categories',
                           list_categories=list_categories)
