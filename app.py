
from flask import Flask, render_template, request, flash, redirect, url_for
import boto3
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = "student-upload-secret"


BUCKET_NAME = "student-file-upload-project"
REGION = "ap-southeast-2"

TOPIC_ARN = "arn:aws:sns:ap-southeast-2:421482182227:FileUploadNotification"


s3 = boto3.client("s3", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)


app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        flash("Please select a file!")
        return redirect(url_for("home"))

    file = request.files["file"]

    if file.filename == "":
        flash("No file selected!")
        return redirect(url_for("home"))

    filename = secure_filename(file.filename)

    if not filename:
        flash("Invalid filename!")
        return redirect(url_for("home"))

    
    s3_key = str(uuid.uuid4()) + "_" + filename

    try:
        
        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            s3_key,
            ExtraArgs={
                "ContentType": file.mimetype or "application/octet-stream"
            }
        )

        
        message = f"""
Hello!

Your file has been successfully uploaded to AWS S3.

UPLOAD DETAILS
-------------------------
File Name: {filename}
Bucket Name: {BUCKET_NAME}
AWS Region: {REGION}
Upload Status: SUCCESSFUL

Thank you for using our Cloud File Upload System!

Regards,
Cloud File Upload Team
"""

        try:
            
            sns.publish(
                TopicArn=TOPIC_ARN,
                Subject="File Uploaded Successfully!",
                Message=message
            )

            flash("File uploaded successfully! Notification email sent.")

        except Exception as e:
            print("SNS notification error:", e)
            flash("File uploaded to S3, but email notification failed.")

    except Exception as e:
        print("S3 upload error:", e)
        flash("File upload failed. Please check the server logs.")

    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
