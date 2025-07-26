"""
addfile.py

Script CLI per organizzare un singolo file in una struttura a cartelle basata sul tipo MIME.
Il file viene spostato in una sottocartella tematica (audio, immagini, documenti),
e un log viene aggiornato (o creato) nel file recap.csv.

Funzionalità:
- Identifica il tipo MIME del file (image, audio, document)
- Sposta il file nella sottocartella appropriata
- Crea la sottocartella se non esistente
- Aggiorna il file recap.csv con:
    - Nome file
    - Tipo MIME
    - Dimensione in byte
    - Cartella di destinazione

Esecuzione:
    python addfile.py nomefile.jpg --directory ./files

Requisiti:
    - Python ≥ 3.6
    - File da spostare presente nella directory indicata

Autore: Franco De Giorgio
Data: Luglio 2025
"""





import os           # per navigare nel filesystem: elencare file, controllare esistenza, creare directory, ottenere dimensioni
import shutil       # per spostare o copiare file da una cartella all'altra
import mimetypes    # per determinare il tipo MIME di un file (es. 'image/jpeg', 'audio/mpeg')
import csv          # per leggere e scrivere file CSV (usato per generare il log recap.csv)
import argparse     # per gestire argomenti passati da linea di comando (CLI)
import sys          # per terminare lo script in caso di errori critici (es. sys.exit(1))


def get_mime_type(file_path):
    """
    Restituisce il tipo MIME di un file, ad esempio 'image/png' o 'document/txt'.
    E la dimensione del file in byte
    Usa il modulo 'mimetypes' di Python che associa estensioni a tipi standardizzati.
    Args:
        file_path: percorso completo al file
    Returns:
        mime_type: stringa del tipo MIME (es. 'image/png')
        size: dimensione in byte
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'Tipo sconosciuto'
    size = os.path.getsize(file_path)
    return mime_type, size

def classifica_file(mime_type):
    """
    Classifica il file in base al tipo MIME.
    Ritorna 'audio', 'immagini', 'documenti' oppure None se non riconosciuto.
    """
    if mime_type is None:
        return None
    if mime_type.startswith('audio'):
        return 'audio'
    elif mime_type.startswith('image'):
        return 'immagini'
    elif mime_type.startswith('application') or mime_type.startswith('text'):
        return 'documenti'
    else:
        return None  # tipo sconosciuto

def sposta_file(file_path, folder_path, categoria):
    """
    Sposta il file nella sottocartella corrispondente alla categoria ('audio', 'immagini', 'documenti').
    Crea la sottocartella se non esiste.

    Args:
        file_path: percorso completo del file da spostare
        folder_path: percorso della cartella principale (es. './files')
        categoria: stringa con il nome della categoria
    """
    destinazione_cartella = os.path.join(folder_path, categoria)

    # Crazione cartella categoria se non esiste
    if not os.path.exists(destinazione_cartella):
        os.makedirs(destinazione_cartella)

    # Costruzione nuovo percorso file
    nome_file = os.path.basename(file_path)
    nuovo_percorso = os.path.join(destinazione_cartella, nome_file)

    # Sposta il file nella nuova posizione
    shutil.move(file_path, nuovo_percorso)

    # Percorso file
    return nuovo_percorso 

def scrivi_log_csv(file_info, csv_path):
    """
    Scrive una riga nel file CSV con le informazioni sul file spostato.

    Args:
        file_info: dizionario con le chiavi 'Nome', 'Tipo', 'Size'
        csv_path: percorso del file recap.csv
    """
    # Verifica se il file recap.csv esiste già
    file_esiste = os.path.exists(csv_path)

    # Apre il file in modalità append (aggiunta)
    with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
        # Definisce le intestazioni
        intestazioni = ['Nome', 'Tipo', 'Size Byte','Percorso']
        
        # Crea il writer
        writer = csv.DictWriter(csvfile, fieldnames=intestazioni)

        # Scrive l’intestazione solo se il file non esisteva
        if not file_esiste:
            writer.writeheader()
        
        # Scrive la riga del file corrente
        writer.writerow(file_info)



def main():
    """
    Funzione principale che gestisce l'organizzazione di un singolo file tramite CLI:
    lo classifica, sposta e registra un log nel file recap.csv.

    Args:
        folder_path: percorso alla cartella principale (es. './files')
    """

    # Definizione e parsing degli argomenti CLI in un'unica soluzione
    parser = argparse.ArgumentParser(
        description="Sposta un file in base alla tipologia MIME all'interno della relativa sotto cartella e crea un file recap.csv per il log",
        epilog="Esempio:\n  python addfile.py nomefile -d ./cartella\n"
               "Suggerimento:\n"
               "  Per conoscere i file validi spostabili in una cartella, esegui senza 'nomefile':\n"
               "  python addfile.py -d ./files",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('filename', nargs='?', help="Nome del file da spostare (obbligatorio)")
    parser.add_argument('-d', '--directory', type=str, help="Cartella da organizzare (es. './files')")

    args = parser.parse_args()

    # Gestione della cartella: priorità alla CLI, altrimenti input utente
    folder_path = args.directory
    if not folder_path:
        folder_path = input("Inserisci il percorso della cartella da organizzare (es. ./files): ")

    if not os.path.isdir(folder_path):
        print(f"Errore: la cartella '{folder_path}' non esiste o non è accessibile.")
        sys.exit(1)

    # Filtra i file spostabili e gestisce l'opzione di listing (senza filename)
    tipi_validi = ('image', 'audio', 'text', 'application')
    available_files = []
    for f in os.listdir(folder_path):
        full_path = os.path.join(folder_path, f)
        if os.path.isfile(full_path) and f != 'recap.csv':
            mime_info = mimetypes.guess_type(full_path)
            if mime_info[0] and mime_info[0].split('/')[0] in tipi_validi:
                available_files.append(f)
    available_files.sort()

    # Se non è stato fornito un nome file, elenca i file disponibili e termina
    if not args.filename:
        if available_files:
            print(f"File disponibili nella cartella '{folder_path}' da spostare:")
            for f in available_files:
                print(f"  - {f}")
        else:
            print(f"Nessun file valido da spostare trovato nella cartella '{folder_path}'.")
        sys.exit(0)

    # Validazione del nome file fornito
    filename = args.filename
    if filename not in available_files:
        print(f"Errore: Il file '{filename}' non è valido o non è presente nella cartella '{folder_path}' "
              "o il suo tipo non è supportato.")
        if available_files:
            print("File disponibili:")
            for f in available_files:
                print(f"  - {f}")
        sys.exit(1)

    # Processamento del file
    file_path = os.path.join(folder_path, filename)

    try:
        mime_type, size = get_mime_type(file_path)
    except Exception as e:
        print(f"Errore nel rilevare il tipo MIME o la dimensione del file '{filename}': {e}")
        sys.exit(1)

    categoria = classifica_file(mime_type)

    if categoria is None:
        print(f"File '{filename}' di tipo '{mime_type}' non riconosciuto, nessuna azione eseguita.")
        sys.exit(0) # Non è un errore critico, solo un file non gestibile

    try:
        nuovo_percorso = sposta_file(file_path, folder_path, categoria)
    except Exception as e:
        print(f"Errore durante lo spostamento del file '{filename}': {e}")
        sys.exit(1)

    file_info = {
        'Nome': filename,
        'Tipo': mime_type,
        'Size Byte': size,
        'Percorso': nuovo_percorso
    }

    csv_path = os.path.join(folder_path, 'recap.csv')
    try:
        scrivi_log_csv(file_info, csv_path)
    except Exception as e:
        print(f"Errore durante la scrittura del log nel file '{csv_path}': {e}")
        # Non blocca l'esecuzione se il file è già stato spostato
        pass

    print(f"\n--- Riepilogo Operazione ---")
    print(f"Nome: {filename}")
    print(f"Tipo: {mime_type}")
    print(f"Dimensione: {size} byte")
    print(f"Categoria: {categoria}/")
    print(f"Percorso aggiornato: {nuovo_percorso}")
    print(f"Log registrato in: {csv_path}")
    print("-" * 40)


if __name__=='__main__':
    main()