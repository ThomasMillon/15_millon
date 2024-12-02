from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

from flask import session, g
import pymysql.cursors

#mysql --user=tmillon  --password=mdp --host=serveurmysql.iut-bm.univ-fcomte.fr --database=BDD_tmillon



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
@app.route('/contrat/show', methods=['GET', 'POST'])
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

    sql = '''
        SELECT 
        MIN(AAAA_MM_JJ) AS minDate, 
        MAX(AAAA_MM_JJ) AS maxDate, 
        MIN(Duree_location) AS minDuree, 
        MAX(Duree_location) AS maxDuree, 
        MIN(Tarif) AS minTarif, 
        MAX(Tarif) AS maxTarif
        FROM Loue___Contrat;
        '''
    mycursor.execute(sql)
    valeurs = mycursor.fetchone()

    etudiant = request.form.get('etudiant', '')
    velo = request.form.get('velo', '')
    date_debut_min = request.form.get('date_debut_min', '')
    if date_debut_min == '':
        date_debut_min = valeurs["minDate"]
    date_debut_max = request.form.get('date_debut_max', '')
    if date_debut_max == '':
        date_debut_max = valeurs["maxDate"]
    duree_min = request.form.get('duree_min', '')
    if duree_min == '':
        duree_min = valeurs["minDuree"]
    duree_max = request.form.get('duree_max', '')
    if duree_max == '':
        duree_max = valeurs["maxDuree"]
    tarif_min = request.form.get('tarif_min', '')
    if tarif_min == '':
        tarif_min = valeurs["minTarif"]
    tarif_max = request.form.get('tarif_max', '')
    if tarif_max == '':
        tarif_max = valeurs["maxTarif"]

    valeurs["etudiant"] = etudiant
    valeurs["velo"] = velo
    valeurs["minDate"] = date_debut_min
    valeurs["maxDate"] = date_debut_max
    valeurs["minDuree"] = duree_min
    valeurs["maxDuree"] = duree_max
    valeurs["minTarif"] = tarif_min
    valeurs["maxTarif"] = tarif_max

    sql = '''
        SELECT Loue___Contrat.ID_Contrat, Loue___Contrat.ID_Etudiant, Loue___Contrat.ID_Velo, Loue___Contrat.AAAA_MM_JJ, Loue___Contrat.Duree_location, Loue___Contrat.Tarif, Etudiant.Nom, Type_de_Modele.Libelle_Modele
        FROM Loue___Contrat
        LEFT JOIN Velo
        ON Loue___Contrat.ID_Velo = Velo.ID_Velo
        JOIN Type_de_Modele
        ON Velo.ID_Modele = Type_de_Modele.ID_Modele
        JOIN Etudiant
        ON Loue___Contrat.ID_Etudiant = Etudiant.ID_Etudiant
        WHERE Etudiant.Nom LIKE %s
        AND Type_de_Modele.Libelle_Modele LIKE %s
        AND Loue___Contrat.AAAA_MM_JJ BETWEEN %s AND %s
        AND Loue___Contrat.Duree_location BETWEEN %s AND %s
        AND Loue___Contrat.Tarif BETWEEN %s AND %s
        ORDER BY AAAA_MM_JJ DESC;
        '''
    tuple_param = (f'%{etudiant}%', f'%{velo}%', date_debut_min, date_debut_max, duree_min, duree_max, tarif_min, tarif_max)
    mycursor.execute(sql, tuple_param)
    filters = mycursor.fetchall()

    sql = '''
            SELECT COUNT(Loue___Contrat.ID_Contrat) AS nbrElement
            FROM Loue___Contrat
            LEFT JOIN Velo
            ON Loue___Contrat.ID_Velo = Velo.ID_Velo
            JOIN Type_de_Modele
            ON Velo.ID_Modele = Type_de_Modele.ID_Modele
            JOIN Etudiant
            ON Loue___Contrat.ID_Etudiant = Etudiant.ID_Etudiant
            WHERE Etudiant.Nom LIKE %s
            AND Type_de_Modele.Libelle_Modele LIKE %s
            AND Loue___Contrat.AAAA_MM_JJ BETWEEN %s AND %s
            AND Loue___Contrat.Duree_location BETWEEN %s AND %s
            AND Loue___Contrat.Tarif BETWEEN %s AND %s
            ORDER BY AAAA_MM_JJ DESC;
            '''
    tuple_param = (f'%{etudiant}%', f'%{velo}%', date_debut_min, date_debut_max, duree_min, duree_max, tarif_min, tarif_max)
    mycursor.execute(sql, tuple_param)
    nbr = mycursor.fetchone()

    return render_template('loue_contrat/show_loue_contrat.html', contrats=Loue___Contrat, marque=meilleureMarque, moisDernier=moisDernier, valeurs=valeurs, filters = filters, nombreTrouve=nbr)

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
    sql='''
    SELECT COUNT(ID_Contrat)
    FROM Loue___Contrat
    WHERE ID_Velo = %s 
    AND (AAAA_MM_JJ BETWEEN %s AND DATE_ADD(%s, INTERVAL %s DAY) 
    OR DATE_ADD(AAAA_MM_JJ, INTERVAL %s DAY) BETWEEN %s AND DATE_ADD(%s, INTERVAL %s DAY)
    OR %s BETWEEN AAAA_MM_JJ AND DATE_ADD(AAAA_MM_JJ, INTERVAL Duree_location DAY)
    OR DATE_ADD(%s, INTERVAL %s DAY) BETWEEN AAAA_MM_JJ AND DATE_ADD(AAAA_MM_JJ, INTERVAL Duree_location DAY));
    '''
    tuple_param = (velo, date_debut, date_debut, duree, duree, date_debut, date_debut, duree, date_debut, date_debut, duree)
    mycursor.execute(sql, tuple_param)
    nbContrat = mycursor.fetchone()
    if nbContrat == 0 :

        sql = '''
        INSERT INTO Loue___Contrat(ID_Contrat, ID_Etudiant, ID_Velo, AAAA_MM_JJ, Duree_location, Tarif) VALUES (NULL, %s, %s, %s, %s, %s);
        '''
        tuple_param = (etudiant, velo, date_debut, duree, tarif)
        mycursor.execute(sql, tuple_param)
        get_db().commit()
    else :
        message = "Action impossible : Il existe déjà une location pour ce vélo à cette date"
        flash(message, 'alert-warning')
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
        SELECT COUNT(ID_Contrat)
        FROM Loue___Contrat
        WHERE ID_Velo = %s 
        AND (AAAA_MM_JJ BETWEEN %s AND DATE_ADD(%s, INTERVAL %s DAY) 
        OR DATE_ADD(AAAA_MM_JJ, INTERVAL %s DAY) BETWEEN %s AND DATE_ADD(%s, INTERVAL %s DAY)
        OR %s BETWEEN AAAA_MM_JJ AND DATE_ADD(AAAA_MM_JJ, INTERVAL Duree_location DAY)
        OR DATE_ADD(%s, INTERVAL %s DAY) BETWEEN AAAA_MM_JJ AND DATE_ADD(AAAA_MM_JJ, INTERVAL Duree_location DAY));
        '''
    tuple_param = (
    velo, date_debut, date_debut, duree, duree, date_debut, date_debut, duree, date_debut, date_debut, duree)
    mycursor.execute(sql, tuple_param)
    nbContrat = mycursor.fetchone()
    if nbContrat == 0:
        sql = '''
        UPDATE Loue___Contrat SET ID_Etudiant = %s, ID_Velo = %s, AAAA_MM_JJ = %s, Duree_location = %s, Tarif = %s WHERE ID_Contrat = %s;
        '''
        tuple_param = (etudiant, velo, date_debut, duree, tarif, id)
        mycursor.execute(sql, tuple_param)
        get_db().commit()
    else :
        message = "Action impossible : Il existe déjà une location pour ce vélo à cette date"
        flash(message, 'alert-warning')
    return redirect('/contrat/show')


@app.route('/contrat/filter', methods=['POST'])
def filter_contrat():
    mycursor = get_db().cursor()
    etudiant = request.args.get('etudiant', '')
    velo = request.args.get('velo', '')
    date_debut_min = request.args.get('date_debut_min', '')

    date_debut_max = request.args.get('date_debut_max', '')

    duree_min = request.args.get('duree_min', '')

    duree_max = request.args.get('duree_max', '')

    tarif_min = request.args.get('tarif_min', '')

    tarif_max = request.args.get('tarif_max', '')


    sql = '''
            SELECT Loue___Contrat.ID_Contrat, Loue___Contrat.ID_Etudiant, Loue___Contrat.ID_Velo, Loue___Contrat.AAAA_MM_JJ, Loue___Contrat.Duree_location, Loue___Contrat.Tarif, Etudiant.Nom, Type_de_Modele.Libelle_Modele
            FROM Loue___Contrat
            LEFT JOIN Velo
            ON Loue___Contrat.ID_Velo = Velo.ID_Velo
            JOIN Type_de_Modele
            ON Velo.ID_Modele = Type_de_Modele.ID_Modele
            JOIN Etudiant
            ON Loue___Contrat.ID_Etudiant = Etudiant.ID_Etudiant
            WHERE Type_de_Modele.Libelle_Modele LIKE %s
            AND Etudiant.Nom LIKE %s
            AND Loue___Contrat.AAAA_MM_JJ BETWEEN %s AND %s
            AND Loue___Contrat.Duree_location BETWEEN %s AND %s
            AND Loue___Contrat.Tarif BETWEEN %s AND %s
            ORDER BY AAAA_MM_JJ DESC;
            '''
    tuple_param = (
    f'%{etudiant}%', f'%{velo}%', date_debut_min, date_debut_max, duree_min, duree_max, tarif_min, tarif_max)
    mycursor.execute(sql, tuple_param)
    filters = mycursor.fetchall()



"""
==========Modèle==========
"""

@app.route('/typedemodele/show', methods=['GET'])
def show_typedemodele_contrat():
    mycursor = get_db().cursor()
    sql = '''
    SELECT Type_de_Modele.ID_Modele, Type_de_Modele.Libelle_Modele, Type_de_Modele.ID_Marque, Marque.Libelle_Marque, Type_de_Modele.Vitesse_max
     FROM Type_de_Modele
     JOIN Marque ON Type_de_Modele.ID_Marque = Marque.ID_Marque
     ORDER BY Libelle_Modele DESC'''
    mycursor.execute(sql)
    Type_de_Modele = mycursor.fetchall()
    sql = '''
    SELECT COUNT(Type_de_Modele.ID_Modele) AS nmbre_modele, Type_de_Modele.ID_Marque, Marque.Libelle_Marque
    FROM Type_de_Modele
    JOIN Marque ON Type_de_Modele.ID_Marque = Marque.ID_Marque
    GROUP BY Type_de_Modele.ID_Marque;
    '''
    mycursor.execute(sql)
    nombre_modele_par_marque = mycursor.fetchall()
    sql = '''
    SELECT Type_de_Modele.Vitesse_max, Type_de_Modele.Libelle_Modele
    FROM Type_de_Modele
    ORDER BY Vitesse_max DESC
    '''
    mycursor.execute(sql)
    veloleplusrapide= mycursor.fetchone()
    return render_template('type_de_modele/show_type_de_modele.html', modeles=Type_de_Modele, nombre_modele_par_marque=nombre_modele_par_marque, veloleplusrapide=veloleplusrapide)

@app.route('/typedemodele/add', methods=['GET'])
def add_typedemodele():
    mycursor = get_db().cursor()
    sql = '''
        SELECT ID_Modele, Libelle_Modele, ID_Marque, Vitesse_max
        FROM Type_de_Modele
        ORDER BY Libelle_Modele;
        '''
    mycursor.execute(sql)
    modeles = mycursor.fetchall()

    sql = '''
        SELECT ID_Marque, Libelle_Marque
        FROM Marque
        '''
    mycursor.execute(sql)
    marques = mycursor.fetchall()
    return render_template('type_de_modele/add_type_de_modele.html', marques=marques)
    #print('''affichage du formulaire pour saisir un type de modèle''')
    #return render_template('type_de_modele/add_type_de_modele.html')

@app.route('/typedemodele/add', methods=['POST'])
def valid_add_typedemodele():
    print('''ajout du type de modele dans le tableau''')
    libelle = request.form.get('libelle')
    id_marque = request.form.get('id_marque')
    vitt = request.form.get('vitt')

    message = 'libelle :' + libelle + ' - marque :' + id_marque + ' - vittesse :' + vitt
    print(message)
    mycursor = get_db().cursor()
    sql = ''' 
    INSERT INTO Type_de_Modele(ID_Modele, Libelle_Modele, ID_Marque,Vitesse_max) VALUES (NULL, %s,%s,%s );
    '''
    tuple_param=(libelle, id_marque, vitt)
    mycursor.execute(sql,tuple_param)

    get_db().commit()
    return redirect('/typedemodele/show')

@app.route('/typedemodele/delete')
def delete_typedemodele():

    print('''suppression d'un type de modèle''')
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql='''
    SELECT COUNT(Velo.ID_Modele) AS velodecemodele FROM Velo WHERE ID_Modele=%s;
    '''
    mycursor.execute(sql,id)
    verif=mycursor.fetchone()
    verif=verif['velodecemodele']
    #flash(verif, 'alert-warning')
    #return redirect('/typedemodele/show')
    if int(verif)>0:
        messageerreur="il y a encore un élément de la table vélo qui fait référence à ce modèle"
        flash(messageerreur, 'alert-warning')
    else :
        sql='''
        DELETE FROM Type_de_Modele WHERE ID_Modele = %s;
        '''
        tuple_param=(id)
        mycursor.execute(sql,tuple_param)
        get_db().commit()
    return redirect('/typedemodele/show')







@app.route('/typedemodele/edit', methods=['GET'])
def edit_typedemodele():
    id = request.args.get('id', '')
    if id != None:
        mycursor = get_db().cursor()
        sql = '''
            SELECT ID_Modele, Libelle_Modele, ID_Marque, Vitesse_max
            FROM Type_de_Modele
            WHERE ID_Modele = %s;
            '''
        tuple_param = (id)
        mycursor.execute(sql, tuple_param)
        get_db().commit()
        modele = mycursor.fetchone()
        mycursor = get_db().cursor()
        sql = '''
                SELECT ID_Marque, Libelle_Marque
                FROM Marque
                ORDER BY Libelle_Marque;
                '''
        mycursor.execute(sql)
        marques = mycursor.fetchall()
    else:
        modele = []
    print(modele)
    return render_template('type_de_modele/edit_type_de_modele.html', modele=modele, marques=marques)

@app.route('/typedemodele/edit', methods=['POST'])
def valid_edit_typedemodele():
    id = request.form.get('id')
    libelle = request.form.get('libelle')
    id_marque = request.form.get('id_marque')
    vitt = request.form.get('vitt')

    mycursor = get_db().cursor()
    sql = '''
    UPDATE Type_de_Modele SET Libelle_Modele = %s, ID_Marque = %s, Vitesse_max = %s WHERE ID_Modele = %s;
    '''
    print(id)
    tuple_param = (libelle, id_marque, vitt, id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/typedemodele/show')



"""
==========Réparation==========
"""


@app.route('/reparation/show', methods=['GET'])
def show_reparation():
    mycursor = get_db().cursor()

    filtre_modele = request.args.get('filtre_modele', '')
    filtre_date_min = request.args.get('filtre_date_min', None)
    filtre_date_max = request.args.get('filtre_date_max', None)
    filtre_prix_min = request.args.get('filtre_prix_min', None)
    filtre_prix_max = request.args.get('filtre_prix_max', None)

    sql = '''
    SELECT Reparation.ID_Reparation,
            Reparation.Prix_Total,
            Reparation.Date_Reparation,
            Reparation.ID_Velo,
            Type_de_Modele.Libelle_Modele,
            Reparation.ID_Type,
            TypeReparation.Libelle_Type
    FROM Reparation
    JOIN Velo ON Reparation.ID_Velo = Velo.ID_Velo
    JOIN Type_de_Modele ON Velo.ID_Modele = Type_de_Modele.ID_Modele
    JOIN TypeReparation ON Reparation.ID_Type = TypeReparation.ID_Type
    '''

    filtre = []

    if filtre_modele:
        sql += " AND Type_de_Modele.Libelle_Modele LIKE %s"
        filtre.append("%" + filtre_modele + "%")
    if filtre_date_min:
        sql += " AND Reparation.Date_Reparation >= %s"
        filtre.append(filtre_date_min)
    if filtre_date_max:
        sql += " AND Reparation.Date_Reparation <= %s"
        filtre.append(filtre_date_max)
    if filtre_prix_min:
        sql += " AND Reparation.Prix_Total >= %s"
        filtre.append(int(filtre_prix_min))
        print(filtre_prix_min)
    if filtre_prix_max:
        sql += " AND Reparation.Prix_Total <= %s"
        filtre.append(int(filtre_prix_max))

    sql += " ORDER BY Date_Reparation DESC"

    mycursor.execute(sql, filtre)
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

    if modele is None:
        modele = {'Libelle_Modele': 'Aucun modèle', 'Nombre_Reparations': 0}

    mycursor = get_db().cursor()
    sql = '''
            SELECT ROUND(AVG(Prix_Total), 2) AS Prix_Moyen
            FROM Reparation;
        '''
    mycursor.execute(sql)
    prix_moyen = mycursor.fetchone()

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

    return render_template('reparation/show_reparation.html',
        reparations=Reparation, modele=modele, prix_moyen=prix_moyen, prix_cher=modele_cher,
        filtres={
            'filtre_modele': filtre_modele,
            'filtre_date_min': filtre_date_min,
            'filtre_date_max': filtre_date_max,
            'filtre_prix_min': filtre_prix_min,
            'filtre_prix_max': filtre_prix_max,
        }
    )


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
@app.route('/Velo/show')
def show_velo():
    mycursor = get_db().cursor()
    sql = '''SELECT Velo.ID_Velo AS id_V, Type_de_Modele.Libelle_Modele AS modele, Velo.Prix, Couleur.Libelle_Couleur AS couleur
             FROM Velo
             INNER JOIN Couleur ON Velo.ID_Couleur = Couleur.ID_Couleur
             INNER JOIN Type_de_Modele ON Velo.ID_Modele = Type_de_Modele.ID_Modele
             ORDER BY id_V, modele;'''
    mycursor.execute(sql)

    Velo = mycursor.fetchall()
    sql = '''SELECT MIN(Velo.Prix) AS Prix_min, Velo.ID_Velo AS id_V, Type_de_Modele.Libelle_Modele AS L_M
             FROM Velo
             LEFT JOIN  Type_de_Modele ON Velo.ID_Modele = Type_de_Modele.ID_Modele
             GROUP BY ID_Velo, Libelle_Modele
             ORDER BY Prix_min;'''
    mycursor.execute(sql)
    prix_pas_cher = mycursor.fetchone()
    sql = '''SELECT Velo.ID_Velo, Type_de_Modele.Libelle_Modele, MAX(Velo.Prix) AS Prix_max
             FROM Velo
             RIGHT JOIN Type_de_Modele ON Velo.ID_Modele = Type_de_Modele.ID_Modele
             GROUP BY Velo.ID_Velo, Type_de_Modele.Libelle_Modele
             ORDER BY Prix_max DESC;'''
    mycursor.execute(sql)
    prix_cher = mycursor.fetchone()
    return render_template('Velo/show_velo.html', prix_pas_cher=prix_pas_cher, prix_cher=prix_cher, Velos=Velo)

@app.route('/Velo/add', methods=['GET'])
def add_velo():

    mycursor = get_db().cursor()
    sql = '''SELECT *
             FROM Velo;'''
    mycursor.execute(sql)

    Velo = mycursor.fetchall()
    mycursor = get_db().cursor()
    sql = '''SELECT ID_Couleur, Libelle_Couleur
                     FROM Couleur
                     ORDER BY ID_Couleur;
                        '''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()
    sql = '''SELECT ID_Modele, Libelle_Modele
                     FROM Type_de_Modele
                     ORDER BY Type_de_Modele.ID_Modele;
                        '''
    mycursor.execute(sql)
    modele = mycursor.fetchall()
    return render_template('Velo/add_velo.html',modele=modele ,couleurs=couleurs, Velo=Velo)

@app.route('/Velo/delete')
def delete_velo():
    id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT ID_Velo
             FROM Velo
             WHERE ID_Velo = %s;'''
    tuple_param = (id)
    get_db().commit()
    change = mycursor.execute(sql, tuple_param)
    if change > 0:
        message = "Impossible de supprimer le Velo en question : " + id + " ! Car une instance de l'entité 'Velo' est utilisé dans une autre entité "
        flash(message, 'alert-warning')
    else:
        mycursor = get_db().cursor()
        sql = '''
            DELETE FROM Velo WHERE ID_Velo = %s
            '''
        tuple_param = (id)
        mycursor.execute(sql, tuple_param)
        get_db().commit()
    return redirect('/Velo/show')

@app.route('/Velo/edit', methods=['GET'])
def edit_velo():
    id=request.args.get('id')
    if id != None:
        id = int(id)
        mycursor = get_db().cursor()
        sql = '''SELECT ID_Velo, ID_Modele, Prix, ID_Couleur
                 FROM Velo
                 WHERE ID_Velo = %s;'''
        tuple_param = (id)
        mycursor.execute(sql, tuple_param)
        get_db().commit()
        Velo = mycursor.fetchone()
        mycursor = get_db().cursor()
        sql = '''SELECT ID_Couleur, Libelle_Couleur
                 FROM Couleur
                 ORDER BY ID_Couleur;
                    '''
        mycursor.execute(sql)
        couleurs = mycursor.fetchall()
        sql = '''SELECT ID_Modele, Libelle_Modele
                 FROM Type_de_Modele
                 ORDER BY Type_de_Modele.ID_Modele;
                    '''
        mycursor.execute(sql)
        modele = mycursor.fetchall()
    else:
        Velo=[]
    return render_template('Velo/edit_velo.html',modele=modele, couleurs=couleurs, Velo=Velo)

@app.route('/Velo/add', methods=['POST'])
def valid_add_velo():
    Prix = request.form.get('prix')
    id_M = request.form.get('id_M')
    couleur = request.form.get('couleur')
    mycursor = get_db().cursor()
    sql = '''INSERT INTO Velo (Prix, ID_Modele, ID_Couleur) VALUES (%s, %s, %s)'''
    tuple_param = (Prix, id_M, couleur)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/Velo/show',)

@app.route('/Velo/edit', methods=['POST'])
def valid_edit_velo():
    id_V = request.form.get('id_V')
    id_M = request.form.get('id_M')
    prix = request.form.get('prix')
    couleur = request.form.get('couleur')
    mycursor = get_db().cursor()
    sql = '''UPDATE Velo SET ID_Modele = %s, Prix = %s, ID_Couleur = %s WHERE ID_Velo = %s;'''
    tuple_param = (id_M, prix, couleur, id_V)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/Velo/show')
