import threading
from datetime import datetime

import psutil

from processing import app
from flask import request, session
from processing.scrape import DomesticData, International
from processing.constant import psf
from flask import render_template
import subprocess

@app.route('/instruction')
def instruction():
    return render_template('instruction.html')

# Define the Streamlit process globally
streamlit_process = None


# Function to start the Streamlit process in a separate thread
def start_streamlit():
    """
    Function to start a Streamlit application in a separate thread.

    This function manages the execution of a Streamlit application, ensuring that it is started as a subprocess,
    capturing its standard output and error streams, handling errors, and preventing multiple instances from running
    simultaneously.

    Parameters:
        None

    Global Variables Used:
        - streamlit_process: A global variable to store the process object representing the Streamlit application.

    Returns:
        None

    Example Usage:
        if __name__ == "__main__":
            psf = "path_to_streamlit_app.py"  # Replace with the actual path to your Streamlit app
            start_streamlit()
    """
    global streamlit_process

    # Check if a Streamlit process is already running
    if streamlit_process is None or not psutil.pid_exists(streamlit_process.pid):
        # Streamlit is not running, so start a new process
        streamlit_command = ["streamlit", "run", psf]

        try:
            streamlit_process = subprocess.Popen(streamlit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                 text=True)
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
    """
   Route function for the home page.

   This function defines a route to the home page of a web application. It performs the following actions:
   - Starts a Streamlit application in a separate thread using the `start_streamlit()` function.
   - The Streamlit application is launched as a separate thread to prevent blocking the main web application.
   - The thread is given a 3-second timeout to ensure it has enough time to start.
   - Clears the user's session data.
   - Renders the 'downloadForm.html' template to display the home page of the web application.

   Parameters:
       None

   Returns:
       Flask response: Returns the rendered 'downloadForm.html' template as the home page of the web application.
   """
    # Start the Streamlit process in a separate thread
    streamlit_thread = threading.Thread(target=start_streamlit)
    streamlit_thread.start()
    streamlit_thread.join(3)
    session.clear()
    return render_template("downloadForm.html")


def responding(func, name):
    """
    Helper function for generating response messages.

    This function takes a function `func` as input and attempts to execute it. If `func` runs successfully,
    it returns a success message with a 'status' of 'success' and a 'message' indicating success. If `func` raises
    an exception, it returns an error message with a 'status' of 'error' and a 'message' containing details of the error.

    Parameters:
        func (function): The function to be executed.

    Returns:
        dict: A dictionary containing the response status ('status') and message ('message').

    Example Usage:
        response = responding(some_function)
        :param name:
    """
    try:
        func
        responses = {'status': 'success', 'message': f'Data download from {name} successful!'}
    except Exception as e:
        responses = {'status': 'error', 'message': f'Error: {str(e)}'}
    return responses


# Initialize the response variable
response = {}

category, path, choice = None, None, None


@app.route('/process_form', methods=['POST'])
def process_form():
    """
    Route function to process the form submission.

    This function handles the submission of a web form and performs the following actions:
    - Determines the category of the form submission (domestic or international).
    - Retrieves user input based on the category.
    - Calls the appropriate data scraping function based on user input.
    - Generates a response message using the 'responding()' function to indicate success or failure.
    - Stores category, path, and choice in the Flask session.
    - Renders the 'downloadForm.html' template, providing the response message.

    Parameters:
        None

    Returns:
        Flask response: Returns the rendered 'downloadForm.html' template with the response message.

    Example Usage:
        This function is invoked when a POST request is made to the '/process_form' route.
    """
    global category, path, choice, response
    if 'download_button_domestic' in request.form:
        category = 'domestic'

        # Retrieve user input
        path = request.form.get('location')
        choice = request.form.get('category-domestic')  # Use 'category-download' for domestic data
        website = request.form.get('domestic-websites')

        DomesticScraper = DomesticData.Scraper(path, choice)

        if website == 'GDP':
            response = responding(DomesticScraper.GDP(), 'GDP')
        else:
            response = responding(DomesticScraper.NBC(), 'NBC')

    if "download_button_international" in request.form:
        category = 'international'
        year, month, day = None, None, None

        # Retrieve user input
        sector = request.form.get('International-Sectors')
        choice = request.form.get('international-website')

        date_string = request.form.get('date')
        year_inflation = request.form.get('infYear')

        # Convert the date string to a datetime object
        if date_string:
            date_object = datetime.strptime(date_string, '%Y-%m-%d')

            # Extract year, month, and day from the datetime object
            year = date_object.year
            month = date_object.month
            day = date_object.day
        elif year_inflation:
            year = int(year_inflation)

        path = request.form.get('path-international')
        option = request.form.get('iInternational-Sectors')

        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        month_year = request.form.get('month-year')

        scrapping = International.Scraper(choice=choice, destinationDir=path, option=option, day=day,
                                          start_date=start_date, end_date=end_date, month=month, year=year,
                                          month_year=month_year)

        if sector == 'ExchangeRate':
            response = responding(scrapping.ExchangeRate(), 'Exchange Rate')
        elif sector == 'Export':
            response = responding(scrapping.Export(), 'Export')
        elif sector == 'OpecBasketPrice':
            response = responding(scrapping.OpecBasketPrice(), 'OpecBasket Price')
        elif sector == 'InflationRate':
            response = responding(scrapping.InflationRate(), 'Inflation Rate')

    # Store data in Flask session
    session['category'] = category
    session['path'] = path
    session['choice'] = choice

    # Handle other form submissions or render the page as needed
    return render_template("downloadForm.html", response=response)


@app.route('/streamlit')
def streamlit_page():
    """
    Route function for the Streamlit page.

    This function defines a route to a Streamlit page within a web application. It performs the following actions:
    - Retrieves data from the Flask session, specifically the 'category', 'path', and 'choice' variables.
    - Renders the 'streamlit.html' template, providing the retrieved data as template variables for display on the page.

    Parameters:
        None

    Returns:
        Flask response: Returns the rendered 'streamlit.html' template with category, path, and choice variables.

    Example Usage:
        This function is invoked when a GET request is made to the '/streamlit' route.
    """
    # Retrieve data from Flask session
    categories = session.get('category')
    destination = session.get('path')
    options = session.get('choice')

    return render_template('streamlit.html', category=categories, path=destination, choice=options)
