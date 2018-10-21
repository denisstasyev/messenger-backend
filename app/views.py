from flask import request, abort, jsonify, render_template
from app import app


@app.route('/<string:name>/')  # вызывать эту функцию если в браузере путь .../name/
@app.route('/')
def index(name="world"):
    return "Hello, {}!".format(name)


@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == "GET":
        return render_template('form.html')
        # return '''<html><head></head><body>
        # <form method="POST" action="/form/">
        #     <input name="first_name" >
        #     <input name="last_name" >
        #     <input type="submit" >
        # </form>
        # </body></html>'''
    else:
        rv = jsonify(request.form)
        return rv
        # print(request.form)  # request.form - словарь
        # abort(404)
