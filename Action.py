#Importation des modules
import sqlite3

from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)

# Connexion à la base de données
conn = sqlite3.connect('actions.db')

# Création d'un curseur pour exécuter des requêtes
c = conn.cursor()

#Création de la table Action
c.execute('''CREATE TABLE IF NOT EXISTS Action (
          ID TEXT PRIMARY KEY,
          Intitule TEXT NOT NULL,
          Taux_avancement TEXT NOT NULL,
          Objectif TEXT NOT NULL
)''')


#Valide la transcation avec la BDD       
conn.commit()
conn.close()

# Fonction pour ajouter une action
def add_action(action_id, intitule, taux_avancement, objectif):
    conn = sqlite3.connect('actions.db')
    c = conn.cursor()

    # Vérifie si l'ID existe déjà
    exist_action = select_action(action_id)
    if exist_action:
        return "Erreur : L'ID d'action existe déjà."

    c.execute('INSERT INTO Action (ID, Intitule, Taux_avancement, Objectif) VALUES (?, ?, ?, ?)', (action_id, intitule, taux_avancement, objectif))

    conn.commit()
    
    conn.close()

# Fonction pour sélectionner une action par ID
def select_action(action_id):
    #Connexion à la BDD
    conn = sqlite3.connect('actions.db')

    #Création d'un curseur 
    c = conn.cursor()

    #? Permet d'éviter les attaques par injection grace à un paramètre de substitution
    #le tuple avec la virgule (action_id,) est utilisé pour indiquer qu'il s'agit d'un seul paramètre
    c.execute('SELECT * FROM Action WHERE ID = ?', (action_id,))

    #fetchone permet de récuperer un enregistrement
    action = c.fetchone()

    #Fermeture de la connexion et on retourne le résultat 
    conn.close()
    
    return action


# Fonction pour modifier les informations d'une action
def update_action(action_id, intitule, taux_avancement, objectif):

    #intitule = input("Nouvel intitulé : ")
    #taux_avancement = input("Nouveau taux d'avancement : ")
    #objectif = input("Nouvel objectif : ")

    #On vérifie que le taux est bien compris entre 0 et 100
    # if not is_valid_taux_avancement(taux_avancement):
    #     print("Erreur : Le taux d'avancement doit être un nombre entre 0 et 100.")
    #     return
    
    conn = sqlite3.connect('actions.db')
    c = conn.cursor()

    c.execute('''UPDATE Action SET 
            Intitule = ?,
            Taux_avancement = ?,
            Objectif = ?
        WHERE ID = ?
    ''', (intitule, taux_avancement, objectif, action_id))

    conn.commit()

    conn.close()

# Fonction pour retirer une action par ID
def delete_action(action_id):
    conn = sqlite3.connect('actions.db')
    c = conn.cursor()

    c.execute('DELETE FROM Action WHERE ID = ?', (action_id,))

    conn.commit()

    conn.close()

#Au debut j'avais pensé à faire un CHECK en SQL mais pas possible car VARCHAR et pas INT
#Fonction pour vérifier que le taux est bien compris entre 0 et 100
def is_valid_taux_avancement(taux_avancement):

    # Convertir la valeur en entier pour effectuer la vérification
    taux = int(taux_avancement)

    # Vérifier si le nombre est compris entre 0 et 100
    if 0 <= taux <= 100:
        return True
    else:
        return False
    

#Exemple d'éxécution de ces fonctions 

    #Add
#add_action('fe23-12', 'Action 1', '75', 'Finir avant le 24 juillet')
#add_action('fe32-19', 'Action 2', '15', 'Finir avant le 26 juillet')
#add_action('3', 'Action 3', '14', 'Finir avant le 29 juillet')

    #Select
#select_action('fe32-19')

    #Update  
#update_action('fe32-19')

    #Delete
#delete_action('3')


#PARTIE WEBB

#Page principale
@app.route('/', methods=['GET'])
def index():
    return render_template('Action.html')

#Fonction add qui récupère les données saisis dans le form
@app.route('/add', methods=['POST'])
def add():
    action_id = request.form['add_id']
    intitule = request.form['intitule']
    taux_avancement = request.form['taux_avancement']
    objectif = request.form['objectif']

    # Vérification du taux d'avancement
    # if not is_valid_taux_avancement(taux_avancement):
    #     return "Erreur : Le taux d'avancement doit être un nombre entre 0 et 100."

    add_action(action_id, intitule, taux_avancement, objectif)

    return redirect('/')

#Fonction select qui récupère l'ID et renvoie le reste des données associées
@app.route('/select', methods=['POST'])
def select():
    action_id = request.form['select_id']
    action = select_action(action_id)

    if action:
        # Si l'action est trouvée on renvoie les informations au template
        return render_template('Action.html', action=action, no_action=False)
    else:
        # Si l'action n'est pas trouvée on renvoie un message d'erreur
        return render_template('Action.html', no_action=True)

    #return redirect('/')


#Fonction update qui récupère les données saisis dans le form et les mets à jour dans la BDD
@app.route('/update', methods=['POST'])
def update():
    action_id = request.form['modif_id']
    intitule = request.form['new_intitule']
    taux_avancement = request.form['new_taux']
    objectif = request.form['new_objectif']

    # Vérification du taux d'avancement
    # if not is_valid_taux_avancement(taux_avancement):
    #     return "Erreur : Le taux d'avancement doit être un nombre entre 0 et 100."

    update_action(action_id, intitule, taux_avancement, objectif)
    return redirect('/')


#Fonction delete qui récupère l'ID saisis dans le form et supprime les données associées
@app.route('/delete', methods=['POST'])
def delete():
    action_id = request.form['delete_id']
    delete_action(action_id)
    return redirect('/')



