from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, IntegerField, StringField , PasswordField,BooleanField
from wtforms.validators import Length, InputRequired, ValidationError,NumberRange, Email,DataRequired,EqualTo
from application.models import Entry
class PredictionForm(FlaskForm):
    tax = IntegerField("Tax",
        validators=[InputRequired(),NumberRange(min=0, max=580)])
    engine_size = FloatField("Engine Size",
        validators=[InputRequired(),NumberRange(min=0.0, max=6.3)])
    model = StringField("Model",
        validators=[InputRequired()])
    mileage = IntegerField("Mileage",
        validators=[InputRequired(),NumberRange(min=1, max=323000)])
    year = IntegerField("Year",
        validators=[InputRequired(),NumberRange(min=1997, max=2020)])
    mpg = FloatField("mpg",
        validators=[InputRequired(),NumberRange(min=18.0, max=188.3)])
    submit = SubmitField("Predict")

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    cfm_password = PasswordField('Comfirm Password',
                                 validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField("Sign up")

    def validate_email(self,email):
        email = Entry.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Account with this email already exist")
    
    def validate_cfm_password(self, field):
        if field.data != self.password.data:
            raise ValidationError('Passwords do not match.')
        
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Log In")