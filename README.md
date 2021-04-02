# checkModemAlcatelMW40V
 Programma che interroga la home del modem per recuperare informazioni, avvisare l'utente ed gestire l'alimentazione.

## Materiale utilizzato
 - Raspberry Pi 3B+;
 - presa Tapo TP-LINK P100;
 - modem Alcatel MW40V.

## Software utilizzato
 - Python3;
 - libreria [PyP100](https://github.com/fishbigger/TapoP100).

## Installazione
Per utilizzare questo script bisogna installare la versione 3 di Python (necessaria per la libreria PyP100).
Per installare PyP100 eseguire
```
pip3 install PyP100
```

## Utilizzo
Prima di utilizzare lo script bisogna settare alcuni parametri nel file di configurazione. I parametri sono tutti obbligatori (per il momento). Per utilizzare le notifiche IFTTT bisogna avere un account e creare un evento per ricevere le notifiche. Per poter utilizzare la presa Tapo c'è bisogno di configurarla tramite l'app Tapo (quindi bisogna creare l'account e collegare la presa alla rete).
Una volta riempiti tutti i campi nel file di configurazione è possibile eseguire lo script tramite
```
python3 check.py ./config
```
Da notare che l'ultimo parametro è il file di configurazione ed è obbligatorio.
