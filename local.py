import tkinter.ttk
import requests
import mysql.connector
from produto import Produto
from tkinter import *


def limpar():
    produto.limpar_atualizacoes()


def filtrar_produtos():
    p = grade_produtos.get()
    if p == 'negativo':
        for i in tv.get_children():
           tv.delete(i)

        for (cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque) in produto.notificar_negativos():
            tv.insert('', 'end', values=(cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque))

    if p == 'aumento':
        for i in tv.get_children():
           tv.delete(i)

        for (cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque) in produto.notificar_aumento():
            tv.insert('', 'end', values=(cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque))

    if p == 'reducao':
        for i in tv.get_children():
            tv.delete(i)

        for (cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque) in produto.notificar_reducao():
            tv.insert('', 'end', values=(cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque))

    if p == 'negativo_aumento':
        for i in tv.get_children():
           tv.delete(i)

        for (cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque)\
                in produto.notificar_negativos_aumento():
            tv.insert('', 'end', values=(cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque))

    if p == 'negativo_reducao':
        for i in tv.get_children():
           tv.delete(i)

        for (cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque)\
                in produto.notificar_negativos_reducao():
            tv.insert('', 'end', values=(cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque))

    if p == 'padrao':
        for i in tv.get_children():
           tv.delete(i)

        for (cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque) in produto.notificar():
            tv.insert('', 'end', values=(cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque))


conexao = mysql.connector.connect(
    host='localhost',
    database='local',
    user='root',
    password=''
)

link = 'http://127.0.0.1:5000/api'
requisicao = requests.get(link)
# print(requisicao)
# print(requisicao.json())
matriz = requisicao.json()
produto = Produto(matriz)
produto.atualizar()


janela = Tk()
janela.configure(background='#006666')
janela.title('Baner')
texto_inicial = Label(janela, text='ALTERAÇÕES DE PREÇO.')
texto_inicial.grid(column=0, row=0, padx=10, pady=10)

texto_secundario = Label(janela, text='OS PRODUTOS A SEGUIR ESTÃO MUDANDO DE PREÇO')
texto_secundario.grid(column=0, row=1, padx=5, pady=10)


tv = tkinter.ttk.Treeview(janela, columns=('cod', 'descricao', 'preco', 'diferenca', 'aumento_reducao',
                                           'porcentagem', 'estoque'), show='headings')
tv.column('cod', minwidth=0, width=50)
tv.column('descricao', minwidth=0, width=100)
tv.column('preco', minwidth=0, width=100)
tv.column('diferenca', minwidth=0, width=100)
tv.column('aumento_reducao', minwidth=0, width=100)
tv.column('porcentagem', minwidth=0, width=100)
tv.column('estoque', minwidth=0, width=100)

tv.heading('cod', text='CÓD')
tv.heading('descricao', text='DESCRIÇÃO')
tv.heading('preco', text='PREÇO')
tv.heading('diferenca', text='DIFERENCA')
tv.heading('aumento_reducao', text='AUMENTO_REDUCAO')
tv.heading('porcentagem', text='PORCENTAGEM')
tv.heading('estoque', text='ESTOQUE')
tv.grid()

for (cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque) in produto.notificar():
    tv.insert('', 'end', values=(cod, descricao, preco, diferenca, aumento_reducao, porcentagem, estoque))

grade_produtos = StringVar()

texto_negativo = 'NEGATIVOS'
rb_negativo = Radiobutton(janela, text=f'{texto_negativo:<190}', value='negativo', variable=grade_produtos,
                          bg='#006666', fg='black')
rb_negativo.grid(column=0)

texto_aumento = 'AUMENTANDO'
rb_aumento = Radiobutton(janela, text=f'{texto_aumento:<185}', value='aumento', variable=grade_produtos,
                         bg='#006666', fg='black')
rb_aumento.grid(column=0)

texto_reducao = 'REDUZINDO'
rb_reducao = Radiobutton(janela, text=f'{texto_reducao:<190}', value='reducao', variable=grade_produtos,
                         bg='#006666', fg='black')
rb_reducao.grid(column=0)

texto_negativo_aumentando = 'NEGATIVOS AUMENTANDO'
rb_negativo_aumento = Radiobutton(janela, text=f'{texto_negativo_aumentando:<174}',
                                  value='negativo_aumento', variable=grade_produtos, bg='#006666', fg='black')
rb_negativo_aumento.grid(column=0)

texto_negativo_reduzindo = 'NEGATIVOS REDUZINDO'
rb_negativo_reducao = Radiobutton(janela, text=f'{texto_negativo_reduzindo:<179}',
                                  value='negativo_reducao', variable=grade_produtos, bg='#006666', fg='black')
rb_negativo_reducao.grid(column=0)

texto_padrao = 'PADRÃO'
rb_padrao = Radiobutton(janela, text=f'{texto_padrao:<193}', value='padrao', variable=grade_produtos,
                        bg='#006666', fg='black')
rb_padrao.grid(column=0)

texto_filtar = 'FILTRAR'
butao_filtrar = Button(janela, text=f'{texto_filtar:^20}', command=filtrar_produtos, bg='black', fg='white')
butao_filtrar.grid(columnspan=10, padx=10, pady=10)

butao_limpar = Button(janela, text=' LIMPAR ATUALIZAÇÕES ', command=limpar, bg='black', fg='white')
butao_limpar.grid(columnspan=10, padx=10, pady=10)

janela.mainloop()
