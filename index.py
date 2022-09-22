import os
from io import BytesIO
import PyPDF2
from flask import Flask, render_template, request, redirect, session, make_response, send_file, send_from_directory
# from werkzeug import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['pdf','PDF'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_pdf', methods=['GET', 'POST'])
def show_pdf():
    if request.method == 'POST':
        send_data = request.files['send_data']
        if send_data and allowed_file(send_data.filename):
            
            output_pdf = PyPDF2.PdfFileWriter()

            pdf  = PyPDF2.PdfFileReader(send_data)
            pdf2  = PyPDF2.PdfFileReader(send_data)

            numPages = pdf.getNumPages()

            for i in range(numPages):

                shipping_label = pdf.pages[i]
                invoice = pdf2.pages[i]
                shipping_label.cropBox.lowerLeft=(168,478)
                shipping_label.cropBox.upperRight = (430,820)
                
                invoice.cropBox.lowerLeft=(0,78)
                invoice.cropBox.upperRight = (800,470)


                output_pdf.addPage(shipping_label)

                output_pdf.addPage(invoice)

            #this works
            # outputStream = open(r"output.pdf", "wb")
            # output_pdf.write(outputStream)

            outfile = BytesIO()
            output_pdf.write(outfile)
            outfile.seek(0)

            output_filename = send_data.filename +'-output.pdf'

            return send_file(outfile,mimetype='application/pdf',download_name=output_filename)

            # return render_template('pdf.html', result=result)

@app.route('/manifest.json')
def manifest():
    return send_from_directory(app.static_folder, 'manifest.json')


@app.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory(app.static_folder, 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.route('/ads.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
    app.debug = True
    app.run()