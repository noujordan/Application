#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3

def create_database():
    conn = sqlite3.connect('association.bd')
    cursor = conn.cursor()

    # Création de la table Étudiants
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Etudiants (
            id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance TEXT NOT NULL,
            email TEXT NOT NULL,
            filiere TEXT NOT NULL,
            niveau TEXT NOT NULL,
            date_inscription TEXT NOT NULL
        )
    """)

    # Création de la table Paiements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Paiements (
            id_paiement INTEGER PRIMARY KEY AUTOINCREMENT,
            id_etudiant INTEGER NOT NULL,
            montant REAL NOT NULL,
            date_paiement TEXT NOT NULL,
            mode_paiement TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (id_etudiant) REFERENCES Etudiants (id_etudiant)
        )
    ''')
    
    # Création de la table Taches
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Taches (
            id_tache INTEGER PRIMARY KEY AUTOINCREMENT,
            id_etudiant INTEGER,
            description TEXT NOT NULL,
            date_creation TEXT NOT NULL,
            budget REAL NOT NULL,
            etat TEXT NOT NULL,
            FOREIGN KEY (id_etudiant) REFERENCES Etudiants (id_etudiant)
     )
    """)

    conn.commit()

create_database()

conn=sqlite3.connect('association.bd')
cursor=conn.cursor()
#CHECK(status IN ('espece', 'cheque', 'carte bancaire'))
#CHECK(status IN ('cloture', 'en cours', 'en attente'))


# In[2]:


import locale
from datetime import datetime
locale.setlocale(locale.LC_TIME, 'French_France.1252')

def demander_date(format_attendu, format_description):
    while True:
        try:
            date_string = input(f"au format {format_description} : ")
            a = datetime.strptime(date_string, format_attendu)
            return date_string;
        except ValueError:
            print(f"Format invalide! Respectez le format {format_description}.")


# In[3]:


#Gestion des étudiants

def collecte_etudiant():
    nom=input("Entrer le nom de l'étudiant\t")
    prenom=input("Entrer le prenom de l'étudiant\t")
    print("Entrer la date de naissance")
    daten=demander_date("%d %B %Y", "JJ Mois AAAA (Exemple: 11 février 2006)")
    email=input("Entrer l'adresse électronique de l'étudiant\t")  
    fil=input("Entrer la filière de l'étudiant\t")
    niv=input("Entrer le niveau de l'étudiant\t")
    print("Entrer la date d'inscription")
    datei=demander_date("%d %B %Y", "JJ Mois AAAA (Exemple: 01 janvier 2025)")
    return (nom,prenom,daten,email,fil,niv,datei);
    
def ajout_etudiant(nom, prenom, date_naissance, email, filiere, niveau, date_inscription):
    cursor.execute("""
        INSERT INTO Etudiants (nom, prenom, date_naissance, email, filiere, niveau, date_inscription)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nom, prenom, date_naissance, email, filiere, niveau, date_inscription))
    conn.commit()

def modifie_etudiant(id_etudiant,nom, prenom, date_naissance, email, filiere, niveau, date_inscription):
    cursor.execute("""
        UPDATE Etudiants
        SET nom = ?, prenom = ?, date_naissance = ?, email = ?, filiere = ?, niveau = ?, date_inscription = ?
        WHERE id_etudiant = ?
    """, (nom, prenom, date_naissance, email, filiere, niveau, date_inscription, id_etudiant))
    conn.commit()

def supprime_etudiant(id_etudiant):
    cursor.execute("""DELETE FROM Etudiants WHERE id_etudiant = ?""", (id_etudiant,))
    conn.commit()

def recherche_etudiant(num,info):
    if num == 1:
        cursor.execute("""
        SELECT * FROM Etudiants
        WHERE id_etudiant=? """,(info,))
    elif num == 2:
        cursor.execute("""
        SELECT * FROM Etudiants
        WHERE nom=? """,(info,))
    elif num == 3:
        cursor.execute("""
        SELECT * FROM Etudiants
        WHERE prenom=? """,(info,))
    else:
        cursor.execute(""" """)
        print("Choix Incorrect!!!")
    rows=cursor.fetchall()
    if len(rows) == 0:
        print("L'étudiant n'existe pas")
        return 1;
    else:
        return rows; 
    conn.commit()

def affiche_etudiant(rows):
    for row in rows:
        print("nId_étudiant:",row[0],"\tNom:",row[1],"\tPrenom:",row[2],
              "\tDate Naissance:",row[3],"   Email:",row[4],"\tFilière:",row[5],
              "\tNiveau:",row[6],"   Date Inscription:",row[7])


# In[4]:


#Gestion des tâches

def collecte_tache():
    desc=input("Entrer une description de la tâche\t")
    print("Entrer la date de création de la Tâche\t")
    datecre=demander_date("%d %B %Y", "JJ Mois AAAA (Exemple: 06 Juillet 2005)")
    bud=input("Entrer le budget à allouer à la tâche\t")
    eta=int(input("CHoisissez l'etat de la tâche:\n1-Cloturé\n2-En Cours\n3-En Attente\t"))
    if eta == 1:
        return (desc, datecre, bud, "cloture")
    elif eta == 2:
        return (desc, datecre, bud, "en cours")
    elif eta == 3:
        return (desc, datecre, bud, "en attente")
    else:
        print("Etat de la tâche incorrect")
        return 1;

def ajout_tache(id_etudiant, description, date_creation, budget, etat):
    cursor.execute("""
        INSERT INTO Taches (id_etudiant, description, date_creation, budget, etat)
        VALUES (?, ?, ?, ?, ?)
    """, (id_etudiant, description, date_creation, budget, etat))
    conn.commit()

def modifie_tache(id_tache, id_etudiant, description, date_creation, budget, etat):
    cursor.execute("""
        UPDATE Taches
        SET id_etudiant = ?, description = ?, date_creation = ?, budget = ?, etat = ?
        WHERE id_tache = ?
    """, (id_etudiant, description, date_creation, budget, etat, id_tache))
    conn.commit()

def supprime_tache(num,id): 
    if num == 1:
        cursor.execute('DELETE FROM Taches WHERE id_tache = ?', (id,))
    else:
        cursor.execute('DELETE FROM Taches WHERE id_etudiant = ?', (id,))
    conn.commit()

def recherche_tache(num,info):
    if num == 1:
        cursor.execute("""
        SELECT * FROM Taches
        WHERE id_tache = ? """,(info,))
    elif num == 2:
        cursor.execute("""
        SELECT * FROM Taches
        WHERE description = ? """,(info,))
    elif num == 3:
        cursor.execute("""
        SELECT * FROM Taches
        WHERE id_etudiant = ? """,(info,))
    else:
        cursor.execute(""" """)
        print("Choix Incorrect!!!")
    rows=cursor.fetchall()
    if len(rows) == 0:
        print("La tâche n'existe pas")
        return 1;
    else:
        return rows;
    conn.commit()
    
def affiche_tache(rows):
    for row in rows:
        print("\nId_tâche:",row[0],"\tId_étudiant:",row[1],"\tDescription:",row[2],
              "\tDate Création:",row[3],"\tBudget:",row[4],"\tEtat:",row[5])


# In[5]:


#Gestion des paiements

def collecte_paiement():
    mon=input("Entrer le montant du paiement\t")
    print("Entrer la date du paiement\t")
    datepa=demander_date("%d %B %Y", "JJ Mois AAAA (Exemple: 24 janvier 2005 )")
    desc=input("Entrer une description du paiement")
    mode=int(input("CHoisissez le mode de paiment:\n1-espèce\n2-chèque\n3-Carte Bancaire\t"))
    if mode == 1:
        return (mon, datepa, "espece", desc);
    elif mode == 2:
        return (mon, datepa, "cheque", desc);
    elif mode == 3:
        return (mon, datepa, "carte bancaire", desc);
    else:
        print("Mode de paiement incorrect")
        return 1;
        

def ajout_paiement(id_etudiant, montant, date_paiement, mode_paiement, description):
    cursor.execute("""
        INSERT INTO Paiements (id_etudiant, montant, date_paiement, mode_paiement, description)
        VALUES (?, ?, ?, ?, ?)
    """, (id_etudiant, montant, date_paiement, mode_paiement, description))
    conn.commit()

def modifie_paiement(id_paiement, id_etudiant, montant, date_paiement, mode_paiement, description):
    cursor.execute("""
        UPDATE Paiements
        SET id_etudiant = ?, montant = ?, date_paiement = ?, mode_paiement = ?, description = ?
        WHERE id_paiement = ?
    """, (id_etudiant, montant, date_paiement, mode_paiement, description, id_paiement))
    conn.commit()

def supprime_paiement(num,id):
    if num == 1:
        cursor.execute('DELETE FROM Taches WHERE id_paiement = ?', (id,))
    else:
        cursor.execute('DELETE FROM Taches WHERE id_etudiant = ?', (id,))
    conn.commit()
    
def recherche_paiement(num,info):
    if num == 1:
        cursor.execute("""
        SELECT * FROM Paiements
        WHERE id_paiement=? """,(info,))
    elif num == 2:
        cursor.execute("""
        SELECT * FROM Paiements
        WHERE description=? """,(info,))
    elif num == 3:
        cursor.execute("""
        SELECT * FROM Paiements
        WHERE mode_paiement =? """,(info,))
    elif num == 4:
        cursor.execute("""
        SELECT * FROM Paiements
        WHERE date_paiement=? """,(info,))
    else:
        cursor.execute(""" """)
        print("Choix incorrect")
    rows=cursor.fetchall()
    if len(rows) == 0:
        print("Le Paiement n'existe pas")
        return 1;
    else:
        return rows;
    conn.commit()
    
def affiche_paiement(rows):
    for row in rows:
        print("\nId_paiement:",row[0],"\tId_étudiant:",row[1],"\tMontant:",row[2],
              "\tDate Paiement:",row[3],"\tMode Paiement:",row[4],"\tDescription:",row[5])


# In[ ]:


#Visualisation
import matplotlib.pyplot as plt
def main_menu():
    while True:
        print("\nMENU PRINCIPAL")
        print("QUE VOULEZ-VOUS?")
        print("1. Ajouter un étudiant")
        print("2. Modifier les données d'un étudiant")
        print("3. Supprimer un étudiant")
        print("4. Rechercher des étudiants")
        print("5. Ajouter une tâche")
        print("6. Modifier les informations d'une tâche")
        print("7. Supprimer une tâche")
        print("8. Rechercher des tâches")
        print("9. Enregistrer un nouveau paiement")
        print("10. Modifier les informations d'un paiement")
        print("11. Supprimer un paiement")
        print("12. Rechercher des paiements")
        print("13. afficher les listes des étudiants")
        print("14. afficher les listes des tâches")
        print("15. afficher les listes des paiements")
        print("16. Consulter les tâches d'un étudiant")
        print("17. Consulter l'historique des paiements d'un étudiant")
        print("18. Connaitre le montant total payé par un étudiant")
        print("19. Connaitre les états respectifs des différentes tâches")
        print("20. Connaitre les cotisations des étudiants")
        print("21. Connaitre la somme des cotisations des étudiants")
        print("22. Afficher pour chaque mois le total des montants payés")
        print("23. Afficher pour chaque mode de paiement le total des montant payés")
        print("AUTRE. Quitter")

        choice = int(input("Choisissez une option: "))

        if choice == 1:
            a=collecte_etudiant()
            ajout_etudiant(a[0],a[1],a[2],a[3],a[4],a[5],a[6])
            
        elif choice == 2:
            iid=input("Entrer l'identifiant de l'étudiant où l'on doit modifier les informations\t")
            if recherche_etudiant(1,iid) != 1:
                a=collecte_etudiant()
                modifie_etudiant(iid,a[0],a[1],a[2],a[3],a[4],a[5],a[6])
            
        elif choice == 3:
            iid=input("Entrer l'identifiant de l'étudiant à supprimer\t")
            a = recherche_etudiant(1,iid)
            if a != 1:
                print("L'étudiant de Coordonnées:")
                affiche_etudiant(a)
                supprime_etudiant(iid)
                supprime_tache(2,iid)
                supprime_paiement(2,iid)
                print("a été Supprimé")
        
        elif choice == 4:
            choix=int(input("Rechercher par:\n1-Identifiant\n2-Nom\n3-Prenom\t"))
            donne=input("Entrer la donnée à rechercher")
            a = recherche_etudiant(choix,donne)
            if a != 1:
                affiche_etudiant(a)
        
        elif choice == 5:
            iid=input("Entrer l'identifiant de l'étudiant responsable de la tâche\t")
            if recherche_etudiant(1,iid) != 1:
                a = collecte_tache()
                if a != 1:
                    ajout_tache(iid,a[0],a[1],a[2],a[3])
                
        elif choice == 6:
            idt=input("Entrer l'identifiant de la tâche à modifier\t")
            if recherche_tache(1,idt) != 1:
                idd=input("Entrer l'identifiant de l'étudiant responsable de la tâche\t")
                if recherche_etudiant(1,iid) != 1:
                    a = collecte_tache()
                    if a != 1:
                        modifie_tache(idt,iid,a[0],a[1],a[2],a[3])
                
        elif choice == 7:
            idt=input("Entrer l'identifiant de la tâche à supprimer\t")
            a = recherche_tache(1,idt)
            if a != 1:
                print("La Tâche de Coordonnées:")
                affiche_tache(a)
                supprime_tache(1,idt)
                print("a été Supprimé")
            
        elif choice == 8:
            choix=int(input("Rechercher par:\n1-Description\n2-Identifiant de l'étudiant responsable\t"))
            donne=input("Entrer la donnée à rechercher\t")
            a = recherche_tache(choix+1,donne)
            if a != 1:
                affiche_tache(a)
        
        elif choice == 9:
            iid=input("Entrer l'identifiant de l'étudiant ayant éffectué le paiement\t")
            if recherche_etudiant(1,iid) != 1:
                a = collecte_paiement()
                if a != 1:
                    ajout_paiement(iid,a[0],a[1],a[2],a[3])
                
        elif choice == 10:
            idp=input("Entrer l'identifiant du paiement")
            if recherche_paiement(1,idp) != 1:
                iid=input("Entrer l'identifiant de l'étudiant ayant effectué le paiement\t")
                if recherche_etudiant(1,iid) != 1:
                    a = collecte_paiement()
                    if a != 1:
                        modifie_paiement(idp,iid,a[0],a[1],a[2],a[3])
            
        elif choice == 11:
            idp=input("Entrer l'identifiant du paiement à supprimer\t")
            a = recherche_paiement(1,idp)
            if a != 1:
                print("Le Paiement de Coordonnées:")
                affiche_paiement(a)
                supprime_paiement(1,idp)
                print("a été Supprimé")
            
        elif choice == 12:
            choix=int(input("Rechercher par:\t1-Description\n2-Mode de Paiement\n3-Date de Paiement\t"))
            if choix == 1:
                donne=input("Entrer la description à rechercher\t")
            elif choix == 2:
                mode=int(input("CHoisissez le mode de paiment à rechercher:\n1-espèce\n2-chèque\n3-Carte Bancaire\t"))
                if mode == 1:
                    donne = "espece"
                elif mode == 2:
                    donne = "cheque"
                elif mode == 3:
                    donne = "carte bancaire"
                else:
                    print("Mode de paiement incorrect")
            elif choix == 3:
                print("Entrer la date du paiement à rechercher\t")
                donne=demander_date("%d %B %Y", "JJ Mois AAAA (Exemple: 24 janvier 2005 )")
            else:
                print("Choix Incorrect!!!")
            if choix in [1, 2, 3]:
                a = recherche_paiement(choix+1,donne)
                if a != 1:
                    affiche_paiement(a)
        
        elif choice == 13:
            choix=int(input("Vous voulez afficher les étudiants:\n1-Par Niveau\n2-Par Filière\nAutre-Tout afficher\t"))
            if choix == 1:
                cursor.execute("""
                SELECT * FROM Etudiants
                ORDER BY niveau""")
            elif choix == 2:
                cursor.execute("""
                SELECT * FROM Etudiants
                ORDER BY filiere""")
            else:
                cursor.execute("""
                SELECT * FROM Etudiants""")
            rows=cursor.fetchall()
            if len(rows) == 0:
                print("Aucun étudiant enregistré")
            else:
                affiche_etudiant(rows)
            conn.commit()
            
        elif choice == 14:
            cursor.execute("""SELECT * FROM Taches""")
            rows=cursor.fetchall()
            if len(rows) == 0:
                print("Aucune tâche enregistrée")
            else:
                affiche_tache(rows)
        
        elif choice == 15:
            cursor.execute("""SELECT * FROM Paiements""")
            rows=cursor.fetchall()
            if len(rows) == 0:
                print("Aucun paiement enregistré")
            else:
                affiche_paiement(rows)
            
        elif choice == 16:
            iid=input("Entrer l'identifiant de l'étudiant")
            a = recherche_etudiant(1,iid)
            if a != 1:
                cursor.execute("""
                    SELECT id_tache, id_etudiant, description, date_creation, budget, etat 
                    FROM Taches NATURAL JOIN Etudiants
                    WHERE id_etudiant = ?""",(iid,))
                rows=cursor.fetchall()
                if len(rows) == 0:
                    print("Cet étudiant n'a éffectué aucune tâche")
                else:
                    affiche_tache(rows)
            conn.commit()
            
        elif choice == 17:
            iid=input("Entrer l'identifiant de l'étudiant")
            a = recherche_etudiant(1,iid)
            if a!= 1:
                cursor.execute("""
                    SELECT id_paiement,id_etudiant,montant,date_paiement,mode_paiement,description
                    FROM Paiements NATURAL JOIN Etudiants
                    WHERE id_etudiant = ?
                    ORDER BY montant""",(iid,))
                rows=cursor.fetchall()
                if len(rows) == 0:
                    print("Cet étudiant n'a éffectué aucun paiement")
                else:
                    affiche_paiement(rows)
                #Séparation des données de la liste
                jour = [item[3] for item in rows]
                montants = [item[2] for item in rows]
                #Création du graphique
                plt.figure(figsize=(10,6))
                plt.bar(jour,montants, color='black')
                #Ajout des titres
                plt.title("HISTORIQUE DE PAIEMENT DE L'ETUDIANT", fontsize=16)
                plt.xlabel("Jour", fontsize=12)
                plt.ylabel("Montants", fontsize=12)
                plt.xticks(rotation=45)
                #Affichage
                plt.tight_layout() # éviter que les titres ne se chevauchent
                plt.show()
            conn.commit()
            
        elif choice == 18:
            iid=input("Entrer l'identifiant de l'étudiant")
            a = recherche_etudiant(1,iid)
            if a!= 1:
                cursor.execute("""
                    SELECT sum(montant) FROM Paiements NATURAL JOIN Etudiants
                    WHERE id_etudiant = ?""",(iid,))
                rows=cursor.fetchall()
                print("Le montant total payé par l'étudiant d'identifiant",iid,"est :",rows[0][0])
            conn.commit()
            
        elif choice == 19:
            cursor.execute("""
                SELECT id_tache,etat FROM Taches""")
            rows=cursor.fetchall()
            if len(rows) == 0:
                print("Aucune tache répertoriée")
            else:
                for row in rows:
                    print("La tâche d'identifiant",row[0],"est",row[1])
                cursor.execute("""
                    SELECT etat, sum(id_tache) FROM Taches
                    GROUP BY etat
                    ORDER BY etat""")
                rows=cursor.fetchall()
                #Séparation des données de la liste
                etat = [item[0] for item in rows]
                valeur = [item[1] for item in rows]
                #Création du graphique
                plt.figure(figsize=(6,6))
                plt.pie(valeur,labels=etat, autopct='%1.1f%%',
                        startangle=90, colors=['skyblue', 'orange', 'lightgreen'])
                #Ajout du titre
                plt.title("REPARTITION DES ETATS", fontsize=16)
                #Affichage
                plt.axis('equal') # Assure que le diagramme est circulaire
                plt.show()

        elif choice == 20:
            choix=int(input("Vous voulez les cotisations:1-D'une Filière\n2-D'un Niveau\nAutre-Généralement\t"))
            if choix == 1:
                info=input("Quelle filière:\t")
                cursor.execute("""
                SELECT nom,prenom,sum(montant) AS s FROM Paiements NATURAL JOIN Etudiants
                WHERE filiere = ?
                GROUP BY id_etudiant
                ORDER BY s""",(info,))
            elif choix == 2:
                info=input("Quel niveau:\t")
                cursor.execute("""
                SELECT nom,prenom,sum(montant) AS s FROM Paiements NATURAL JOIN Etudiants
                WHERE niveau = ?
                GROUP BY id_etudiant
                ORDER BY s""",(info,))
            else:
                cursor.execute("""
                SELECT nom,prenom,sum(montant) AS s FROM Paiements NATURAL JOIN Etudiants
                GROUP BY id_etudiant
                ORDER BY s""")
            rows=cursor.fetchall()
            if len(rows) == 0:
                print("Aucune cotisation")
            else:
                for row in rows:
                    print(row[0]," ",row[1]," a cotisé au total ",row[2])
                #Séparation des données de la liste
                Nom = [item[0]+' '+item[1] for item in rows]
                montants = [item[2] for item in rows]
                #Création du graphique
                plt.figure(figsize=(10,6))
                plt.bar(Nom,montants, color='lightgreen')
                #Ajout des titres
                plt.title("COTISATION DES ETUDUANTS", fontsize=16)
                plt.xlabel("Nom Complet", fontsize=12)
                plt.ylabel("Montant", fontsize=12)
                plt.xticks(rotation=45)
                #Affichage
                plt.tight_layout() # éviter que les titres ne se chevauchent
                plt.show()
            conn.commit()
            
        elif choice == 21:
            choix=int(input("Vous voulez les cotisations:1-D'une Filière\n2-D'un Niveau\nAutre-Généralement\t"))
            if choix == 1:
                info=input("Quelle filière:\t")
                cursor.execute("""
                SELECT sum(montant) FROM Paiements NATURAL JOIN Etudiants
                WHERE filiere = ?""",(info,))
            elif choix == 2:
                info=input("Quel niveau:\t")
                cursor.execute("""
                SELECT sum(montant) FROM Paiements NATURAL JOIN Etudiants
                WHERE niveau = ?""",(info,))
            else:
                cursor.execute("""
                SELECT sum(montant) FROM Paiements NATURAL JOIN Etudiants""")
            rows=cursor.fetchall()
            print("Le Montant total payé par ces étudiants est ",rows[0][0])
            conn.commit()
        
        elif choice == 22:
            cursor.execute("""
                SELECT 
                    substr(date_paiement, instr(date_paiement, ' ') +1, length(date_paiement) - instr(date_paiement, ' ')) AS mois,
                    SUM(montant) as s FROM Paiements
                GROUP BY mois
                ORDER BY s""")
            rows=cursor.fetchall()
            for row in rows:
                print("Mois : ",row[0],", Total: ",row[1])
            #Séparation des données de la liste
            mois = [item[0] for item in rows]
            montants = [item[1] for item in rows]
            #Création du graphique
            plt.figure(figsize=(10,6))
            plt.bar(mois,montants, color='skyblue')
            #Ajout des titres
            plt.title("MONTANT TOTAL PAR MOIS", fontsize=16)
            plt.xlabel("Mois", fontsize=12)
            plt.ylabel("Montant Total", fontsize=12)
            plt.xticks(rotation=45)
            #Affichage
            plt.tight_layout() # éviter que les titres ne se chevauchent
            plt.show()
            conn.commit()
        
        elif choice == 23:
            cursor.execute("""
                SELECT mode_paiement,sum(montant) AS s FROM Paiements
                GROUP BY mode_paiement
                ORDER BY s""")
            rows=cursor.fetchall()
            if len(rows) == 0:
                print("Aucun Paiement")
            else:
                for row in rows:
                    print("Le Montant total Payé par/en",row[0]," est ",row[1])
                #Séparation des données de la liste
                mode = [item[0] for item in rows]
                montants = [item[1] for item in rows]
                #Création du graphique
                plt.figure(figsize=(10,6))
                plt.bar(mode,montants, color='orange')
                #Ajout des titres
                plt.title("MONTANT PAR MODE DE PAIEMENT", fontsize=16)
                plt.xlabel("Mode de Paiement", fontsize=12)
                plt.ylabel("Montant", fontsize=12)
                plt.xticks(rotation=45)
                #Affichage
                plt.tight_layout() # éviter que les titres ne se chevauchent
                plt.show()

            conn.commit()
        else:
            print("\nFERMETURE EN COURS .   .   .   .   .   .   .   .   .   .   .\n")
            input("\nAppuyez sur le bouton 'ENTER' pour fermer le programme\t")
            return 0;
        

if __name__ == "__main__":
    create_database()  # Créer la base de données si elle n'existe pas
    main_menu()  # Lancer le menu principal


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




