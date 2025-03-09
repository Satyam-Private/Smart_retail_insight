from flask import Flask, request, send_from_directory, render_template
import os
from data_processor import generate_insights
import customer_seg

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "outputs"

# Ensure the necessary directories exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

@app.route('/')
def index():
    # Render the upload form page
    return render_template('index.html')

@app.route('/index')
def index1():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        try:
            results = generate_insights(filepath, output_dir=app.config["OUTPUT_FOLDER"])
        except Exception as e:
            return f"Error processing file: {e}", 500
        customer_seg.model(filepath, "outputs")
        # Prepare context for the results page
        context = {
            'filename': file.filename,
            'sales_overview': results.get('sales_overview', {}),
            'top_products': results.get('top_products', []),
            'revenue_trend': os.path.basename(results.get('revenue_trend')) if results.get('revenue_trend') else None,
            'category_insights_image': os.path.basename(results.get('category_insights_image')) if results.get('category_insights_image') else None,
            'before customer segmentation': os.path.basename(results.get('before_customer_segmentation')) if results.get('before_customer_segmentation') else None,
            'after customer segmentation': os.path.basename(results.get('after_customer_segmentation')) if results.get('after_customer_segmentation') else None
        }
        return render_template('results.html', **context)
    return "File not processed", 400

@app.route('/outputs/<filename>')
def outputs(filename):
    # Serve images saved in the outputs folder
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)

if __name__ == '__main__':
    app.run(debug=True)
