# Projekt
Das Projekt ist ein Verwaltungssystem für ToDo Listen.
Es gibt eine Hauptliste in der Alle ToDo Listen stehen. In jeder diese Listen können dann noch Einträge erstellt werden, die sogenannten ToDos.
Es können Listen erstellt, gelöscht werden. Bestehende Listen erweitert werden mit ToDos und ToDos können geändert werden.

# Endpunkte
Methode     Pfad (<Parameter>)                          Funktion

GET	        /todo-lists	                                Alle Listen abrufen
POST	    /todo-list	                                Neue Liste erstellen
GET	        /todo-list/<list_id>	                    Einzelne Liste abrufen
DELETE	    /todo-list/<list_id>	                    Liste und ihre Einträge löschen
POST	    /todo-list/<list_id>/entry	                Neuen Eintrag hinzufügen
PUT	        /todo-list/<list_id>/entry/<entry_id>	    Eintrag aktualisieren
DELETE	    /todo-list/<list_id>/entry/<entry_id>	    Eintrag löschen

# LICENCE
Dieses Projekt steht under der MIT-Lizenz. Siehe die LICENCE Datei für mehr Informationen