import peeweedbevolve
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Store,Warehouse

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

@app.route('/store/', methods=['GET'])
def store_index():
    stores = Store.select()
    return render_template('index.html', stores = stores)

@app.route('/store/:<store_id>', methods=['GET'])
def store_show(store_id):
    store = Store.get_by_id(request.args.get('store_id', store_id))
    store_warehouse = Warehouse.select().where(Warehouse.store == store.id)
    return render_template('store_show.html', store = store, store_warehouse = store_warehouse)

@app.route('/store/new', methods=["GET"])
def store_new():
    return render_template('store.html')

@app.route('/store/', methods = ["POST"])
def store_create():
    store_name = request.form.get('store_name')
    store_1 = Store(name=store_name)
    if store_1.save():
        flash("Store succesfully created")
    return redirect(url_for('store_new'))

@app.route('/store/:<store_id>/', methods=['POST'])
def store_update(store_id):
    store = Store.get_by_id(request.args.get('store_id', store_id))
    store.name = request.form.get('store_update_name')
    store.save()
    return redirect(url_for('store_show', store_id = store_id))

@app.route('/warehouse/new', methods=['GET'])
def warehouse_new():
    stores = Store.select()
    return render_template('warehouse.html', stores = stores)

@app.route('/warehouse/', methods=['POST'])
def warehouse_create():
    store = Store.get_by_id(request.form['store_id'])
    w = Warehouse(location=request.form['warehouse_location'], store=store)
    w.save()
    if w.save():
        flash("Warehouse created")
    return redirect(url_for('warehouse_new'))

if __name__ == '__main__':
    app.run()