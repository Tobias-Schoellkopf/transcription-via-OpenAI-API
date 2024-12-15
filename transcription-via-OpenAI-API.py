from openai import OpenAI
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

import platform
import subprocess

client = OpenAI()

# Initialisierung von tkinter für die graphische Benutzeroberfläche bei der Dateiauswahl
root = tk.Tk()
root.withdraw()  # Verstecken des root-Fensters

## Teil 1: Transkribieren mit Timestamps durch das Whisper-Modell von OpenAI über die OpenAI-API

# Öffnen des Dialogfensters, Benutzerauswahl der Audio-Rohdatei
file_path = filedialog.askopenfilename(title="Wähle eine Audiodatei zum Transkribieren. \nUnterstützte Formate: mp3, mp4, mpeg, mpga, m4a, wav, webm.\nMaximale Dateigröße 25 MB.")

# Öffnen der Audiodatei
audio_file = open(file_path, "rb")

# Verwenden der API für die Transkription
transcript = client.audio.transcriptions.create(
  file = audio_file,
  model = "whisper-1",
  response_format = "verbose_json",
  timestamp_granularities = ["word"],
  language = "de"
)

print(transcript.words) #Ausgabe der Transkription zur Überprüfung, ob alles geklappt hat

# Erstellen eines Dateinamens für den Output der Transkription mit Zeitstempel
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_path = f"transcription_output_{timestamp}.txt"

# Speichern der Transkription in einer Textdatei mit Dateinamen "transcription_output_YYYY-mm-dd-HH-MM-SS"
with open(output_path, "w") as text_file:
    for word_info in transcript.words:
        start = word_info.start or 0
        end = word_info.end or 0
        word = word_info.word or ""
        text_file.write(f"{start}-{end}: {word}\n")

print(f"Roh-Transkription gespeichert unter {output_path}")

## Teil 2: Öffnen der neu erstellten Transkribierten und gestampten Datei, Runden der Zeiten auf zwei Nachkommastellen
## und speichern in einer Variable

#Öffnen der Datei
with open(output_path, "rb") as file:
    content = file.read().decode()

#print(content) #nur zur Überprüfung entkommentieren, falls etwas nicht klappt

# Funktion für Konvertierung der Zeitstempel ins Format [HH:MM:SS]
def format_timestamp(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"[{int(hours):02}:{int(minutes):02}:{int(secs):02}]"

# Zeilenweise Bearbeitung, Runden der Sekunden in den Zeitstempeln, anschließend Konvertierung ins Format [HH:MM:SS] durch Aufruf der Hilfsfunktion
rounded_content = []
for line in content.splitlines():
    parts = line.split(": ")
    if len(parts) == 2:
        timestamps, word = parts
        try:
            # Umwandlung jedes Zeitstempels in eine Integer-Zahl, dann Umwandlung ins Format [HH:MM:SS]
            start, end = (format_timestamp(round(float(num))) for num in timestamps.split("-"))
            rounded_content.append(f"{start}-{end}: {word}")
        except ValueError as e:
            print(f"Error converting timestamps in line: {line}")
            print(f"Exception: {e}")
            rounded_content.append(line)
    else:
        # Falls kein Zeitstempel erkannt, Zeile einfach wieder anhängen
        rounded_content.append(line)

# Vereinigung aller Zeilen zu einem Text
rounded_stamped_transcribed = "\n".join(rounded_content)

# Zeitstempel erstellen für die Datei mit den geundeten Zeitstempeln
timestamp_rounding = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_path_rounding = f"rounded_transcription_output_{timestamp_rounding}.txt"

# Speichern der Datei mit den gerundeten Zeitstempeln
with open(output_path_rounding, "w") as output_file:
    output_file.write(rounded_stamped_transcribed)

print(f"Gerundete Transkription wurde in '{output_path_rounding}' gespeichert.")


#print(rounded_stamped_transcribed)  # Optional, um das Zwischenergebnis zu betrachten


## Teil 3: Zweiter API call an GPT-4-mini mit der Variable, die den transkribierten und gestampten Text enthält.
## GPT-4-mini soll daraus die Segmente schlussfolgern und stampen. Das Ergebnis wird als Textdatei ausgegeben.

completion = client.chat.completions.create(
    model="gpt-4o", #Zum Zeitpunkt der Ausführung des Codes äquivalent zum Modell gpt-4o-2024-08-06
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": (
                "Der folgende Text enthält eine Transkription eines Interviews zweier Personen, in dem jedes einzelne Wort mit einem Zeitstempel der Form [hh:mm:ss] versehen ist. Bitte unterteile den Text so, dass es eine Interview-Form besitzt."
                "Füge nur zu Beginn jedes Sprechteils einen Zeitstempel hinzu, der den Anfangszeitpunkt der Sprechphase markiert. Dieser sollte in der Form [Stunden:Minuten:Sekunden] vor der Sprechphase angegeben werden (inkllusive eckigen Klammern, also zB \"Sprecher A [00:00:20]: text von sprecher A \" für eine Sprechphase, die bei Sekunde 20 beginnt.). Der Zeitstempel soll in derselben Zeile wie die entsprechende Sprechphase stehen. Korrigiere zusätzlich Satzzeichen oder logische Fehler, die durch die Transkription entstanden sind, ändere aber nichts am Sinn."
                f"Das ist der Text: {rounded_stamped_transcribed}"
            )
        }
    ]
)


# Auswertung der Antwort von OpenAI
response_text = completion.choices[0].message.content

# Erstellung des Dateinamens mit Zeitstempel
timestamp_second_call = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"transcript_{timestamp_second_call}.txt"

# Speichern der Antwort in einer Textdatei
with open(filename, "w") as file:
    file.write(response_text)

print(f"Vollständiges Transkript gespeichert unter {filename}")

print(completion.choices[0].message)

# Speichern mit User-Dialog

save_path = filedialog.asksaveasfilename(
        title="Speicherort für transkribierte Datei auswählen",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        initialfile=filename
    )
if save_path:
    with open(save_path, "w") as file:
        file.write(response_text)
    messagebox.showinfo("Transkription abgeschlossen.", f"Transkript erfolgreich gespeichert unter {save_path}"
                        )
    # Öffnen des fertigen Transkripts

    confirm_open = messagebox.askyesno("Gleich öffnen?", "Möchtest du die Datei gleich öffnen?")

    if confirm_open:
        if platform.system() == "Windows":
            os.startfile(save_path)
        elif platform.system() == "Darwin":  # Darwin steht für macOS
            subprocess.call(["open", save_path])
        elif platform.system() == "Linux":
            subprocess.call(["xdg-open", save_path])
        else:
            print("Das Betriebssystem wird nicht unterstützt.")
else:
    messagebox.showinfo("Speichern abgebrochen", "Der Speicherort wurde nicht ausgewählt. Die Transkription wurde abgebrochen."
                        )

