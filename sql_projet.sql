DROP TABLE IF EXISTS Est_equippe_de;
DROP TABLE IF EXISTS Change_piece;

DROP TABLE IF EXISTS Loue___Contrat;
DROP TABLE IF EXISTS Reparation;
DROP TABLE IF EXISTS Velo;
DROP TABLE IF EXISTS Type_de_Modele;
DROP TABLE IF EXISTS Equipement;

DROP TABLE IF EXISTS Marque;
DROP TABLE IF EXISTS Couleur;
DROP TABLE IF EXISTS Piece;
DROP TABLE IF EXISTS TypeReparation;
DROP TABLE IF EXISTS Etudiant;



CREATE TABLE Etudiant(
   ID_Etudiant INT AUTO_INCREMENT,
   Nom VARCHAR(50),
   Prenom VARCHAR(50),
   Ville VARCHAR(50),
   N_Telephone VARCHAR(14),
   E_mail VARCHAR(50),
   Adresse VARCHAR(50),
   PRIMARY KEY(ID_Etudiant)
);

CREATE TABLE TypeReparation(
   ID_Type INT AUTO_INCREMENT,
   Libelle_Type VARCHAR(50),
   PRIMARY KEY(ID_Type)
);

CREATE TABLE Piece(
   ID_Piece INT AUTO_INCREMENT,
   Libelle_Piece VARCHAR(50),
   Prix_Piece DECIMAL(15,2),
   PRIMARY KEY(ID_Piece)
);

CREATE TABLE Couleur(
   ID_Couleur INT AUTO_INCREMENT,
   Libelle_Couleur VARCHAR(50),
   PRIMARY KEY(ID_Couleur)
);

CREATE TABLE Marque(
   ID_Marque INT AUTO_INCREMENT,
   Libelle_Marque VARCHAR(50),
   PRIMARY KEY(ID_Marque)
);


CREATE TABLE Equipement(
   ID_Equipement INT AUTO_INCREMENT,
   Libelle_Equipement VARCHAR(50),
   PRIMARY KEY(ID_Equipement)
);

CREATE TABLE Type_de_Modele(
   ID_Modele INT AUTO_INCREMENT,
   Libelle_Modele VARCHAR(50),
   ID_Marque INT NOT NULL,
   PRIMARY KEY(ID_Modele),
   FOREIGN KEY(ID_Marque) REFERENCES Marque(ID_Marque)
);

CREATE TABLE Velo(
   ID_Velo INT AUTO_INCREMENT,
   ID_Modele INT NOT NULL,
   Prix INT NOT NULL,
   ID_Couleur INT,
   PRIMARY KEY(ID_Velo),
   FOREIGN KEY(ID_Modele) REFERENCES Type_de_Modele(ID_Modele),
   FOREIGN KEY(ID_Couleur) REFERENCES Couleur(ID_Couleur)
);

CREATE TABLE Reparation(
   ID_Reparation INT AUTO_INCREMENT,
   Prix_Total VARCHAR(50),
   Date_Reparation DATE,
   ID_Velo INT NOT NULL,
   ID_Type INT NOT NULL,
   PRIMARY KEY(ID_Reparation),
   FOREIGN KEY(ID_Velo) REFERENCES Velo(ID_Velo),
   FOREIGN KEY(ID_Type) REFERENCES TypeReparation(ID_Type)
);

CREATE TABLE Loue___Contrat(
    ID_Contrat INT AUTO_INCREMENT,
    ID_Etudiant INT,
    ID_Velo INT,
    AAAA_MM_JJ DATE,
    Duree_location VARCHAR(50),
    Tarif VARCHAR(50),
    PRIMARY KEY(ID_Contrat),
    FOREIGN KEY(ID_Etudiant) REFERENCES Etudiant(ID_Etudiant),
    FOREIGN KEY(ID_Velo) REFERENCES Velo(ID_Velo)
);

CREATE TABLE Change_piece(
   ID_Piece INT,
   ID_Reparation INT,
   PRIMARY KEY(ID_Piece, ID_Reparation),
   FOREIGN KEY(ID_Piece) REFERENCES Piece(ID_Piece),
   FOREIGN KEY(ID_Reparation) REFERENCES Reparation(ID_Reparation)
);

CREATE TABLE Est_equippe_de(
   ID_Velo INT,
   ID_Equipement INT,
   PRIMARY KEY(ID_Velo, ID_Equipement),
   FOREIGN KEY(ID_Velo) REFERENCES Velo(ID_Velo),
   FOREIGN KEY(ID_Equipement) REFERENCES Equipement(ID_Equipement)
);

INSERT INTO Etudiant VALUES(NULL,'Varieur','Amaury','ANNEMASSE','04.26.26.71.85','AmauryVarieur@gmail.com','73, Avenue De Marlioz'),
                           (NULL,'Mailhot','Adèle','LE CREUSOT','03.51.52.34.64','AdeleMailhot@gmail.com','11, boulevard Aristide Briand'),
                           (NULL,'Édouard','Tristan','MARIGNANE','04.62.57.09.47','TristanEdouard@jourrapide.com','94, Rue de la Pompe'),
                           (NULL,'Marseau','Bruce','VANNES','02.59.48.94.77','BruceMarseau@jourrapide.com','38, avenue de Provence'),
                           (NULL,'Beaupré','Felicien','VERNON','02.93.53.38.15','FelicienBeaupre@rhyta.com','23, Rue Frédéric Chopin'),
                           (NULL,'Patenaude','Aubrey','LE CHESNAY','01.82.22.24.52','AubreyPatenaude@gmail.com','28, boulevard Aristide Briand'),
                           (NULL,'Goguen','Pansy','CHAMPS-SUR-MARNE','01.55.92.60.55','PansyGoguen@armyspy.com','35, place Maurice-Charretier'),
                           (NULL,'Gour','Agnès','NOGENT-SUR-MARNE','01.36.05.47.05','AgnesGour@rhyta.com','39, boulevard de Prague'),
                           (NULL,'Bondy','Leone','AJACCIO ','04.00.58.01.24','LeoneBondy@rhyta.com','77, Chemin des Bateliers'),
                           (NULL,'Sicard','Ernest','PARIS ','01.51.76.56.08','ErnestSicard@jourrapide.com','98, rue La Boétie'),
                           (NULL,'Raymond','Tearlach','DUNKERQUE ','03.01.65.22.27','TearlachRaymond@jourrapide.com','13, rue Cazade'),
                           (NULL,'Francoeur','Sibyla','VANVES ','01.04.18.93.04','SibylaFrancoeur@gmail.com','13, boulevard d Alsace'),
                           (NULL,'Sylvain','Mariette','VIRY-CHÂTILLON ','01.44.66.51.59','MarietteSylvain@armyspy.com','82, rue Marguerite'),
                           (NULL,'Duplanty','Burkett','MALAKOFF','01.55.35.64.82','BurkettDuplanty@dayrep.com','39, avenue Voltaire'),
                           (NULL,'Carignan','Archard','BASTIA','04.02.50.28.80','ArchardCarignan@jourrapide.com','60, Rue du Limas'),
                           (NULL,'Parenteau','Victor','LONGJUMEAU','01.50.54.35.86','VictorParenteau@gmail.com','22, rue Léon Dierx'),
                           (NULL,'Sanschagrin','Marguerite','TOURS','02.39.57.90.81','MargueriteSanschagrin@rhyta.com','24, avenue Jean Portalis'),
                           (NULL,'Gilbert','Zdenek','AMIENS','03.78.99.27.12','ZdenekGilbert@dayrep.com','48, rue de Geneve'),
                           (NULL,'Bélair','Harcourt','MARSEILLE','04.36.36.69.09','HarcourtBelair@dayrep.com','64, boulevard de la Liberation'),
                           (NULL,'Vaillancour','Mirabelle','BAIE-MAHAULT','05.48.01.09.27','MirabelleVaillancour@rhyta.com','43, Rue Joseph Vernet'),
                           (NULL,'Lussier','Cher','TOURNEFEUILLE','05.75.30.43.58','CherLussier@dayrep.com','63, quai Saint-Nicolas'),
                           (NULL,'Pouchard','Orville','LE PORT','02.79.77.39.75','OrvillePouchard@armyspy.com','25, rue Adolphe Wurtz'),
                           (NULL,'Chouinard','Fauna','NOUMÉA','03.94.97.19.63','FaunaChouinard@dayrep.com','47, Rue Roussy'),
                           (NULL,'Séguin','Franck','ISTRES','04.06.53.08.93','FranckSeguin@jourrapide.com','22, route de Lyon'),
                           (NULL,'Ailleboust','Belisarda','NÎMES','04.52.81.78.49','BelisardaAilleboust@rhyta.com','82, boulevard de Prague');

INSERT INTO TypeReparation VALUES(NULL,'Freignage'),
                                 (NULL,'Transmission'),
                                 (NULL,'Roue'),
                                 (NULL,'Equipement');

INSERT INTO Piece VALUES(NULL, 'Pneu',45),
                        (NULL, 'Chambre à Air',15),
                        (NULL, 'Cadre',120),
                        (NULL, 'Poignée de Frein',55),
                        (NULL, 'Chaine',10),
                        (NULL, 'Selle',35),
                        (NULL, 'Guidon',26),
                        (NULL, 'Dérailleur',25),
                        (NULL, 'Disque de Frein',35);

INSERT INTO Couleur VALUES(NULL, 'ROUGE'),
                          (NULL, 'BLEU'),
                          (NULL, 'ORANGE'),
                          (NULL, 'ROSE'),
                          (NULL, 'VERT'),
                          (NULL, 'JAUNE'),
                          (NULL, 'VIOLET'),
                          (NULL, 'BLANC');

INSERT INTO Marque VALUES(NULL, 'Canyon'),
                         (NULL, 'Lapierre'),
                         (NULL, 'Trek');



INSERT INTO Equipement VALUES(NULL, 'Panier'),
                              (NULL, 'Garde boue'),
                              (NULL, 'Béquille'),
                              (NULL, 'Lampe');

INSERT INTO Type_de_Modele VALUES(NULL, 'Aeroad',1),
                                 (NULL, 'Grail',1),
                                 (NULL, 'Ultimate',1),
                                 (NULL, 'E-explorer',2),
                                 (NULL, 'Xelius',2),
                                 (NULL, 'Pulsium',2),
                                 (NULL, 'Madone',3),
                                 (NULL, 'Verve',3),
                                 (NULL, 'Marlin',3);

INSERT INTO Velo VALUES(NULL,1, 150, 1),
                       (NULL,1, 135, 1),
                       (NULL,1, 145, 1),
                       (NULL,2, 100, 1),
                       (NULL,2, 110, 1),
                       (NULL,3, 151, 2),
                       (NULL,3, 115, 2),
                       (NULL,4, 148, 2),
                       (NULL,4, 135, 3),
                       (NULL,5, 149, 3),
                       (NULL,5, 132, 4),
                       (NULL,5, 147, 4),
                       (NULL,6, 132, 5),
                       (NULL,6, 116, 5),
                       (NULL,7, 118, 6),
                       (NULL,7, 119, 6),
                       (NULL,7, 139, 7),
                       (NULL,7, 165, 7),
                       (NULL,8, 147, 7),
                       (NULL,8, 138, 8),
                       (NULL,9, 154, 8),
                       (NULL,9, 133, 8),
                       (NULL,9, 140, 8);

INSERT INTO Reparation VALUES(NULL,45,'2024_06_06',1,3),
                             (NULL,25,'2024_04_04',15,2),
                             (NULL,100,'2024_11_14',23,1),
                             (NULL,48,'2024_06_06',4,2),
                             (NULL,125,'2024_10_29',18,3),
                             (NULL,39,'2024_08_08',1,2),
                             (NULL,12,'2024_12_24',18,1);

INSERT INTO Change_piece VALUES(8, 6),
                               (1, 4),
                               (5, 6),
                               (7, 1),
                               (4, 3),
                               (2, 2),
                               (2, 5),
                               (1, 6);

INSERT INTO Est_equippe_de VALUES(21, 1),
                                 (21, 3),
                                 (3, 4),
                                 (22, 4),
                                 (5, 2),
                                 (13, 1),
                                 (13, 2),
                                 (19, 4),
                                 (6, 3);

INSERT INTO Loue___Contrat VALUES(NULL,23, 5, '2024-11-14', '2j', '35.5'),
                                 (NULL,12, 16, '2024-11-25', '10h', '12.0'),
                                 (NULL,5, 18, '2024-09-06', '5j', '60.3'),
                                 (NULL,23, 7, '2024-11-18', '2j', '38.9'),
                                 (NULL,2, 5, '2024-12-05', '2j', '35.5'),
                                 (NULL,19, 5, '2024-11-16', '2j', '35.5'),
                                 (NULL,14, 2, '2024-08-09', '5h', '7.2'),
                                 (NULL,1, 3, '2024-11-14', '2j', '33.5'),
                                 (NULL,4, 9, '2024-04-14', '10h', '13.6'),
                                 (NULL,3, 22, '2024-10-01', '2j', '35.5'),
                                 (NULL,6, 1, '2024-09-03', '15j', '120.0'),
                                 (NULL,18, 17, '2024-04-28', '1j', '18.4'),
                                 (NULL,13, 8, '2024-04-05', '2j', '30.5'),
                                 (NULL,9, 15, '2024-09-01', '5j', '62.6'),
                                 (NULL,7, 13, '2024-08-08', '2j', '33.9'),
                                 (NULL,10, 21, '2024-07-07', '12j', '50.0'),
                                 (NULL,8, 19, '2024-06-06', '2j', '39.5'),
                                 (NULL,15, 4, '2024-11-12', '5h', '8.0'),
                                 (NULL,11, 22, '2024-05-05', '10h', '15.6'),
                                 (NULL,14, 9, '2024-04-15', '2j', '34.5'),
                                 (NULL,16, 20, '2024-11-24', '3j', '48.0'),
                                 (NULL,17, 19, '2024-01-01', '100j', '1500.0'),
                                 (NULL,20, 11, '2024-03-20', '2j', '32.5'),
                                 (NULL,21, 6, '2024-12-01', '5h', '7.4'),
                                 (NULL,22, 17, '2024-10-30', '10h', '18.1');




SHOW TABLES;


#Affiche toutes les réparations effectuées sur chaque vélo
SELECT Velo.ID_Velo, Reparation.Date_Reparation, Reparation.Prix_Total, TypeReparation.Libelle_Type
FROM Velo
         JOIN Reparation ON Velo.ID_Velo = Reparation.ID_Velo
         JOIN TypeReparation ON Reparation.ID_Type = TypeReparation.ID_Type
ORDER BY Velo.ID_Velo;

#Affiche le nombre de fois que chaque étudiant à effectué une location
SELECT Etudiant.ID_Etudiant, Etudiant.Nom, Etudiant.Prenom, COUNT(Loue___Contrat.ID_Velo) AS Nombre_Velos_Loues
FROM Etudiant
         JOIN Loue___Contrat ON Etudiant.ID_Etudiant = Loue___Contrat.ID_Etudiant
GROUP BY Etudiant.ID_Etudiant;

#Lister les vélos équipés de chaque type d équipement
SELECT Velo.ID_Velo, Equipement.Libelle_Equipement
FROM Velo
         JOIN Est_equippe_de ON Velo.ID_Velo = Est_equippe_de.ID_Velo
         JOIN Equipement ON Est_equippe_de.ID_Equipement = Equipement.ID_Equipement
ORDER BY Velo.ID_Velo;

#Lister les pièces changées lors de chaque réparation
SELECT Reparation.ID_Reparation, Change_piece.ID_Piece, Piece.Libelle_Piece, Piece.Prix_Piece
FROM Reparation
         JOIN Change_piece ON Reparation.ID_Reparation = Change_piece.ID_Reparation
         JOIN Piece ON Change_piece.ID_Piece = Piece.ID_Piece
ORDER BY Reparation.ID_Reparation;

#Trouver le coût total des réparations pour chaque vélo
SELECT Velo.ID_Velo, SUM(Piece.Prix_Piece) AS Cout_Total_Reparations
FROM Velo
         JOIN Reparation ON Velo.ID_Velo = Reparation.ID_Velo
         JOIN Change_piece ON Reparation.ID_Reparation = Change_piece.ID_Reparation
         JOIN Piece ON Change_piece.ID_Piece = Piece.ID_Piece
GROUP BY Velo.ID_Velo;

#Lister tous les modèles de vélos disponibles par marque
SELECT Marque.Libelle_Marque, Type_de_Modele.Libelle_Modele
FROM Marque
         JOIN Type_de_Modele ON Marque.ID_Marque = Type_de_Modele.ID_Marque;

#Afficher les réparations qui ont impliqué plus de 2 pièces
SELECT Reparation.ID_Reparation, COUNT(Change_piece.ID_Piece) AS Nombre_Pieces
FROM Reparation
         JOIN Change_piece ON Reparation.ID_Reparation = Change_piece.ID_Reparation
GROUP BY Reparation.ID_Reparation
HAVING COUNT(Change_piece.ID_Piece) >= 3;

#Lister les modèles de vélos et le nombre total de réparations effectuées pour chaque modèle
SELECT Type_de_Modele.Libelle_Modele, COUNT(Reparation.ID_Reparation) AS Nombre_Reparations
FROM Type_de_Modele
         JOIN Velo ON Type_de_Modele.ID_Modele = Velo.ID_Modele
         JOIN Reparation ON Velo.ID_Velo = Reparation.ID_Velo
GROUP BY Type_de_Modele.Libelle_Modele
ORDER BY Nombre_Reparations;

#Afficher la liste des pièces utilisées dans les réparations avec leur coût total cumulé
SELECT Piece.Libelle_Piece, SUM(Piece.Prix_Piece) AS Cout_Total
FROM Piece
         JOIN Change_piece ON Piece.ID_Piece = Change_piece.ID_Piece
GROUP BY Piece.Libelle_Piece
ORDER BY Cout_Total;

#Affiche tous les Vélos qui on été loué derant le mois d avril en 2024
SELECT Velo.ID_Velo, Loue___Contrat.AAAA_MM_JJ
FROM Velo
         JOIN Loue___Contrat ON Velo.ID_Velo = Loue___Contrat.ID_Velo
WHERE Loue___Contrat.AAAA_MM_JJ BETWEEN '2024-04-01' AND '2024-04-30';

#affiche les mois ou il y a eu le plus de location en 2024
SELECT MONTH(Loue___Contrat.AAAA_MM_JJ) AS Mois, COUNT(*) AS Nombre_Locations
FROM Loue___Contrat
WHERE YEAR(Loue___Contrat.AAAA_MM_JJ) = 2024
GROUP BY Mois
ORDER BY Nombre_Locations DESC;
