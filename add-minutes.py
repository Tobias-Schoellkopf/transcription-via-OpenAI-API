import re
from datetime import timedelta
import tkinter as tk
from tkinter import filedialog, simpledialog

def adjust_timestamps_in_file(input_path, output_path, offset_minutes):
    # Muster für den Zeitstempel [hh:mm:ss]
    timestamp_pattern = r'\[(\d{2}):(\d{2}):(\d{2})\]'
    offset = timedelta(minutes=offset_minutes)

    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    def add_offset(match):
        hours, minutes, seconds = map(int, match.groups())
        original_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        new_time = original_time + offset
        # Formatieren des neuen Zeitstempels in [hh:mm:ss]
        new_hours = str(new_time.seconds // 3600).zfill(2)
        new_minutes = str((new_time.seconds // 60) % 60).zfill(2)
        new_seconds = str(new_time.seconds % 60).zfill(2)
        return f'[{new_hours}:{new_minutes}:{new_seconds}]'

    # Ersetze alle Zeitstempel im Inhalt mit der add_offset-Funktion
    corrected_content = re.sub(timestamp_pattern, add_offset, content)

    # Schreibe das Ergebnis in die neue Datei
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(corrected_content)

    print(f"Datei mit korrigierten Zeitstempeln gespeichert unter: {output_path}")


# Tkinter-Root erzeugen und ausblenden
root = tk.Tk()
root.withdraw()

# Eingabedatei auswählen
input_path = filedialog.askopenfilename(
    title="Wähle die Eingabedatei mit den Zeitstempeln aus",
    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
)

if not input_path:
    print("Keine Eingabedatei ausgewählt. Programm wird beendet.")
    exit()

# Nach Anzahl der hinzuzufügenden Minuten fragen
offset_minutes = simpledialog.askinteger(
    "Zeitzuschlag",
    "Wie viele Minuten sollen auf die ursprünglichen Zeitstempel addiert werden?",
    parent=root,
    minvalue=0, maxvalue=10000
)

if offset_minutes is None:
    print("Keine Zeitangabe gemacht. Programm wird beendet.")
    exit()

# Ausgabedatei auswählen
output_path = filedialog.asksaveasfilename(
    title="Speichere die korrigierte Datei",
    defaultextension=".txt",
    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
)

if not output_path:
    print("Keine Ausgabedatei ausgewählt. Programm wird beendet.")
    exit()

# Funktion ausführen
adjust_timestamps_in_file(input_path, output_path, offset_minutes)

