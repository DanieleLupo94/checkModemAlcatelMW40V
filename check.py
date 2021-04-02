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
    # TODO Controllare che in ac=1, altrimenti 2
    inCarica = informazioni["chg_state"]
    presa, informazioniPresa = getPresaTapo()
    statoPresa = informazioniPresa["device_on"]

    if (inCarica == 1):
        inCarica = True
    else:
        # Vale 2
        inCarica = False

    scriviLog("Batteria: " + str(batteria) + ", inCarica: " + str(inCarica) + ", statoPresa: " + str(statoPresa))

    if inCarica:
        if batteria == 100:
            sendIFTTTNotification(configurazione["urlWebhook"], "Batteria carica del modem TIM")
            if spegniPresa(presa) == False:
                sendIFTTTNotification(configurazione["urlWebhook"], "Errore nello spegnimento della presa Tapo")
            time.sleep(60 * 5)
        else:
            time.sleep(60 * int(configurazione["minutiAttesa"]))
    else:
        if batteria < 16:
            sendIFTTTNotification(configurazione["urlWebhook"], "Caricare modem TIM!!")
            if accendiPresa(presa) == False:
                sendIFTTTNotification(configurazione["urlWebhook"], "Errore nell'accensione della presa Tapo")
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

scriviLog("Avvio")
check()
