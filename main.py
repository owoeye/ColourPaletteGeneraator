import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
import color_palette

app = Flask(__name__)
Bootstrap(app)

# Secret Key
app.config["SECRET_KEY"] = "2"
app.config['UPLOAD_FOLDER'] = 'static/uploads'


# photo upload form
class PhotoForm(FlaskForm):
    photo = FileField("", validators=[FileRequired()])
    submit = SubmitField('Upload')


# generate color form
class ColorForm(FlaskForm):
    submit = SubmitField('Generate Palette')


# Flask routes for webpages
@app.route('/', methods=['GET', 'POST'])
def index():
    show_palette = False
    photo_form = PhotoForm()
    color_form = ColorForm()

    if photo_form.validate_on_submit():
        file = photo_form.photo.data
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "image.jpg"))
        return render_template("index.html", photo_form=photo_form, color_form=color_form, image="image.jpg", show=show_palette)

    if color_form.validate_on_submit():
        color_list = color_palette.find_colors("static/uploads/image.jpg")
        return render_template("index.html", photo_form=photo_form, color_form=color_form, image="image.jpg", colors=color_list, show=True)

    return render_template('index.html', photo_form=photo_form, color_form=color_form, image="default.jpg", show=show_palette)


if __name__ == "__main__":
    app.run(debug=True)
