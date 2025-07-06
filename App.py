from flask import Flask, render_template, request
from text_moderation import moderate_text
from Image_moderation import moderate_image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    text_result = None
    image_result = None

    if request.method == 'POST':
        user_text = request.form.get('user_text')
        if user_text:
            text_result = moderate_text(user_text)

        file = request.files.get('image')
        if file:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            image_result = moderate_image(path)

    return render_template("index.html", text_result=text_result, image_result=image_result)

if __name__ == '__main__':
    app.run(debug=True)