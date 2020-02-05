'''
You need to have AWS credentials in ~/.aws/credentials
[default]
aws_access_key_id=KEY_ID
aws_secret_access_key=ACCESS_KEY
'''

from flask import Flask, request
import boto3
# from werkzeug.utils import secure_filename

app = Flask(__name__)
S3_BUCKET='test-photo1'
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
@app.route('/')
def index():
    return '''<form method=POST enctype=multipart/form-data action="upload">
    <input type=file name=myfile>
    <input type=submit>
    </form>'''


@app.route('/upload', methods=['POST'])
def upload():
    if "myfile" not in request.files:
        return "No myfile key in request.files"
    s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAIEO6XXJPAZOJJN7A',
                        aws_secret_access_key='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')

    # s3.Bucket('onigazer-photos').put_object(Key='a_python_file.py',
    #                                         Body=request.files['myfile'])
    # There is no file selected to upload
    file = request.files["myfile"]
    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        # file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(s3, file, S3_BUCKET)
        return str(output)
    # upload_file_to_s3(s3, request.files['myfile'], )
    # return '<h1>File saved to S3</h1>'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_s3(s3, file, bucket_name, acl="public-read"):
    try:
        # s3.upload_fileobj(
        #     file,
        #     bucket_name,
        #     file.filename,
        #     ExtraArgs={
        #         "ACL": acl,
        #         "ContentType": file.content_type
        #     }
        # )
        s3.Bucket(bucket_name).put_object(Key=file.filename,
                                            Body=file,ACL='public-read')
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(S3_LOCATION, file.filename)

if __name__ == '__main__':
    app.run(debug=True)
