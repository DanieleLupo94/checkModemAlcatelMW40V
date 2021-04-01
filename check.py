import json
import sys
import time

import requests as req

d = {}
d["jsonrpc"] = "2.0"
d["method"] = "GetSystemStatus"
d["id"] = "13.4"
d["params"] = 'null'

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

def check():
    configurazione = getConfigurazione()
    r = req.post(configurazione["url"], data=json.dumps(d))
    informazioni = json.loads(r.content)["result"]
    batteria = int(informazioni["bat_cap"])
    # TODO Questo valore va preso dalla presa. Quando la batteria arriva al 100% restituirà sempre 1 (false)
    # TODO Controllare che in ac=1, altrimenti 2
    inCarica = informazioni["chg_state"]

    if (inCarica == 1):
        inCarica = True
    else:
        # Vale 2
        inCarica = False

    scriviLog("Batteria: " + str(batteria) + ", inCarica: " + str(inCarica))

    if inCarica:
        if batteria == 100:
            sendIFTTTNotification(configurazione["urlWebhook"], "Batteria carica del modem TIM")
            time.sleep(60 * 5)
            check()
        else:
            time.sleep(60 * int(configurazione["minutiAttesa"]))
            check()
    else:
        if batteria < 16:
            sendIFTTTNotification(configurazione["urlWebhook"], "Caricare modem TIM!!")
            time.sleep(60 * 5)
            check()
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

# Carico il file di configurazione passato da input
if len(sys.argv) != 2:
    raise ValueError('Bisogna passare il file di configurazione.')

pathFile = sys.argv[1]
scriviLog("Avvio")
check()
