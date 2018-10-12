from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

bp = Blueprint('search', __name__,url_prefix='/search')





api_key = '7ecd6a3ceec1b96921b4647095047e8e'


@bp.route('/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        title = request.form['title']
        error = None

        if not title:
            error = 'A name is required.'

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search.get_results', query = title))

    return render_template('search/search.html')



@bp.route('/results/<query>',methods=('GET',))
def get_results(query):

    if query is None :
        query = 'house'

    params = {
        'api_key' : api_key,
        'query' : query
    }
    req = requests.get('https://api.themoviedb.org/3/search/tv',params)


    if not req.ok:
        #print('there was an error in the request : ', req.status_code)
        pass

    reqj = req.json()
    results = []
    if reqj["total_results"] == 0:
        # print('no result corresponding')
        pass
    else:
        for res in reqj["results"]:
            results += [{
                'title' : res['name'],
                'date' : res['first_air_date'],
                'popularity' : res['popularity'],
                'overview' : res['overview'],
                'id' : res['id']
            }]
            print(results[-1])

    return render_template('search/results.html', results=results)