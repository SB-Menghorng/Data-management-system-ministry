import subprocess
from processing.constant import dashboard, excelDashboard
import psutil

# Define the Streamlit processes globally
streamlit_process1 = None
streamlit_process2 = None


def start_dashboard():
    """
    Function to start the dashboard Streamlit application in a separate thread.
    """
    global streamlit_process1

    if streamlit_process1 is None or not psutil.pid_exists(streamlit_process1.pid):
        try:
            streamlit_process1 = subprocess.Popen(["streamlit", "run", dashboard, '--server.port', '90'],
                                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = streamlit_process1.communicate()

            if streamlit_process1.returncode != 0:
                print("Error running Dashboard Streamlit app. Return code:", streamlit_process1.returncode)
                print("Streamlit error output:", err)
            else:
                print("Dashboard Streamlit output:", out)
        except Exception as e:
            print("Error starting Dashboard Streamlit app:", str(e))
    else:
        print("Dashboard Streamlit is already running")


def start_excel():
    """
    Function to start the excel Streamlit application in a separate thread.
    """
    global streamlit_process2

    if streamlit_process2 is None or not psutil.pid_exists(streamlit_process2.pid):
        try:
            streamlit_process2 = subprocess.Popen(["streamlit", "run", excelDashboard, '--server.port', '80'],
                                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = streamlit_process2.communicate()

            if streamlit_process2.returncode != 0:
                print("Error running Excel Streamlit app. Return code:", streamlit_process2.returncode)
                print("Streamlit error output:", err)
            else:
                print("Excel Streamlit output:", out)
        except Exception as e:
            print("Error starting Excel Streamlit app:", str(e))
    else:
        print("Excel Streamlit is already running")


if __name__ == "__main__":
    start_dashboard()
    start_excel()
