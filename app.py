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


@app.route('/contrat/show', methods=['GET'])
def show_loue_contrat():
    mycursor = get_db().cursor()
    sql = '''
    SELECT ID_Contrat, ID_Etudiant, ID_Velo, AAAA_MM_JJ, Duree_location, Tarif
     FROM Loue___Contrat
     ORDER BY AAAA_MM_JJ DESC'''
    mycursor.execute(sql)
    Loue___Contrat = mycursor.fetchall()
    return render_template('loue_contrat/show_loue_contrat.html', contrats=Loue___Contrat)

@app.route('/contrat/add', methods=['GET'])
def add_contrat():
    return render_template('loue_contrat/add_loue_contrat.html')

@app.route('/contrat/delete')
def delete_contrat():
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''
    DELETE FROM Loue___Contrat WHERE ID_Contrat = %s'''
    tuple_param = (id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/contrat/show')