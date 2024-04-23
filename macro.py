import tkinter as tk
from tkinter import ttk
import keyboard
import time
import json

# Fonction pour exécuter une commande
def execute_command(command):
    keyboard.press('t')
    keyboard.release('t')
    time.sleep(0.1)  # Attente courte
    keyboard.write(command)
    time.sleep(0.1)  # Attente courte
    keyboard.press_and_release('enter')

# Gestionnaire d'événements pour la pression des touches
def on_key_press(event):
    if event.name in shortcuts:
        execute_command(shortcuts[event.name][1])
        print(f"Commande exécutée: {shortcuts[event.name][0]}")

# Fonction pour ajouter un raccourci personnalisé
def add_shortcut():
    key = entry_key.get()
    name = entry_name.get()
    command = entry_command.get()
    shortcuts[key] = (name, command)
    update_table()
    entry_key.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_command.delete(0, tk.END)
    save_shortcuts()

# Fonction pour sauvegarder les raccourcis dans un fichier .json
def save_shortcuts():
    with open("shortcuts.json", "w") as file:
        json.dump(shortcuts, file)

# Fonction pour charger les raccourcis depuis un fichier .json
def load_shortcuts():
    try:
        with open("shortcuts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Configuration de la fenêtre
window = tk.Tk()
window.title("Custom Shortcuts")
window.geometry("600x400")
window.config(bg="#f0f0f0")

# Création d'un style pour les boutons avec des bords arrondis
style = ttk.Style()
style.configure('TButton', font=("Arial", 12), padding=5, relief="raised", background="#66c2ff", foreground="#ffffff")
style.map('TButton', foreground=[('active', '#ffffff'), ('disabled', '#a3a3a3')], background=[('active', '#0077cc'), ('disabled', '#d9d9d9')])

# Création d'un libellé pour le titre
title_label = tk.Label(window, text="Custom Shortcuts", font=("Arial", 20), bg="#f0f0f0", pady=10)
title_label.pack()

# Création d'un cadre pour les raccourcis personnalisés
custom_frame = tk.Frame(window, bg="#f0f0f0")
custom_frame.pack()

# Zone de saisie pour ajouter un raccourci personnalisé
entry_key = tk.Entry(custom_frame, font=("Arial", 12), width=5, relief="solid", bd=1)
entry_key.grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(custom_frame, font=("Arial", 12), width=20, relief="solid", bd=1)
entry_name.grid(row=0, column=1, padx=10, pady=5)
entry_command = tk.Entry(custom_frame, font=("Arial", 12), width=30, relief="solid", bd=1)
entry_command.grid(row=0, column=2, padx=10, pady=5)
add_button = ttk.Button(custom_frame, text="Ajouter", command=add_shortcut)
add_button.grid(row=0, column=3, padx=10, pady=5)

# Création d'un cadre pour afficher les raccourcis personnalisés
table_frame = tk.Frame(window, bg="#f0f0f0")
table_frame.pack(pady=10)

# Charger les raccourcis depuis le fichier .json
shortcuts = load_shortcuts()

# Fonction pour mettre à jour le tableau avec les raccourcis personnalisés
def update_table():
    # Supprimer les lignes existantes du tableau
    for widget in table_frame.winfo_children():
        widget.destroy()
    
    # En-têtes du tableau
    tk.Label(table_frame, text="Touche clavier du Raccourci", font=("Arial", 14), bg="#f0f0f0", padx=10, pady=5, relief="solid", bd=1).grid(row=0, column=0)
    tk.Label(table_frame, text="Nom du raccourci", font=("Arial", 14), bg="#f0f0f0", padx=10, pady=5, relief="solid", bd=1).grid(row=0, column=1)
    tk.Label(table_frame, text="Commande à écrire", font=("Arial", 14), bg="#f0f0f0", padx=10, pady=5, relief="solid", bd=1).grid(row=0, column=2)

    # Afficher les raccourcis personnalisés dans le tableau
    row = 1
    for key, value in shortcuts.items():
        tk.Label(table_frame, text=key, font=("Arial", 12), bg="#f0f0f0", padx=10, pady=5, relief="solid", bd=1).grid(row=row, column=0)
        tk.Label(table_frame, text=value[0], font=("Arial", 12), bg="#f0f0f0", padx=10, pady=5, relief="solid", bd=1).grid(row=row, column=1)
        tk.Label(table_frame, text=value[1], font=("Arial", 12), bg="#f0f0f0", padx=10, pady=5, relief="solid", bd=1).grid(row=row, column=2)
        
        # Boutons pour modifier ou supprimer la commande
        edit_button = ttk.Button(table_frame, text="Modifier", command=lambda k=key: edit_shortcut(k))
        edit_button.grid(row=row, column=3, padx=5, pady=2)
        delete_button = ttk.Button(table_frame, text="Supprimer", command=lambda k=key: delete_shortcut(k))
        delete_button.grid(row=row, column=4, padx=5, pady=2)
        row += 1

# Fonction pour modifier un raccourci personnalisé
def edit_shortcut(key):
    entry_key.delete(0, tk.END)
    entry_key.insert(0, key)
    entry_name.delete(0, tk.END)
    entry_name.insert(0, shortcuts[key][0])
    entry_command.delete(0, tk.END)
    entry_command.insert(0, shortcuts[key][1])
    delete_shortcut(key)

# Fonction pour supprimer un raccourci personnalisé
def delete_shortcut(key):
    del shortcuts[key]
    update_table()
    save_shortcuts()

# Mise à jour initiale du tableau
update_table()

# Ajouter le gestionnaire d'événements pour la pression des touches
keyboard.on_press(on_key_press)

# Laisser le programme s'exécuter en boucle
window.mainloop()
