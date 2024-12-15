from pydub import AudioSegment

import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import os



def split_audio(file_path, segment_length=8 * 60 * 1000, output_dir=None):
    # Laden der Audiodatei
    audio = AudioSegment.from_file(file_path)

    # Berechnen der Segmentlänge
    total_length = len(audio)
    segments = []

    # Aufteilung der Audiodatei in Segmente
    for i in range(0, total_length, segment_length):
        start_time = i
        end_time = min(i + segment_length, total_length)
        segment = audio[start_time:end_time]
        segments.append(segment)

    # Falls kein Ausgabe-Verzeichnis übergeben wurde, Standard auf aktuelles Verzeichnis setzen
    if not output_dir:
        output_dir = os.getcwd()

    # Speichern jedes Segments im gewählten Verzeichnis
    for idx, segment in enumerate(segments):
        segment_filename = f"segment_{idx + 1}.mp3"
        segment_path = os.path.join(output_dir, segment_filename)
        segment.export(segment_path, format="mp3", bitrate="64k")

    print(f"Audio wurde in {len(segments)} Segmente aufgeteilt und gespeichert.")
    return segments

# Erstelle ein unsichtbares Tkinter-Fenster für Dialoge
root = tk.Tk()
root.withdraw()

# Schritt 1: Datei auswählen
file_path = filedialog.askopenfilename(
    title="Wähle eine Audiodatei aus",
    filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac *.m4a")]
)

if not file_path:
    print("Keine Datei ausgewählt. Das Programm wird beendet.")
else:
    # Schritt 2: Code ausführen (Segmentierung)
    segments = split_audio(file_path)

    # Schritt 3: Ausgabe-Verzeichnis auswählen
    output_dir = filedialog.askdirectory(title="Wähle ein Ausgabe-Verzeichnis für die Segmente")

    if not output_dir:
        print("Kein Ausgabe-Verzeichnis gewählt. Die Segmente liegen im aktuellen Verzeichnis.")
    else:
        # Segmente erneut mit bekanntem Ausgabe-Verzeichnis speichern
        split_audio(file_path, output_dir=output_dir)
        print(f"Segmente wurden im Verzeichnis {output_dir} gespeichert.")




