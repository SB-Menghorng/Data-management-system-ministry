import streamlit as st
from streamlit_option_menu import option_menu
from processing.visualizations.merchandise_visualizing import dom_merchandise
from streamlit_app import shared_data


def bar():
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Settings'],
                               icons=['house', 'gear'], menu_icon="cast", default_index=1)
        selected

path = shared_data['path']
def domestic():
    dom_merchandise(path)