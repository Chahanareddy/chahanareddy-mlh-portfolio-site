import os
from flask import Flask, render_template
from dotenv import load_dotenv

from app.data import hobbies

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Chahana Reddy", url=os.getenv("URL"))


@app.route('/hobbies')
def hobbies_page():
    return render_template(
        'hobbies_page.html',
        url=os.getenv("URL"),
        hobbies=hobbies,
    )
