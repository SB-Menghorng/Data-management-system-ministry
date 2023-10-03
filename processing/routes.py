import threading
from datetime import datetime

from processing import app
from flask import request, session

from processing.Streamlit.streamlit import start_dashboard, start_excel
from processing.scrape import DomesticData, International
from flask import render_template


@app.route('/instruction')
def instruction():
    return render_template('instruction.html')


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
    dashboard_thread = threading.Thread(target=start_dashboard)
    dashExcel_thread = threading.Thread(target=start_excel)

    dashExcel_thread.start()
    dashboard_thread.start()

    dashboard_thread.join(3)  # Wait for dashboard_thread to complete for 3 seconds
    dashExcel_thread.join(3)  # Wait for dashExcel_thread to complete for 3 seconds

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
        name (str): The name of the function or task being executed.

    Returns:
        dict: A dictionary containing the response status ('status') and message ('message').

    Example Usage:
        response = responding(some_function, "Data Download")
    """
    try:
        func()  # Execute the input function
        response_ = {'status': 'success', 'message': f'Data download from {name} completed successfully!'}
    except Exception as e:
        response_ = {'status': 'error', 'message': f'Error: {str(e)}'}
    return response_


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
            response = responding(DomesticScraper.GDP, 'GDP')
        else:
            response = responding(DomesticScraper.NBC, 'NBC')

    if "download_button_international" in request.form:
        category = 'international'
        year, month, day = None, None, None

        # Retrieve user input
        sector = request.form.get('International-Sectors')
        choice = request.form.get('international-website')

        path = request.form.get('path-international')

        date_string = request.form.get('date')
        year_inflation = request.form.get('infYear')

        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        month_year = request.form.get('month-year')

        # Convert the date string to a datetime object
        if date_string:
            date_object = datetime.strptime(date_string, '%Y-%m-%d')

            # Extract year, month, and day from the datetime object
            year = date_object.year
            month = date_object.month
            day = date_object.day
        elif year_inflation:
            year = int(year_inflation)
        elif month_year:
            # Parse the input date string into a datetime object
            parsed_date = datetime.strptime(month_year, '%Y-%m')

            # Format the parsed date as 'Month, Year'
            month_year = parsed_date.strftime('%B, %Y')

        scrapping = International.Scraper(choice=choice, destinationDir=path, day=day, start_date=start_date,
                                          end_date=end_date, month=month, year=year, month_year=month_year)

        if sector == 'ExchangeRate':
            response = responding(scrapping.ExchangeRate, 'Exchange Rate')
        elif sector == 'Export':
            response = responding(scrapping.Export, 'Export')
        elif sector == 'OpecBasketPrice':
            response = responding(scrapping.OpecBasketPrice, 'OpecBasket Price')
        elif sector == 'InflationRate':
            response = responding(scrapping.InflationRate, 'Inflation Rate')

    # Store data in Flask session
    session['category'] = category
    session['path'] = path
    session['choice'] = choice

    # Handle other form submissions or render the page as needed
    return render_template("downloadForm.html", response=response)


@app.route('/excelDashboard')
def excelDashBoard():
    return render_template('excelDashBoard.html')


@app.route('/Dashboard')
def streamlit_page():
    """
    Route function for the Streamlit page.

    This function defines a route to a Streamlit page within a web application. It performs the following actions:
    - Retrieves data from the Flask session, specifically the 'category', 'path', and 'choice' variables.
    - Renders the 'dashBoard.html' template, providing the retrieved data as template variables for display on the page.

    Parameters:
        None

    Returns:
        Flask response: Returns the rendered 'dashBoard.html' template with category, path, and choice variables.

    Example Usage:
        This function is invoked when a GET request is made to the '/streamlit' route.
    """
    # Retrieve data from Flask session
    categories = session.get('category')
    destination = session.get('path')
    options = session.get('choice')

    return render_template('dashBoard.html', category=categories, path=destination, choice=options)
