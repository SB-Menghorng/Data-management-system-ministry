# Define your functions for different dashboards
import streamlit as st


def dashboard1():
    st.write("Shared data file does not exist or is empty.")


def dashboard2():
    st.write("This is Dashboard 2")
    # Add content for Dashboard 2 here


def dashboard3():
    # Create a Streamlit dashboard with three columns and two rows
    col1, col2, col3 = st.columns(3)  # Three columns
    row1, row2 = st.columns(2)  # Two rows

    # Column 1, Row 1 content
    with col1:
        st.header("Column 1, Row 1")
        # Add your content for this section

    # Column 2, Row 1 content
    with col2:
        st.header("Column 2, Row 1")
        # Add your content for this section

    # Column 3, Row 1 content
    with col3:
        st.header("Column 3, Row 1")
        # Add your content for this section

    # Column 1, Row 2 content
    with row1:
        st.header("Column 1, Row 2")
        # Add your content for this section

    # Column 2, Row 2 content
    with row2:
        st.header("Column 2, Row 2")
        # Add your content for this section

    # Column 2, Row 2 content
    with row2:
        st.header("Column 3, Row 2")
        # Add your content for this section