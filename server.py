from flask import Flask, render_template,request,flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import face_detection
import yolo_image
app=Flask(__name__)

app.config["UPLOAD_FOLDER"]="static/uploaded"
app.config["DISPLAYED_FOLDER"]="static/displayed"
app.secret_key = "secret key"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/uploader", methods=["GET","POST"])
def uploader():
    if request.method=="POST":
        if "image" not in request.files:
            flash("No image selected!!!")
            return redirect(url_for("home"))
        file = request.files['image']
        if file.filename == '':
            flash('No image selected for uploading!!!')
            return redirect(url_for("home"))
        if file and allowed_file(file.filename):
            img=request.files["image"]
            file_name=secure_filename(img.filename)
            image_path=(os.path.join(app.config["UPLOAD_FOLDER"],file_name))
            img.save(image_path)
            output_path=os.path.join(app.config["DISPLAYED_FOLDER"],file_name)
            yolo_image.main(image_path,output_path)
            flash('Uploaded successfully!!!')
            # Do processing 
            return render_template("index.html",display_rendered=file_name,detected=file_name)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(url_for("home"))
        
@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename="uploaded/"+filename), code=301)

@app.route('/display_detected/<filename>')
def display_detected_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename="displayed/"+filename), code=301)
  
  
if __name__=="__main__":
    app.run(host="0.0.0.0")