# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import datetime

from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, DateTimeField
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms import widgets, SelectMultipleField
from wtforms.fields.html5 import DateTimeLocalField

class MultiCheckboxField(SelectMultipleField):
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.CheckboxInput()

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])

class SearchForm(FlaskForm):
	string_of_files = ['период\r\n']
	list_of_files = string_of_files[0].split()
	# create a list of value/description tuples
	files = [(x, x) for x in list_of_files]
	example = MultiCheckboxField('Label', choices=files)
	origcity = StringField ('origcity', validators=[DataRequired()])
	destcity = StringField ('destcity', validators=[DataRequired()])
	example = MultiCheckboxField('Label', choices=files)
	search = SubmitField()
	Time = DateTimeLocalField(default=datetime.datetime.now(),validators=[DataRequired()])
