import streamlit as st
from streamlit_option_menu import option_menu
from processing.visualizations.merchandise_visualizing import dom_merchandise


def bar():
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Settings'],
                               icons=['house', 'gear'], menu_icon="cast", default_index=1)
        selected


