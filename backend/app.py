from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import pandas as pd
import numpy as np
from utils.email_sender import send_email
from utils.export import export_to_pdf, export_to_excel, export_to_csv
import os

# Initialize Flask app
app = Flask(_name_, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'supersecretkey'

# Global variables to store data and weights
data = None
weights = {'Productivity': 0.4, 'Quality': 0.3, 'Timeliness': 0.3}  # Default weights

@app.route('/')
def index():
    """
    Home page where users can upload their data file.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle file upload and validate the file.
    """
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('index'))
    
    if file:
        try:
            # Read the uploaded file into a DataFrame
            df = pd.read_excel(file)
            global data
            data = df.to_dict(orient='list')  # Convert DataFrame to dictionary
            flash('File uploaded successfully', 'success')
        except Exception as e:
            flash(f'Error reading file: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """
    Dashboard to display scores, update weights, and visualize data.
    """
    global weights, data
    
    if data is None:
        flash('No data available. Please upload a file first.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Update weights based on user input
        try:
            weights = {
                'Productivity': float(request.form['productivity_weight']),
                'Quality': float(request.form['quality_weight']),
                'Timeliness': float(request.form['timeliness_weight'])
            }
            flash('Weights updated successfully', 'success')
        except ValueError:
            flash('Invalid weight values. Please enter numbers.', 'danger')
    
    # Calculate scores based on weights
    scores = []
    for i in range(len(data['Employee'])):
        score = sum(data[category][i] * weights[category] for category in weights)
        scores.append(score)
    
    data['Score'] = scores  # Add scores to the data dictionary
    return render_template('dashboard.html', data=data, weights=weights)

@app.route('/export/<format>')
def export(format):
    """
    Export the scorecard in the specified format (PDF, Excel, CSV).
    """
    if data is None:
        flash('No data available to export.', 'danger')
        return redirect(url_for('index'))
    
    if format == 'pdf':
        file_path = export_to_pdf(data)
    elif format == 'excel':
        file_path = export_to_excel(data)
    elif format == 'csv':
        file_path = export_to_csv(data)
    else:
        flash('Invalid export format', 'danger')
        return redirect(url_for('dashboard'))
    
    return send_file(file_path, as_attachment=True)

@app.route('/send_email', methods=['GET', 'POST'])
def send_email_route():
    """
    Send the scorecard via email as an attachment.
    """
    if data is None:
        flash('No data available to send.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = "Performance Scorecard"
        body = "Please find the attached performance scorecard."
        file_path = export_to_pdf(data)
        
        if send_email(recipient, subject, body, file_path):
            flash('Email sent successfully', 'success')
        else:
            flash('Failed to send email', 'danger')
        
        return redirect(url_for('dashboard'))
    
    return render_template('email_form.html')

if _name_ == '_main_':
    app.run(debug=True)