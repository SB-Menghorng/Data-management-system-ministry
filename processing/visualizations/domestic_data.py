# domestic_data.py
from processing.visualizations.merchandise_visualizing import dom_merchandise
from streamlit_app import shared_data


class DomesticData:
    def __init__(self, path=None, choice=None):
        self.path = path
        self.choice = choice

    def get_path_and_choice(self):
        # Access shared variable to retrieve path and choice
        path = shared_data['path']
        choice = shared_data['choice']
        return path, choice

    def display_visualize(self):
        # Retrieve path and choice from shared variable
        self.path, self.choice = self.get_path_and_choice()
        if self.choice == 'merchandise trade':
            dom_merchandise(self.path)
