import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import MySQLDatabase, Model, CharField, TextField, DateTimeField
import datetime
from playhouse.shortcuts import model_to_dict

from app.data import education, experiences, hobbies, map_locations, pages, travel_locations

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

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

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']

    timeline_post = TimelinePost.create(
        name=name,
        email=email,
        content=content
    )

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    post = TimelinePost.get_or_none(TimelinePost.id == post_id)

    if post is None:
        return {"error": "Timeline post not found"}, 404

    post.delete_instance()

    return {
        "message": "Timeline post deleted successfully",
        "id": post_id,
    }