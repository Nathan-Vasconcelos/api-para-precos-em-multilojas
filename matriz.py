import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

conexao = mysql.connector.connect(
    host='localhost',
    database='matriz',
    user='root',
    password=''
)


@app.route('/')
def homepage():
    return 'HOME PAGE API'


@app.route('/api')
def api():

    conexao = mysql.connector.connect(
        host='localhost',
        database='matriz',
        user='root',
        password=''
    )
    cursor = conexao.cursor()
    cursor.execute('select * from produtos')
    comando = cursor.fetchall()
    atualizacao = {'id': 0, 'nome': '', 'valor': 0}
    dic = {}
    for c in comando:
        atualizacao['id'] = c[0]
        atualizacao['nome'] = c[1]
        atualizacao['valor'] = c[2]
        dic[c[0]] = atualizacao.copy()
    resposta = dic
    return jsonify(resposta)


app.run()
