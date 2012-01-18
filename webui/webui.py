from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import urllib

DEBUG = True
SECRET_KEY = 'knotted noodle'

app = Flask (__name__)
app.config.from_object (__name__)

@app.route ('/')
def list_proj():
    entries = [x.strip() for x in open ('proj_list', 'r').readlines()]
    return render_template ('proj_list.html', entries = entries)

@app.route ('/proj/<name>')
def view_proj (name):
    return 'Proj: ' + name

@app.route ('/add', methods=['POST'])
def add_entry():
    with open ('proj_list', 'a') as projlist:
	projlist.write (request.form['title'] + '\n')
    flash ('New project was successfully created')
    return redirect (url_for('list_proj'))

@app.route ('/table')
def show_table():
    lines = open ('table-desc', 'r').readlines()
    xs = lines[0].split()
    ys = lines[0].split()
    return render_template ('table.html', xs=xs, ys=ys)

@app.route ('/complex/<x>/<y>')
def view_complex (x, y):
    return 'hello: ' + x + ',' + y

if '__main__' == __name__:
    app.run()



