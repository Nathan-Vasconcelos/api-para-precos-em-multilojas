import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    database='local',
    user='root',
    password=''
)


class Produto:
    def __init__(self, matriz):
        self.matriz = matriz

        cursor = conexao.cursor()
        cursor.execute('select * from produtos')
        comando = cursor.fetchall()
        atualizacao = {'id': 0, 'nome': '', 'valor': 0, 'atualizado': '', 'diferenca': 0, 'aumento_reducao': '',
                       'estoque': 0}
        dic = {}
        for c in comando:
            atualizacao['id'] = c[0]
            atualizacao['nome'] = c[1]
            atualizacao['valor'] = c[2]
            atualizacao['atualizado'] = c[3]
            atualizacao['estoque'] = c[6]
            dic[c[0]] = atualizacao.copy()

        self.resposta = dic

    def atualizar(self):
        for i in range(1, len(self.matriz) + 1):

            if self.matriz[f'{i}']['valor'] != self.resposta[i]['valor']:
                diferenca = self.resposta[i]['valor'] - self.matriz[f'{i}']['valor']

                if diferenca < 0:
                    diferenca = diferenca * -1
                print(f"PRODUTO: {self.matriz[f'{i}']['nome']} NOVO VALOR: {self.matriz[f'{i}']['valor']}"
                      f" DIFERENÇA: {diferenca}")

                novo_valor = self.matriz[f'{i}']['valor']
                if novo_valor > self.resposta[i]['valor']:
                    self.resposta[i]['aumento_reducao'] = 'A'
                else:
                    self.resposta[i]['aumento_reducao'] = 'R'

                cursor = conexao.cursor()
                comando = f"""
                            update local.produtos set valor = {novo_valor}, atualizado = 'S', diferenca = {diferenca},
                            aumento_reducao = '{self.resposta[i]["aumento_reducao"]}'
                             where (id = '{self.resposta[i]["id"]}')
                """
                cursor.execute(comando)
                conexao.commit()

    def notificar(self):
        cursor = conexao.cursor()
        cursor.execute("""select id, nome, valor, diferenca, aumento_reducao, estoque from produtos
         where atualizado = 'S' and estoque > 0 order by diferenca desc;""")
        self.comando_notificar = cursor.fetchall()
        # print(f'{len(self.comando_notificar)} PRODUTOS COM ESTOQUE POSITIVO MUDARAM DE PREÇO')

        cursor = conexao.cursor()
        cursor.execute("""select id, nome, valor, diferenca, aumento_reducao, estoque from produtos
                 where atualizado = 'S' and estoque <= 0 order by diferenca desc;""")
        self.comando_notificar_negativos = cursor.fetchall()

        lista_provisoria = []
        lista_produtos = []
        for i in self.comando_notificar:
            self.porcentagem_aumento_reducao(i[4], i[3], i[2])
            lista_provisoria.append(i[0])
            lista_provisoria.append(i[1])
            lista_provisoria.append(f'{i[2]:.2f}')
            lista_provisoria.append(f'{i[3]:.2f}')
            lista_provisoria.append(self.palavra)
            lista_provisoria.append(f'{self.porcentagem:.1f}%')
            lista_provisoria.append(i[5])
            lista_produtos.append(lista_provisoria[:])
            lista_provisoria.clear()
        return lista_produtos

    def notificar_negativos(self):
        # print(f'{len(self.comando_notificar_negativos)} PRODUTOS COM ESTOQUE NEGATIVO MUDARAM DE PREÇO')

        lista_provisoria = []
        lista_produtos = []
        for i in self.comando_notificar_negativos:
            self.porcentagem_aumento_reducao(i[4], i[3], i[2])
            lista_provisoria.append(i[0])
            lista_provisoria.append(i[1])
            lista_provisoria.append(f'{i[2]:.2f}')
            lista_provisoria.append(f'{i[3]:.2f}')
            lista_provisoria.append(self.palavra)
            lista_provisoria.append(f'{self.porcentagem:.1f}%')
            lista_provisoria.append(i[5])
            lista_produtos.append(lista_provisoria[:])
            lista_provisoria.clear()
        return lista_produtos

    def notificar_aumento(self):
        lista_provisoria = []
        lista_produtos = []
        for i in self.comando_notificar:
            self.porcentagem_aumento_reducao(i[4], i[3], i[2])
            if self.palavra == 'aumento':
                lista_provisoria.append(i[0])
                lista_provisoria.append(i[1])
                lista_provisoria.append(f'{i[2]:.2f}')
                lista_provisoria.append(f'{i[3]:.2f}')
                lista_provisoria.append(self.palavra)
                lista_provisoria.append(f'{self.porcentagem:.1f}%')
                lista_provisoria.append(i[5])
                lista_produtos.append(lista_provisoria[:])
                lista_provisoria.clear()
        return lista_produtos

    def notificar_reducao(self):
        lista_provisoria = []
        lista_produtos = []
        for i in self.comando_notificar:
            self.porcentagem_aumento_reducao(i[4], i[3], i[2])
            if self.palavra == 'redução':
                lista_provisoria.append(i[0])
                lista_provisoria.append(i[1])
                lista_provisoria.append(f'{i[2]:.2f}')
                lista_provisoria.append(f'{i[3]:.2f}')
                lista_provisoria.append(self.palavra)
                lista_provisoria.append(f'{self.porcentagem:.1f}%')
                lista_provisoria.append(i[5])
                lista_produtos.append(lista_provisoria[:])
                lista_provisoria.clear()
        return lista_produtos

    def notificar_negativos_aumento(self):
        lista_provisoria = []
        lista_produtos = []
        for i in self.comando_notificar_negativos:
            self.porcentagem_aumento_reducao(i[4], i[3], i[2])
            if self.palavra == 'aumento':
                lista_provisoria.append(i[0])
                lista_provisoria.append(i[1])
                lista_provisoria.append(f'{i[2]:.2f}')
                lista_provisoria.append(f'{i[3]:.2f}')
                lista_provisoria.append(self.palavra)
                lista_provisoria.append(f'{self.porcentagem:.1f}%')
                lista_provisoria.append(i[5])
                lista_produtos.append(lista_provisoria[:])
                lista_provisoria.clear()
        return lista_produtos

    def notificar_negativos_reducao(self):
        lista_provisoria = []
        lista_produtos = []
        for i in self.comando_notificar_negativos:
            self.porcentagem_aumento_reducao(i[4], i[3], i[2])
            if self.palavra == 'redução':
                lista_provisoria.append(i[0])
                lista_provisoria.append(i[1])
                lista_provisoria.append(f'{i[2]:.2f}')
                lista_provisoria.append(f'{i[3]:.2f}')
                lista_provisoria.append(self.palavra)
                lista_provisoria.append(f'{self.porcentagem:.1f}%')
                lista_provisoria.append(i[5])
                lista_produtos.append(lista_provisoria[:])
                lista_provisoria.clear()
        return lista_produtos

    def porcentagem_aumento_reducao(self, i, diferenca, valor):
        if i == 'R':
            self.palavra = 'redução'
            self.porcentagem = diferenca * 100 / (valor + diferenca)

        else:
            self.palavra = 'aumento'
            self.porcentagem = diferenca * 100 / (valor - diferenca)

    @staticmethod
    def limpar_atualizacoes():
        cursor = conexao.cursor()
        cursor.execute("update local.produtos set atualizado = 'N', diferenca = null, aumento_reducao = null")
        conexao.commit()
