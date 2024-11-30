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
            host="serveurmysql.iut-bm.univ-fcomte.fr",
            user="tmillon",
            password="mdp",
            database="BDD_tmillon",
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
def show_layout():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run()

"""
==========Loue / Contrat==========
"""
@app.route('/contrat/show', methods=['GET'])
def show_loue_contrat():
    mycursor = get_db().cursor()
    sql = '''
    SELECT Loue___Contrat.ID_Contrat, Loue___Contrat.ID_Etudiant, Loue___Contrat.ID_Velo, Loue___Contrat.AAAA_MM_JJ, Loue___Contrat.Duree_location, Loue___Contrat.Tarif, Etudiant.Nom, Type_de_Modele.Libelle_Modele
     FROM Loue___Contrat
     LEFT JOIN Velo
     ON Loue___Contrat.ID_Velo = Velo.ID_Velo
    JOIN Type_de_Modele
    ON Velo.ID_Modele = Type_de_Modele.ID_Modele
    JOIN Etudiant
    ON Loue___Contrat.ID_Etudiant = Etudiant.ID_Etudiant
     ORDER BY AAAA_MM_JJ DESC;
     '''
    mycursor.execute(sql)
    Loue___Contrat = mycursor.fetchall()
    sql = '''
    SELECT Marque.Libelle_Marque, COUNT(Marque.ID_Marque) AS nbmLoue
    FROM Loue___Contrat
    LEFT JOIN Velo
    ON Loue___Contrat.ID_Velo = Velo.ID_Velo
    JOIN Type_de_Modele
    ON Velo.ID_Modele = Type_de_Modele.ID_Modele
    JOIN Marque
    ON Type_de_Modele.ID_Marque = Marque.ID_Marque
    WHERE MONTH(Loue___Contrat.AAAA_MM_JJ) = MONTH(NOW())
    GROUP BY Marque.ID_Marque
    ORDER BY nbmLoue DESC;
    '''
    mycursor.execute(sql)
    meilleureMarque = mycursor.fetchall()

    sql = '''
        SELECT Marque.Libelle_Marque, COUNT(Marque.ID_Marque) AS nbmLoue
        FROM Loue___Contrat
        LEFT JOIN Velo
        ON Loue___Contrat.ID_Velo = Velo.ID_Velo
        JOIN Type_de_Modele
        ON Velo.ID_Modele = Type_de_Modele.ID_Modele
        JOIN Marque
        ON Type_de_Modele.ID_Marque = Marque.ID_Marque
        WHERE MONTH(Loue___Contrat.AAAA_MM_JJ) = MONTH(DATE_ADD(NOW(), INTERVAL -1 MONTH))
        GROUP BY Marque.ID_Marque
        ORDER BY nbmLoue DESC;
        '''
    mycursor.execute(sql)
    moisDernier = mycursor.fetchall()
    return render_template('loue_contrat/show_loue_contrat.html', contrats=Loue___Contrat, marque=meilleureMarque, moisDernier=moisDernier)

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


"""
==========Modèle==========
"""


"""
==========Réparation==========
"""
@app.route('/reparation/show', methods=['GET'])
def show_reparation():
    mycursor = get_db().cursor()
    sql = '''
    SELECT Reparation.ID_Reparation, Reparation.Prix_Total, Reparation.Date_Reparation, Reparation.ID_Velo, Type_de_Modele.Libelle_Modele, Reparation.ID_Type, TypeReparation.Libelle_Type, COUNT(Piece.ID_Piece) AS NbPiece
     FROM Reparation
     JOIN Velo ON Reparation.ID_Velo = Velo.ID_Velo
     JOIN Type_de_Modele ON Velo.ID_Modele = Type_de_Modele.ID_Modele
     JOIN TypeReparation ON Reparation.ID_Type = TypeReparation.ID_Type
     JOIN Change_piece ON Reparation.ID_Reparation = Change_piece.ID_Reparation
     JOIN Piece ON Change_piece.ID_Piece = Piece.ID_Piece
     GROUP BY Reparation.ID_Reparation
     ORDER BY Date_Reparation DESC'''
    mycursor.execute(sql)
    Reparation = mycursor.fetchall()
    mycursor = get_db().cursor()
    sql = '''
            SELECT Type_de_Modele.Libelle_Modele, COUNT(Reparation.ID_Reparation) AS Nombre_Reparations
            FROM Reparation
            JOIN Velo ON Reparation.ID_Velo = Velo.ID_Velo
            JOIN Type_de_Modele ON Velo.ID_Modele = Type_de_Modele.ID_Modele
            GROUP BY Type_de_Modele.Libelle_Modele
            ORDER BY Nombre_Reparations DESC
            LIMIT 1;
        '''
    mycursor.execute(sql)
    modele = mycursor.fetchone()

    # Si aucun modèle n'est trouvé (pas de réparations), on envoie un message par défaut
    if modele is None:
        modele = {'Libelle_Modele': 'Aucun modèle', 'Nombre_Reparations': 0}

    mycursor = get_db().cursor()
    sql = '''
            SELECT ROUND(AVG(Prix_Total), 2) AS Prix_Moyen
            FROM Reparation;
        '''
    mycursor.execute(sql)
    prix_moyen = mycursor.fetchone()
    print(prix_moyen)

    mycursor = get_db().cursor()
    sql = '''
            SELECT Type_de_Modele.Libelle_Modele, ROUND(AVG(Reparation.Prix_Total), 2) AS Prix
            FROM Reparation
            JOIN Velo ON Reparation.ID_Velo = Velo.ID_Velo
            JOIN Type_de_Modele ON Velo.ID_Modele = Type_de_Modele.ID_Modele
            GROUP BY Type_de_Modele.Libelle_Modele
            ORDER BY Prix DESC
            LIMIT 1;
    '''
    mycursor.execute(sql)
    modele_cher = mycursor.fetchone()

    return render_template('reparation/show_reparation.html', reparations=Reparation, modele=modele, prix_moyen=prix_moyen, prix_cher=modele_cher)


@app.route('/reparation/add', methods=['GET'])
def add_reparation():
    mycursor = get_db().cursor()
    sql='''
    SELECT Velo.ID_Velo, Type_de_Modele.Libelle_Modele
    FROM Velo
    JOIN Type_de_Modele
    ON Velo.ID_Modele = Type_de_Modele.ID_Modele
    ORDER BY Velo.ID_Velo;
    '''
    mycursor.execute(sql)
    velos = mycursor.fetchall()
    sql='''
    SELECT ID_Type, Libelle_Type
    FROM TypeReparation
    ORDER BY ID_Type;
    '''
    mycursor.execute(sql)
    types = mycursor.fetchall()
    return render_template('reparation/add_reparation.html', velos = velos , types = types)

@app.route('/reparation/add', methods=['POST'])
def valid_add_reparation():
    prix = request.form.get('prix','')
    date = request.form.get('date', '')
    velo = request.form.get('velo', '')
    type = request.form.get('type', '')

    mycursor = get_db().cursor()
    sql = '''
    INSERT INTO Reparation(ID_Reparation, Prix_Total, Date_Reparation, ID_Velo, ID_Type) VALUES (NULL, %s, %s, %s, %s);
    '''
    tuple_param = (prix, date, velo, type)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/reparation/show')

@app.route('/reparation/delete')
def delete_reparation():
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''
    SELECT ID_Reparation
    FROM Change_piece
    WHERE ID_Reparation = %s'''
    tuple_param = (id)
    change = mycursor.execute(sql, tuple_param)
    if change > 0:
        message = "Impossible de supprimer la réparation d'id : " + id + " car elle est utilisée dans l'entité 'Change_piece'"
        flash(message, 'alert-warning')
    else :
        mycursor = get_db().cursor()
        sql = '''
        DELETE FROM Reparation WHERE ID_Reparation = %s
        '''
        tuple_param = (id)
        mycursor.execute(sql, tuple_param)
        get_db().commit()
    return redirect('/reparation/show')


@app.route('/reparation/edit', methods=['GET'])
def edit_reparation():
    id=request.args.get('id', '')

    if id != None :
        id = int(id)
        mycursor = get_db().cursor()
        sql = '''
        SELECT ID_Reparation, Prix_Total, Date_Reparation, ID_Velo, ID_Type
        FROM Reparation
        WHERE ID_Reparation = %s;
        '''
        tuple_param = (id)
        mycursor.execute(sql, tuple_param)
        get_db().commit()
        reparation = mycursor.fetchone()
        mycursor = get_db().cursor()
        sql = '''
            SELECT Velo.ID_Velo, Type_de_Modele.Libelle_Modele
            FROM Velo
            JOIN Type_de_Modele
            ON Velo.ID_Modele = Type_de_Modele.ID_Modele
            ORDER BY Velo.ID_Velo;
            '''
        mycursor.execute(sql)
        velos = mycursor.fetchall()
        sql = '''
            SELECT ID_Type, Libelle_Type
            FROM TypeReparation
            ORDER BY ID_Type;
            '''
        mycursor.execute(sql)
        types = mycursor.fetchall()
    else :
        reparation = []
    return render_template('reparation/edit_reparation.html', reparation=reparation, velos=velos, types=types)


@app.route('/reparation/edit', methods=['POST'])
def valid_edit_reparation():
    id = request.form.get('id')
    prix = request.form.get('prix')
    date = request.form.get('date')
    velo = request.form.get('velo')
    type = request.form.get('type')

    mycursor = get_db().cursor()
    sql = '''
    UPDATE Reparation SET Prix_Total = %s, Date_Reparation = %s, ID_Velo = %s, ID_Type = %s WHERE ID_Reparation = %s;
    '''
    tuple_param = (prix, date, velo, type, id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/reparation/show')


"""
==========Vélo==========
"""
