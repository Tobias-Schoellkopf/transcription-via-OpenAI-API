# Transkription einer Audiodatei mithilfe des OpenAI-Modells Whisper-v2 Large sowie gpt-4o

>🤖 Benötigt einen eigenen OpenAI-API-Key.

>🌐 Benötigt eine Internetverbindung.

>🍎 Nur getestet unter macOS.

<div align="justify">
  Dieses Projekt enthält drei verschiedene Python-Codes, welche zusammen mithilfe 
  eines OpenAI-API-Keys zur Transkription von Audiodateien verwendet werden können.
  Für zusätzliche Informationen zur Erstellung eines persönlichen API-Keys siehe 
  OpenAI's <a href="https://platform.openai.com/docs/api-reference/authentication">API Dokumentation</a>. 
  <b>Das eigentliche Transkriptionsskript ist <i>transcription-via-OpenAI-API.py</i>, für lange oder große Audiodateien
  wird allerdings eine Vor- und Nachbereitung mithilfe von <i>audio-split.py</i> und <i>add-minutes.py</i> empfohlen.</b>
</div>

### audio-split.py
> 🥚 Schritt 1: Pre-Processing
<div align="justify">
  Das eigentliche Transkriptionsskript kann aufgrund der Limitierung bezüglich des Whisper-v2 Large Modells seitens OpenAI nur Audiodateien mit einer Größe von Maximal 25 MB
  verarbeiten. Allerdings wird empfholen, dieses Maximum nicht auszureizen und kleinere Datein zu verwenden, da das ebenfalls verwendete gpt-4o Modell ein
  begrenztes <a href="https://platform.openai.com/docs/models/gp">Token Output Limit</a> von 16 384 Tokens (Stand: November 2024) besitzt <a href="https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them">(<i>Was ist ein Token?</i>)</a>. Wird eine Audiodatei mit besonders vielen Worten   (also entweder aufgrund der Länge oder der Wortdichte der Audiodatei) 
  verwendet, kann es passieren, dass die maximale Tokengröße überschritten wird. Dies macht sich dadurch bemerkbar, dass die Transkription in der finalen Textdatei an einem Punkt 
  abbricht.</p>
  
  <p> Das <i>audio-split.py</i> Skript unterteilt eine Audiodatei in Segmente mit einer Segmentlänge von acht Minuten. Außerdem werden die Segmente in das MP3-Format mit einer
  Bitrate von 64 kbps konvertiert. Dies ist für das Whisper-v2 Large Modell vollkommen ausreichend, verringert aber die Dateigröße. Bewährt haben sich <b>Segmentlängen von 8-10 Minuten</b>,
  je nach Inhalt könnten aber auch längere Segmente funktionieren, dies kann im Code selber verändert werden. </p>
</div>

### transcription-via-OpenAI-API.py
> 🐣 Schritt 2: Transkription
<div align="justify">
  <p> Dies ist das eigentliche Transkriptionsskript. Zunächst muss innerhalb der Python-Programmierumgebung der persönliche OpenAI-API-Key als Umgebungsvariable festgelegt werden. 
      Anschließend kann eine Audiodatei (oder eine Audiosegmentdatei, wie sie im ersten Schritt präpariert wurde) ausgewählt werden. Diese wird dann zunächst über einen ersten API-Aufruf Wort-für-Wort 
      mithilfe des Whisper-v2 Large modells transkribiert und jedes Wort mit einem Zeitstempel versehen. Die Wort-für-Wort transkription wird dann über einen zweiten API-Aufruf mithilfe des gpt-4o-Modells
      semantisch Nachbearbeitet, hierbei werden die Wörter kontextuell zu Sätzen, Sinnabschnitten und Sprechersegmenten unterteilt. Die Zeitstempel bleiben für jedes Sprechersegment erhalten. Das Ergebnis ist 
      eine Textdatei mit der finalen Transkription.</p>
</div>

> ⚠️ Dieser Schritt führt einen API-Call an das Whisper-v2 Large Modell sowie einen weiteren an das gpt-4o-Modell von OpenAI aus. Dementsprechend zu beachten sind die <a href="https://openai.com/api/pricing/">Kosten</a>, die sich nach der Anzahl der verarbeiteten Token richtet.

### add-minutes.py
> 🐥 Schritt 3: Post-Processing
<div align="justify">
  <p> Dieser Code kann verwendet werden, um die Zeitstempel eines Skripts um eine beliebige Zeit anzupassen. Die Zeit in Minuten wird dann auf jeden Zeitstempel addiert (oder subtrahiert, wenn eine negative Zahl eingegeben wird). Besonders nützlich, wenn zuvor eine längere Datei in verschiedene Segmente erstellt wurde vor dem Zusammenfügen der Segmente die Zeitstempel korrigiert werden sollen.
  </p>
