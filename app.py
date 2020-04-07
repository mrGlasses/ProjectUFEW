from flask import Flask, jsonify
app = Flask(__name__)
from datetime import datetime
import re
import amelia
import configparser

#trueVer.bugFix.checkpoint.try
ver = '0.1.2.5'

conn = []
cnfer = configparser.ConfigParser()
cnfer.sections()
cnfer.read('config.cnf')
if 'DB' in cnfer:
    conn.append(cnfer['DB']['host'])
    conn.append(cnfer['DB']['user'])
    conn.append(cnfer['DB']['pass'])
    conn.append(cnfer['DB']['db'])

@app.route("/")
def home():
    return "Up! Credits To Nickolas G."

@app.route("/ver")
def verN():
    return ver

@app.route("/isConnected")
def alive():
    return amelia.isAlive(conn)

@app.route("/put/<Aparam>")
def openSP(Aparam):
    lister = Aparam.split('@')
    Aproc = lister[0]
    lister.pop(0)
    if len(lister) == 0:
        lister = ()
    content = amelia.ameliaGoProcExec(conn, Aproc, lister)
    content = jsonify(content)
    return content

@app.route("/do/<Aparam>")
def execSP(Aparam):
    lister = Aparam.split('@')
    Aproc = lister[0]
    lister.pop(0)
    if len(lister) == 0:
        lister = ()
    content = amelia.ameliaGoProcOpen(conn, Aproc, lister)
    content = jsonify(content)
    return content

@app.route("/neh")
def neh():
    return 'neh'

@app.route("/putter/<Aparam>")
def openSPA(Aparam):
    return Aparam

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




