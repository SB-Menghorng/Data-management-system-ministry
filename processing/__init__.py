from flask import Flask
from processing.constant import static_folder

app = Flask(__name__, static_folder=static_folder)
app.config["SECRET_KEY"] = "b4324232a7c49f309373ff24"

from processing import routes
