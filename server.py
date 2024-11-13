from flask import Flask, Response,render_template,request,jsonify
from flask_cors import CORS
import os
import io
from xhtml2pdf import pisa
import json
import base64
app = Flask(__name__)
CORS(app, resources={r"/post-endpoint": {"origins": "*"}}) 
port = int(os.environ.get('PORT', 4004))
templates_path = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=templates_path)
@app.route('/generatePDF', methods=['POST'])
def generatePDF():
    data = request.get_json()

    context=  {      "pdfData": data  }  

    html = render_template('/template.html', **context) 
    pdf_buffer = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=pdf_buffer) 
    pdf_content = pdf_buffer.getvalue()
    pdf_buffer.seek(0)
    # return Response(
    #       pdf_content,
    #       mimetype='application/pdf',
    #       headers={"Content-Disposition": "inline; filename=generated.pdf"}
    #   )
    base64_pdf = base64.b64encode(pdf_content).decode('utf-8') 
    return jsonify({"PDF_base64": base64_pdf }), 200 
     
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port,debug=True)