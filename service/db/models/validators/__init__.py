from wtforms import Form, TextField, validators

class SportClubForm(Form):
    homepage = TextField('homepage', [validators.URL()])
