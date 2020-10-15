import peeweedbevolve
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Store

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store/', methods=["GET"])
def store_new():
    return render_template('store.html')

@app.route('/store/', methods = ["POST"])
def store_create():
    store_name = request.form.get('store_name')
    store_1 = Store(name=store_name)
    if store_1.save():
        flash("Store succesfully created")
    return redirect(url_for('store_new'))

if __name__ == '__main__':
    app.run()