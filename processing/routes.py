import os
import threading

import psutil

from processing import app
from flask import request, session
from processing.scrape import DomesticData, International
from processing.constant import psf
from flask import render_template
import subprocess

# Define the Streamlit process globally
streamlit_process = None


# Function to start the Streamlit process in a separate thread
def start_streamlit():
    global streamlit_process

    # Check if a Streamlit process is already running
    if streamlit_process is None or not psutil.pid_exists(streamlit_process.pid):
        # Streamlit is not running, so start a new process
        streamlit_command = ["streamlit", "run", psf,
                             "--server.headless", "true",
                             "--server.enableXsrfProtection", "false",
                             "--server.port", "8505"]

        try:
            streamlit_process = subprocess.Popen(streamlit_command, stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE, text=True)
            out, err = streamlit_process.communicate()

            if streamlit_process.returncode != 0:
                print("Error running Streamlit app. Return code:", streamlit_process.returncode)
                print("Streamlit error output:", err)
            else:
                print("Streamlit output:", out)
        except Exception as e:
            print("Error:", e)
    else:
        print("Streamlit is already running")


# Route to the home page
@app.route('/')
@app.route('/home_page')
def home_page():
    # Start the Streamlit process in a separate thread
    streamlit_thread = threading.Thread(target=start_streamlit)
    streamlit_thread.start()
    streamlit_thread.join(3)
    session.clear()
    return render_template("home.html")


def responding(func):
    try:
        func
        responses = {'status': 'success', 'message': 'Data download successful!'}
    except Exception as e:
        responses = {'status': 'error', 'message': f'Error: {str(e)}'}
    return responses


# Initialize the response variable
response = {}

category, path, choice = None, None, None


@app.route('/process_form', methods=['POST'])
def process_form():
    global category, path, choice, response
    if 'download_button_domestic' in request.form:
        category = 'domestic'

        # Retrieve user input
        path = request.form.get('location')
        choice = request.form.get('category-domestic')  # Use 'category-download' for domestic data
        website = request.form.get('domestic-websites')

        # # Write data to a shared file
        # with open('shared_data.txt', 'w') as file:
        #     file.write(f'{category},{path},{choice}')

        if website == 'website1':
            response = responding(DomesticData.GDP(path, choice).scrap_GDP_Choice())
        else:
            response = responding(DomesticData.NBC(path, choice).scrap_NBC_Choice())

    if "download_button_international" in request.form:
        category = 'international'

        # Retrieve user input
        path = request.form.get('path-international')
        website = request.form.get('international-website')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')

        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        # page_number = int(request.form.get('page_number'))
        input_date_str = request.form.get('input_date_str')

        scrapping = International.Scraper(path=path, year=year, day=day, month=month)
        if website == 'website1':
            response = responding(scrapping.opec_org())
        elif website == 'website2':
            response = responding(scrapping.ExchangeRateIndonesia())
        elif website == 'website3':
            response = responding(scrapping.thailand_exchange_rate())
        elif website == 'website4':
            response = responding(scrapping.exp_srilanka())
        elif website == 'website5':
            response = responding(scrapping.china_exchange_rate(path=path, start_date=start_date, end_date=end_date))
        elif website == 'website6':
            response = responding(scrapping.adb())
        elif website == 'website7':
            response = responding(scrapping.banglashdesh_ex_rate(input_date_str=input_date_str))

    # Store data in Flask session
    session['category'] = category
    session['path'] = path
    session['choice'] = choice

    # Handle other form submissions or render the page as needed
    return render_template('home.html', response=response)


@app.route('/streamlit')
def streamlit_page():
    # Retrieve data from Flask session
    category = session.get('category')
    path = session.get('path')
    choice = session.get('choice')

    return render_template('streamlit.html', category=category, path=path, choice=choice)
