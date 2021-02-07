from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddCategoryForm(FlaskForm):
    name = StringField("Add: ", validators=[DataRequired()])
    id = IntegerField("ID", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DeleteCategoryForm(FlaskForm):
    name = StringField("Delete: ", validators=[DataRequired()])
    submit = SubmitField("Submit")
