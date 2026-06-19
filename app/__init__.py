import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from app.data import education, experiences, hobbies, map_locations, pages, travel_locations

load_dotenv()
app = Flask(__name__)


@app.context_processor
def inject_menu():
    return {
        "pages": pages,
        "active_page": request.endpoint,
    }


@app.route('/')
def index():
    return render_template('index.html', title="Chahana Reddy", url=os.getenv("URL"))


@app.route('/experience')
def experience_page():
    return render_template(
        'experience_page.html',
        title="Experience",
        url=os.getenv("URL"),
        experiences=experiences,
    )


@app.route('/education')
def education_page():
    return render_template(
        'education_page.html',
        title="Education",
        url=os.getenv("URL"),
        education=education,
    )


@app.route('/hobbies')
def hobbies_page():
    return render_template(
        'hobbies_page.html',
        title="Hobbies",
        url=os.getenv("URL"),
        hobbies=hobbies,
    )


@app.route('/places')
def travel_page():
    return render_template(
        'travel_page.html',
        title="Places I've Visited",
        url=os.getenv("URL"),
        travel_locations=travel_locations,
        map_locations=map_locations,
    )
