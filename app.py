from flask import Flask, jsonify
app = Flask(__name__)
from datetime import datetime
import re
import amelia
import configparser


def AnsiPos(subStr, fullStr):
    result = [pos for pos, char in enumerate(fullStr) if char == subStr]
    return result

#trueVer.bugFix.checkpoint.try
ver = '0.1.2.6'

conn = []
cnfer = configparser.ConfigParser()
cnfer.sections()
cnfer.read('config.cnf')
if 'DB' in cnfer:
    conn.append(cnfer['DB']['host'])
    conn.append(cnfer['DB']['user'])
    conn.append(cnfer['DB']['pass'])
    conn.append(cnfer['DB']['db'])

@app.route("/", methods=['GET', 'POST', 'PUT'])
def home():
    return "Up!"

@app.route("/ver", methods=['GET', 'POST', 'PUT'])
def verN():
    return ver

@app.route("/isConnected", methods=['GET', 'POST', 'PUT'])
def alive():
    return amelia.isAlive(conn)

@app.route("/put/<Aparam>", methods=['GET', 'POST', 'PUT'])
def openSP(Aparam):
    lister = Aparam.split('@')
    Aproc = lister[0]
    lister.pop(0)
    if len(lister) == 0:
        lister = ()
    content = amelia.ameliaGoProcOpen(conn, Aproc, lister)
    content = jsonify(content)
    return content

@app.route("/do/<Aparam>", methods=['GET', 'POST', 'PUT'])
def execSP(Aparam):
    lister = Aparam.split('@')
    Aproc = lister[0]
    lister.pop(0)
    if len(lister) == 0:
        lister = ()
    content = amelia.ameliaGoProcExec(conn, Aproc, lister)
    if len(AnsiPos('err', content)) == 0:
        content = 'ok'
    content = jsonify(content)
    return content

@app.route("/testeJson/", methods=['GET', 'POST', 'PUT'])
def teste():
    content = amelia.ameliaGoOpenSql(conn, "select 8, name from test")
    content = jsonify(content)
    return content

@app.route("/neh")
def neh():
    return 'neh'

@app.route("/putter/<Aparam>", methods=['GET', 'POST', 'PUT'])
def openSPA(Aparam):
    return Aparam

@app.route("/testeInsert/<insertClause>", methods=['GET', 'POST', 'PUT'])
def testeIn(insertClause):
    conexao = amelia.baseConnect('0.0.0.0', 'root', 'root', 'test')
    lcursor = conexao.cursor()
    query = amelia.simpleSqlExec(lcursor, "select " + insertClause)
    conexao.commit()
    content = jsonify(query)
    return content


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
