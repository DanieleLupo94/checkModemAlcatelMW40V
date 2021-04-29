import json
import sys
import time

import requests as req
from PyP100 import PyP100

d = {}
d["jsonrpc"] = "2.0"
d["method"] = "GetSystemStatus"
d["id"] = "13.4"
d["params"] = 'null'

# Carico il file di configurazione passato da input
if len(sys.argv) != 2:
    raise ValueError('Bisogna passare il file di configurazione.')

pathFile = sys.argv[1]

def getConfigurazione():
    fileConfig = open(pathFile)
    configurazioni = {}
    for line in fileConfig.read().splitlines():
        configurazioni[line.split(' = ')[0]] = line.split(' = ')[1]
        '''if configurazioni[line.split(' = ')[0]] == 'True':
            configurazioni[line.split(' = ')[0]] = True
        if configurazioni[line.split(' = ')[0]] == 'False':
            configurazioni[line.split(' = ')[0]] = False'''
    return configurazioni

def getPresaTapo():
    configurazione = getConfigurazione()
    p100 = PyP100.P100(configurazione["ipPresa"], configurazione["emailAccountTapo"], configurazione["passwordAccountTapo"])
    p100.handshake() 
    p100.login()
    return p100, json.loads(p100.getDeviceInfo())["result"]

def accendiPresa(presa):
    presa.turnOn()
    presa, info = getPresaTapo()
    return info["device_on"] == True

def spegniPresa(presa):
    presa.turnOff()
    presa, info = getPresaTapo()
    return info["device_on"] == False

def check():
    configurazione = getConfigurazione()
    r = req.post(configurazione["url"], data=json.dumps(d))
    informazioni = json.loads(r.content)["result"]
    batteria = int(informazioni["bat_cap"])
    inCarica = informazioni["chg_state"]
    presa, informazioniPresa = getPresaTapo()
    statoPresa = informazioniPresa["device_on"]

    scriviLog("Batteria: " + str(batteria) + ", inCarica: " + str(inCarica) + ", statoPresa: " + str(statoPresa))

    if inCarica == 0:
        # Sta caricando
        time.sleep(60 * int(configurazione["minutiAttesa"]))
        check()
    elif inCarica == 1:
        # Ha finito di caricare
        sendIFTTTNotification(configurazione["urlWebhookIFTTT"], "Batteria carica del modem TIM")
        if spegniPresa(presa) == False:
            sendIFTTTNotification(configurazione["urlWebhookIFTTT"], "Errore nello spegnimento della presa Tapo")
        time.sleep(60 * 5)
        check()
    elif inCarica == 2:
        # Non è in carica
        if batteria < int(configurazione["minimoBatteria"]):
            sendIFTTTNotification(configurazione["urlWebhookIFTTT"], "Caricare modem TIM!!")
            if accendiPresa(presa) == False:
                sendIFTTTNotification(configurazione["urlWebhookIFTTT"], "Errore nell'accensione della presa Tapo")
            time.sleep(60 * 5)
        else:
            time.sleep(60 * int(configurazione["minutiAttesa"]))
        check()

def sendIFTTTNotification(urlWebhook = "", testo = ""):
    req.post(urlWebhook, json={'value1': testo})
    scriviLog("Notifica: " + testo)

def scriviLog(testo):
    pathLog = getConfigurazione()["pathLog"]
    fileLog = open(pathLog, "a+")
    # Aggiungo il timestamp al log
    t = "[" + time.asctime(time.localtime(time.time())) + "] " + str(testo)
    fileLog.write(t)
    fileLog.write("\n")
    fileLog.close()
    '''if getConfigurazione()["urlOnlineLogWriter"]:
        req.post(getConfigurazione()["urlOnlineLogWriter"], data={'riga': t})'''

def main():
    scriviLog("Avvio")
    check()

try:
    main()
except:
    scriviLog("Qualquadra non cosa")
    main()
finally:
    scriviLog("Passo e chiudo")
    configurazione = getConfigurazione()
    sendIFTTTNotification(configurazione["urlWebhookIFTTT"], "Programma terminato.")
    
