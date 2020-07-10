from flask import Flask
from flask import render_template 

import zipfile
from json import loads, decoder


# --- for uploading files ---
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"zip"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# --- ................... ---



def unzip_tweets(filename):
    working_dir = app.config["UPLOAD_FOLDER"] + "/"
    with zipfile.ZipFile(working_dir + filename, 'r') as zip_ref:
            zip_ref.extractall(working_dir + "dir_" + filename)

    working_dir += "dir_" + filename + "/"
    try:
        json_file = open(working_dir + "data/tweet.js", "r").read()
        json_file = "[" + json_file.split("[", 1)[1]
        
        tweet_data = loads(json_file)
        for tweet in tweet_data:
            tweet = tweet["tweet"]
            print(tweet["id_str"])
            <...>
            data_base.write( User_id, tweet["id_str"], tweet["created_at"] )
            <...>

    except FileNotFoundError:
        return "File not found"
    except decoder.JSONDecodeError:
        return "JSON decode error"
    return 0



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "petr_lapa_ochen_horoshiy"


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html") 


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            status = unzip_tweets(filename)
            if status != "Success":
                ...
            return redirect("/index")
        
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")
