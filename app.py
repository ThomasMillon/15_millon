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
     ORDER BY AAAA_MM_JJ DESC;
     '''
    mycursor.execute(sql)
    Loue___Contrat = mycursor.fetchall()
    return render_template('loue_contrat/show_loue_contrat.html', contrats=Loue___Contrat)

@app.route('/contrat/add', methods=['GET'])
def add_contrat():
    mycursor = get_db().cursor()
    sql='''
    SELECT ID_Etudiant, Nom, Prenom
    FROM Etudiant
    ORDER BY Nom;
    '''
    mycursor.execute(sql)
    etudiants = mycursor.fetchall()
    sql='''
    SELECT Velo.ID_Velo, Type_de_Modele.Libelle_Modele
    FROM Velo
    JOIN Type_de_Modele
    ON Velo.ID_Modele = Type_de_Modele.ID_Modele
    ORDER BY Type_de_Modele.ID_Modele;
    '''
    mycursor.execute(sql)
    velos = mycursor.fetchall()
    return render_template('loue_contrat/add_loue_contrat.html', etudiants = etudiants , velos = velos)

@app.route('/contrat/delete')
def delete_contrat():
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''
    DELETE FROM Loue___Contrat WHERE ID_Contrat = %s;'''
    tuple_param = (id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/contrat/show')

@app.route('/contrat/edit', methods=['GET'])
def edit_contrat():
    id=request.args.get('id', '')

    if id != None :
        id = int(id)
        mycursor = get_db().cursor()
        sql = '''
        SELECT ID_Contrat, ID_Etudiant, ID_Velo, AAAA_MM_JJ, Duree_location, Tarif
        FROM Loue___Contrat
        WHERE ID_Contrat = %s;
        '''
        tuple_param = (id)
        mycursor.execute(sql, tuple_param)
        get_db().commit()
        contrat = mycursor.fetchone()
        mycursor = get_db().cursor()
        sql = '''
            SELECT ID_Etudiant, Nom, Prenom
            FROM Etudiant
            ORDER BY Nom;
            '''
        mycursor.execute(sql)
        etudiants = mycursor.fetchall()
        sql = '''
            SELECT Velo.ID_Velo, Type_de_Modele.Libelle_Modele
            FROM Velo
            JOIN Type_de_Modele
            ON Velo.ID_Modele = Type_de_Modele.ID_Modele
            ORDER BY Type_de_Modele.ID_Modele;
            '''
        mycursor.execute(sql)
        velos = mycursor.fetchall()
    else :
        contrat = []
    return render_template('loue_contrat/edit_loue_contrat.html', contrat=contrat, etudiants=etudiants, velos=velos)

@app.route('/contrat/add', methods=['POST'])
def valid_add_contrat():
    etudiant = request.form.get('etudiant','')
    velo = request.form.get('velo', '')
    date_debut = request.form.get('date_debut', '')
    duree = request.form.get('duree', '')
    tarif = request.form.get('tarif', '')

    mycursor = get_db().cursor()
    sql = '''
    INSERT INTO Loue___Contrat(ID_Contrat, ID_Etudiant, ID_Velo, AAAA_MM_JJ, Duree_location, Tarif) VALUES (NULL, %s, %s, %s, %s, %s);
    '''
    tuple_param = (etudiant, velo, date_debut, duree, tarif)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/contrat/show')


@app.route('/contrat/edit', methods=['POST'])
def valid_edit_contrat():
    id = request.form.get('id')
    etudiant = request.form.get('etudiant')
    velo = request.form.get('velo')
    date_debut = request.form.get('date_debut')
    duree = request.form.get('duree')
    tarif = request.form.get('tarif')

    mycursor = get_db().cursor()
    sql = '''
    UPDATE Loue___Contrat SET ID_Etudiant = %s, ID_Velo = %s, AAAA_MM_JJ = %s, Duree_location = %s, Tarif = %s WHERE ID_Contrat = %s;
    '''
    tuple_param = (etudiant, velo, date_debut, duree, tarif, id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/contrat/show')