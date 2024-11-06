# Collaborative Project

Benvenuti nel repository **Collaborative Project**. Questo progetto include strumenti e funzionalità avanzate per il controllo vocale di un sistema di riconoscimento della parola chiave e di trascrizione automatica.

## Come clonare la repository

Per ottenere una copia locale del progetto, clona questa repository usando il comando seguente nel terminale:

```bash
git clone https://github.com/MatteoMissana/collaborative_project.git
```

Prima di eseguire il codice, assicurati di avere installato tutte le dipendenze necessarie. Queste sono specificate nel file requirements.txt. Puoi installarle utilizzando pip con il comando:

```bash 
pip install -r requirements.txt
```

Nota: Si consiglia di utilizzare un ambiente virtuale per mantenere le dipendenze isolate. Per creare un ambiente virtuale, esegui

```bash 
python -m venv nome_tuo_ambiente
```

e attivalo prima di installare i requisiti.

Per avviare il progetto, esegui semplicemente lo script version_2.py. Questo script inizierà ad ascoltare l’audio per rilevare parole chiave e trascriverle automaticamente.

```bash
python main.py
```

Assicurati di avere il microfono collegato e correttamente configurato sul tuo dispositivo, poiché il sistema si basa sull'input audio in tempo reale.

Se riscontri problemi con l'autenticazione o il riconoscimento della parola chiave, verifica che la tua chiave di accesso sia valida e aggiornata nel codice.

## .gitignore - Guida Rapida

Il file .gitignore indica a Git quali file e cartelle ignorare, evitando di tracciarli e committarli nel repository. È utile per escludere file generati automaticamente, di configurazione locale, o dati sensibili.

Come Funziona

Posizionamento: Inserisci .gitignore nella directory principale del progetto. Ogni entry sarà applicata a quella cartella e alle sue sottodirectory.

Sintassi Base:


nomefile.ext – Ignora file specifici

cartella/ – Ignora l’intera cartella

*.estensione – Ignora tutti i file con una specifica estensione (es. *.log)
