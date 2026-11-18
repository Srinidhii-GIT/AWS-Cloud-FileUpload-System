
# AWS Cloud-Based File Upload & Notification System

## Project Overview
A cloud-based web application that allows users to upload files through a web interface.

Uploaded files are stored in Amazon S3, and email notifications are sent using Amazon SNS.

## Technologies Used
- Python
- Flask
- Amazon EC2
- Amazon S3
- Amazon SNS
- Boto3
- HTML and CSS

## Architecture
1. Users upload files through the Flask web application.
2. Flask runs on Amazon EC2.
3. Boto3 uploads files to Amazon S3.
4. Amazon SNS sends email notifications after successful uploads.

## Features
- Web-based file upload
- Cloud storage using Amazon S3
- Automated email notifications
- Public web application access

## Installation
Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py
