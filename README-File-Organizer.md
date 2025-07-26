# 📁 File Organizer e Analisi Immagini con Python

## 🔍 Introduzione

Questo progetto in **Python** ha come obiettivo l'organizzazione automatica dei file contenuti in una directory, seguita da un'analisi strutturata delle immagini tramite elaborazione numerica.

Il progetto è suddiviso in **due macro-fasi**:

---

## 🗂️ Step 1: Organizzazione automatica dei file

Lo script scorre **in ordine alfabetico** tutti i file presenti nella cartella principale (`./files`) e li sposta in una **sottocartella tematica**, determinata sulla base del tipo MIME del file (audio, documento o immagine).  
Se la sottocartella non esiste, viene **creata automaticamente**.

### 📌 Funzionalità:

- Determinazione automatica del tipo di file tramite `mimetypes`.
- Creazione dinamica delle cartelle di destinazione.
- Spostamento fisico dei file con tracciamento.
- Generazione (o aggiornamento) di un file `recap.csv` per tenere traccia degli spostamenti effettuati.

### 🧾 Output generato:

Per ogni file trattato, lo script stampa:
- **Nome del file**
- **Tipo MIME**
- **Dimensione (in byte)**
- **Cartella di destinazione**

### 🗃️ Esempio di struttura risultante:


### 📝 Il file `recap.csv`

Viene creato automaticamente se non esistente, e contiene le seguenti colonne:
- **Nome del file**
- **Tipo MIME**
- **Dimensione (in byte)**
---

## 🧪 Step 3: Analisi strutturale delle immagini

Questo step esegue un'**analisi automatica** della cartella `immagini/`, elaborando ogni file tramite la libreria `PIL` (Python Imaging Library) e convertendo ciascuna immagine in un array `NumPy` per l'analisi pixel-based.

### 🔍 Per ogni immagine, vengono estratte:

- **Nome del file**
- **Altezza** (in pixel)
- **Larghezza** (in pixel)
- **Media dei valori di colore**, a seconda del tipo di immagine:
  - Se l'immagine è in scala di grigi (tutti i canali RGB uguali pixel per pixel), viene calcolata la media dei valori del singolo canale e riportata nella colonna `grayscale`.
  - Se l'immagine è a colori (`RGB` o `RGBA`), vengono riportate le medie dei singoli canali: `R`, `G`, `B`, e `ALPHA`.

### 🧾 Esempio di tabella generata:

| name         | height | width | grayscale | R     | G     | B     | ALPHA |
|--------------|--------|-------|-----------|-------|-------|-------|--------|
| bw.png       | 512    | 512   | 124.1     | 0.0   | 0.0   | 0.0   | 0.0    |
| eclipse.png  | 1024   | 768   | 0.0       | 123.6 | 118.7 | 112.5 | 133.0  |
| trump.jpeg   | 800    | 600   | 0.0       | 134.2 | 126.9 | 119.5 | 0.0    |

> **Nota:** Se l'immagine non presenta trasparenza effettiva, il valore della colonna `ALPHA` è impostato a `0.0`.

---

## 🛠️ Librerie utilizzate

- `os`, `shutil` → gestione file e directory
- `mimetypes` → rilevamento tipo file
- `csv` → generazione e aggiornamento log `recap.csv`
- `argparse` → gestione della riga di comando
- `PIL.Image` → lettura ed elaborazione immagini
- `numpy` → elaborazione matriciale
- `tabulate` → visualizzazione tabellare ordinata

---

## ✅ Obiettivi raggiunti

- 🧠 Automazione dell'organizzazione dei file
- 🧾 Tracciabilità degli spostamenti tramite file `.csv`
- 🧬 Analisi automatica e dettagliata dei contenuti immagine
- 📊 Visualizzazione chiara dei risultati tramite tabella formattata

---

### 🧩 Panoramica delle Funzioni

| **Funzione**                           | **Responsabilità**                                                             |
|----------------------------------------|---------------------------------------------------------------------------------|
| `get_mime_type(file_path)`             | Restituisce tipo MIME e dimensione del file in byte                            |
| `classifica_file(mime_type)`           | Ritorna la categoria: `audio`, `immagini`, `documenti`, oppure `None`          |
| `sposta_file(file_path, destinazione)` | Crea la sottocartella se non esiste e vi sposta il file                        |
| `scrivi_log_csv(file_info, csv_path)`  | Aggiunge una riga al file `recap.csv` con nome, tipo e dimensione del file     |
| `organizza_files(folder_path)`         | Funzione principale: scorre i file, li classifica, li sposta e registra il log |
| `analizza_immagini(cartella_immagini)` | Analizza tutte le immagini nella cartella specificata e stampa la tabella      |

---

## 👨‍💻 Autore:

## ***Franco De Giorgio***  

📅 **Data di completamento:** Luglio 2025

---
