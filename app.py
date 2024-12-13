import os
import pdfkit
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import chatbot

app = Flask(__name__)
CORS(app)

# To crate a pdf wkhtmltopdf should installed path should set as follows
# Specify the path to wkhtmltopdf executable
# Adjust this path based on installation
config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

@app.route('/get-shelf-location', methods=['POST'])
def get_shelf_location():
    data = request.json
    input_text = data.get('input_text', '')
    
    greeting_response = chatbot.respond_to_greeting(input_text)
    if greeting_response:
        return jsonify({
            'message': greeting_response,
            'locations': {},
            'pdf_url': None
        })
    
    tagged_input = chatbot.process_input(input_text)
    goods_list = [word for word, tag in tagged_input if tag.startswith('NN')]
    
    locations = chatbot.get_goods_location(goods_list)
    
    # Generate PDF
    pdf_filename = generate_pdf(goods_list, locations)
    
    return jsonify({
        'message': None,
        'locations': locations,
        'pdf_url': f'/download/{pdf_filename}'
    })

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    directory = os.getcwd()
    return send_from_directory(directory, filename, as_attachment=True)

def generate_pdf(goods_list, locations):
    html_content = generate_html(goods_list, locations)
    pdf_filename = 'shelf_locations.pdf'
    pdfkit.from_string(html_content, pdf_filename, configuration=config)
    return pdf_filename

def generate_html(goods_list, locations):
    html_content = f'''
    <html>
    <head><title>Shelf Locations</title></head>
    <body>
        <h1>Shelf Locations</h1>
        <p>Requested goods: {', '.join(goods_list)}</p>
        <ul>
    '''
    for good, shelf in locations.items():
        html_content += f'<li>{good}: Shelf {shelf}</li>'
    
    html_content += '''
        </ul>
    </body>
    </html>
    '''
    return html_content

if __name__ == '__main__':
    app.run(debug=True)
