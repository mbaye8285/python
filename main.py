import sqlite3

# Connexion à la base (elle est créée si elle n'existe pas)
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

#creation de compte utilisateur
# main.py
def authenticate():
    username = input("Nom d'utilisateur: ")
    password = input("Mot de passe: ")
    
    if username == "mbayesarr" and password == "passer@1":
        print("Authentification réussie! Bienvenue .")
        return True
    else:
        print("Échec de l'authentification. Identifiants incorrects.")
        return False

if authenticate():
    # Votre code après authentification réussie
    print("Accès autorisé au programme...")

# Création de la table des tâches
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed INTEGER DEFAULT 0
    )
""")
conn.commit()

# Fonction d'affichage du menu
def afficher_menu():
    print("\n=== Gestionnaire de Tâches ===")
    print("1. Ajouter une tâche")
    print("2. Afficher les tâches")
    print("3. Marquer une tâche comme terminée")
    print("4. Supprimer une tâche")
    print("5. Quitter")

# Ajouter une tâche
def ajouter_tache():
    titre = input("Titre de la tâche : ")
    description = input("Description : ")
    cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (titre, description))
    conn.commit()
    print("Tâche ajoutée avec succès.")

# Afficher toutes les tâches
def afficher_taches():
    cursor.execute("SELECT * FROM tasks")
    taches = cursor.fetchall()
    if not taches:
        print("Aucune tâche enregistrée.")
    for t in taches:
        statut = "✔️" if t[3] else "❌"
        print(f"{t[0]}. {t[1]} - {statut} \n   Description : {t[2]}")

# Marquer une tâche comme terminée
def terminer_tache():
    id_tache = input("ID de la tâche à marquer comme terminée : ")
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (id_tache,))
    conn.commit()
    print("Tâche mise à jour.")

# Supprimer une tâche
def supprimer_tache():
    id_tache = input("ID de la tâche à supprimer : ")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id_tache,))
    conn.commit()
    print("Tâche supprimée.")

# Boucle principale
while True:
    afficher_menu()
    choix = input("Choix : ")
    if choix == '1':
        ajouter_tache()
    elif choix == '2':
        afficher_taches()
    elif choix == '3':
        terminer_tache()
    elif choix == '4':
        supprimer_tache()
    elif choix == '5':
        print("Fermeture...")
        break
    else:
        print("Choix invalide.")

# Fermer la connexion à la base
conn.close()
