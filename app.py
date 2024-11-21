from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

from flask import session, g
import pymysql.cursors

#mysql --user=tmillon  --password=mdp --host=serveurmysql --database=BDD_tmillon



def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="serveurmysql.iut-bm.univ-fcomte.fr",                 # à modifier
            user="tmillon",                     # à modifier
            password="mdp",                # à modifier
            database="BDD_tmillon",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def show_layout():  # put application's code here
    return render_template('layout.html')


if __name__ == '__main__':
    app.run()


@app.route('/loue_contrat/show', methods=['GET'])
def show_loue_contrat():
    return render_template('loue_contrat/show_loue_contrat.html')