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

## Configurazione
Il file di configurazione comprende i seguenti parametri:
 - urlWebhookIFTTT: url del webhook per la chiamata al servizio IFTTT;
 - url: url homepage modem;
 - minutiAttesa: attesa, espressa in minuti, tra un controllo ed un'altra;
 - minimoBatteria: livello della batteria a cui si deve avviare la carica;
 - ipPresa: indirizzo ip della presa Tapo;
 - emailAccountTapo: email dell'account Tapo con cui è stato registrato il dispositivo;
 - passwordAccountTapo: password dell'account Tapo di cui è stato specificato l'email. ATTENZIONE: La password deve essere al massimo 8 caratteri. Leggere [P100 issues](https://github.com/fishbigger/TapoP100/issues);
 - pathLog: path del file log.

## Utilizzo
Prima di utilizzare lo script bisogna settare alcuni parametri nel file di configurazione. I parametri sono tutti obbligatori (per il momento). Una volta riempiti tutti i campi nel file di configurazione è possibile eseguire lo script tramite
```
python3 check.py ./config
```
Da notare che l'ultimo parametro è il file di configurazione ed è obbligatorio.
