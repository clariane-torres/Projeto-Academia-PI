from PyQt5 import uic,QtWidgets #importar uic e QTWigets do pyqt5 #ler o arquivo .ui e para montar os elementos em uma tela
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
import datetime
# from reportlab.pdfgen import canvas

#configurar conexão com o BD
banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "academia"

)


#************* Funcionalidades LOGIN e USUÁRIO****************
def login_dados():
    tela_login.label_6.setText("")
    nome_usuario = tela_login.lineEdit.text()
    senha = tela_login.lineEdit_2.text()

    cursor = banco.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE login=%s", (nome_usuario,))
    resultado = cursor.fetchone()
    

    if resultado: #se encontrou algum nome de usuário com o nome de usuário fornecido
        senha_armazenada = resultado[0]
        if senha == senha_armazenada:
            tela_login.close()
            tela_principal.show()
        else:
            tela_login.label_6.setText("senha incorreta!")
            tela_login.lineEdit.setText("")
            tela_login.lineEdit_2.setText("")
        
    else:
        tela_login.label_6.setText("Usuário não encontrado!")
        tela_login.lineEdit.setText("")
        tela_login.lineEdit_2.setText("")

def abrir_cadastro():
    tela_cadastro.show()

def cadastro_usuario():
    nome = tela_cadastro.lineEdit.text()
    login = tela_cadastro.lineEdit_2.text()
    senha = tela_cadastro.lineEdit_3.text()
    c_senha = tela_cadastro.lineEdit_4.text()

    if senha != c_senha:
        QMessageBox.warning(tela_cadastro, "Erro", "As senhas não coincidem.")
        tela_cadastro.lineEdit.setText("")
        tela_cadastro.lineEdit_2.setText("")
        tela_cadastro.lineEdit_3.setText("")
        tela_cadastro.lineEdit_4.setText("")
        return
    
    try:
        cursor = banco.cursor()
        comandoSQL = "INSERT INTO usuarios (nome, login, senha, c_senha) VALUES (%s,%s,%s,%s)"
        dados = (str(nome), str(login), str(senha), str(c_senha))
        cursor.execute(comandoSQL, dados)
        banco.commit()
        QMessageBox.information(tela_cadastro, "SUCESSO", "Usuário cadastrado com sucesso!")
        tela_cadastro.close() # fechar a janela de cadastro após o sucesso do cadastro

    except Exception as e:
        QMessageBox.critical(tela_cadastro, "Erro", f"Erro ao cadastrar usuário: {e}")

#************* Funcionalidades CLIENTE****************
def abrir_tela_cadastro_clientes():
    tela_principal.hide()
    tela_cadastro_clientes.show()

def excluir_dados_clientes():
    linha = tela_listar_clientes.tableWidget.currentRow()
    tela_listar_clientes.tableWidget.removeRow(linha)


    cursor = banco.cursor()
    cursor.execute("SELECT id FROM cliente")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos [linha][0]
    cursor.execute("DELETE FROM cliente WHERE id =" + str(valor_id))
    banco.commit()

def salvar_cadastro_clientes():
    campo1 = tela_cadastro_clientes.lineEdit.text()
    campo2 = tela_cadastro_clientes.lineEdit_2.text()
    campo3 = tela_cadastro_clientes.lineEdit_3.text()
    campo4 = tela_cadastro_clientes.comboBox_3.currentText()
    campo5 = tela_cadastro_clientes.lineEdit_4.text()
    campo6 = tela_cadastro_clientes.lineEdit_5.text()
    campo7 = tela_cadastro_clientes.lineEdit_6.text()
    campo8 = tela_cadastro_clientes.lineEdit_7.text()
    campo9 = tela_cadastro_clientes.lineEdit_8.text()   
    campo10 = tela_cadastro_clientes.comboBox.currentText()
    campo11 = tela_cadastro_clientes.comboBox_2.currentText()

    print(campo1,campo2,campo3,campo4,campo5,campo6,campo7,campo8,campo9,campo10,campo11)

    #Configuração a ação no BD
    cursor = banco.cursor()
    comando_sql = "INSERT INTO cliente (nome, cpf, telefone, sexo, data_de_nascimento, email, endereco,bairro,cep, cidade, estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    dados = (str(campo1),str (campo2),str (campo3),str (campo4),str (campo5),str (campo6),str (campo7),str (campo8),str (campo9),str (campo10),str (campo11))
    cursor.execute(comando_sql, dados)
    banco.commit()
    QMessageBox.information(tela_cadastro_clientes, "SUCESSO", "Cliente cadastrado com sucesso!")
    tela_cadastro_clientes.lineEdit.setText("")
    tela_cadastro_clientes.lineEdit_2.setText("")
    tela_cadastro_clientes.lineEdit_3.setText("")
    tela_cadastro_clientes.lineEdit_4.setText("")
    tela_cadastro_clientes.lineEdit_5.setText("")
    tela_cadastro_clientes.lineEdit_6.setText("")
    tela_cadastro_clientes.lineEdit_7.setText("")
    tela_cadastro_clientes.lineEdit_8.setText("")


def abrir_listar_cliente():
    tela_principal.hide()
    tela_listar_clientes.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM cliente"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    print(dados_lidos)
    
    tela_listar_clientes.tableWidget.setRowCount(len(dados_lidos))#definir o nº de linhas da tabela
    tela_listar_clientes.tableWidget.setColumnCount(12)#definir o nº de colunas da tabela

    for i in range(0,len(dados_lidos)):
        for j in range(0,12):
            tela_listar_clientes.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 


def tela_cadastro_clientes_voltar():
    tela_cadastro_clientes.hide()
    tela_principal.show()


def tela_listar_clientes_voltar():
    tela_listar_clientes.hide()
    tela_cadastro_clientes.show()

def tela_editar_cliente_voltar():
    tela_editar_cliente.hide()
    tela_listar_clientes.show()

# def abrir_editar_cliente():
#     tela_editar_cliente.show()


def editar_cliente():
    global editar_id

    linha = tela_listar_clientes.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM cliente")
    dados_lidos = cursor.fetchall()
    cliente_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM cliente WHERE id="+ str(cliente_id))
    produtos = cursor.fetchall()
    tela_editar_cliente.show()

    tela_editar_cliente.lineEdit.setText(str(produtos[0][0]))
    tela_editar_cliente.lineEdit_2.setText(str(produtos[0][1]))
    tela_editar_cliente.lineEdit_3.setText(str(produtos[0][2]))
    tela_editar_cliente.lineEdit_4.setText(str(produtos[0][3]))
    tela_editar_cliente.lineEdit_5.setText(str(produtos[0][4]))
    tela_editar_cliente.lineEdit_6.setText(str(produtos[0][5]))
    tela_editar_cliente.lineEdit_7.setText(str(produtos[0][6]))
    tela_editar_cliente.lineEdit_8.setText(str(produtos[0][7]))
    tela_editar_cliente.lineEdit_9.setText(str(produtos[0][8]))
    tela_editar_cliente.lineEdit_10.setText(str(produtos[0][9]))
    tela_editar_cliente.lineEdit_11.setText(str(produtos[0][10]))
    tela_editar_cliente.lineEdit_12.setText(str(produtos[0][11]))
    editar_id = cliente_id
    
def salvar_editar_clientes():
    global editar_id
    #ler dados do lineEdit
    codigo = tela_editar_cliente.lineEdit.text()
    nome = tela_editar_cliente.lineEdit_2.text()
    cpf = tela_editar_cliente.lineEdit_3.text()
    telefone = tela_editar_cliente.lineEdit_4.text()
    sexo = tela_editar_cliente.lineEdit_5.text()
    dt_nasc = tela_editar_cliente.lineEdit_6.text()
    email = tela_editar_cliente.lineEdit_7.text()
    endereco = tela_editar_cliente.lineEdit_8.text()
    bairro = tela_editar_cliente.lineEdit_9.text()
    cep = tela_editar_cliente.lineEdit_10.text()
    cidade = tela_editar_cliente.lineEdit_11.text()
    estado = tela_editar_cliente.lineEdit_12.text()

    #atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute(f"UPDATE cliente SET nome = '{nome}', cpf = '{cpf}', telefone = '{telefone}', sexo = '{sexo}', data_de_nascimento = '{dt_nasc}', email = '{email}', endereco = '{endereco}', bairro = '{bairro}', cep = '{cep}', cidade = '{cidade}', estado = '{estado}' WHERE id = '{editar_id}'")
    banco.commit()

    
    #atualizar as janelas 
    tela_editar_cliente.close()
    tela_listar_clientes.close()
    abrir_listar_cliente()
    
    


#************* Funcionalidades MODALIDADES****************
def salvar_modalidades():
    campo1 = tela_modalidades.comboBox.currentText()
    campo2 = tela_modalidades.textEdit.toPlainText()
    print(campo1, campo2)
    cursor = banco.cursor()
    comando_sql = "INSERT INTO modalidades (nome, descricao) VALUES (%s,%s)"
    dados = (str(campo1),str (campo2))
    cursor.execute(comando_sql, dados)
    banco.commit()
    QMessageBox.information(tela_modalidades, "SUCESSO", "Modalidade cadastrado com sucesso!")
    tela_modalidades.textEdit.setText("")
    
    
def abrir_tela_modalidades():
    tela_modalidades.show()

def tela_modalidades_voltar():
    tela_modalidades.hide()
    tela_principal.show()

def listar_modalidades():
    tela_principal.hide()
    tela_listar_modalidades.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM modalidades"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    print(dados_lidos)
    
    tela_listar_modalidades.tableWidget.setRowCount(len(dados_lidos))#definir o nº de linhas da tabela
    tela_listar_modalidades.tableWidget.setColumnCount(3)#definir o nº de colunas da tabela

    for i in range(0,len(dados_lidos)):
        for j in range(0,3):
            tela_listar_modalidades.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 

# def abrir_editar_modalidade():
#     tela_editar_modalidade.show()


def excluir_dados_modalidades():
    linha = tela_listar_modalidades.tableWidget.currentRow()
    tela_listar_modalidades.tableWidget.removeRow(linha)


    cursor = banco.cursor()
    cursor.execute("SELECT id FROM modalidades")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos [linha][0]
    cursor.execute("DELETE FROM modalidades WHERE id =" + str(valor_id))
    banco.commit()


def editar_modalidade():
    global editar_id

    linha = tela_listar_modalidades.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM modalidades")
    dados_lidos = cursor.fetchall()
    modalidade_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM modalidades WHERE id="+ str(modalidade_id))
    produtos = cursor.fetchall()
    tela_editar_modalidade.show()

    tela_editar_modalidade.lineEdit.setText(str(produtos[0][0]))
    tela_editar_modalidade.lineEdit_2.setText(str(produtos[0][1]))
    tela_editar_modalidade.lineEdit_3.setText(str(produtos[0][2]))
    editar_id = modalidade_id
    
def salvar_editar_modalidades():
    global editar_id
    #ler dados do lineEdit
    codigo = tela_editar_modalidade.lineEdit.text()
    nome = tela_editar_modalidade.lineEdit_2.text()
    descricao = tela_editar_modalidade.lineEdit_3.text()
   
    #atualizar os dados no banco
    cursor = banco.cursor()
    
    cursor.execute(f"UPDATE modalidades SET nome = '{nome}', descricao = '{descricao}' WHERE id = '{editar_id}'")
    banco.commit()

    
    #atualizar as janelas 
    tela_editar_modalidade.close()
    tela_listar_modalidades.close()
    listar_modalidades()




def tela_listar_modalidades_voltar():
    tela_listar_modalidades.hide()
    tela_editar_modalidade.show()

def editar_modalidades_voltar():
    tela_listar_modalidades.hide()###################
    tela_modalidades.show()

def tela_editar_modalidades_voltar():
    tela_editar_modalidade.hide()
    tela_listar_modalidades.show()




#************* Funcionalidades PLANOS****************
def abrir_tela_planos():
    tela_planos.show()



def listar_planos():######################################################
    tela_principal.hide()
    tela_listar_planos.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM plano"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    print(dados_lidos)
    
    tela_listar_planos.tableWidget.setRowCount(len(dados_lidos))#definir o nº de linhas da tabela
    tela_listar_planos.tableWidget.setColumnCount(4)#definir o nº de colunas da tabela

    for i in range(0,len(dados_lidos)):
        for j in range(0,4):
            tela_listar_planos.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def salvar_planos():
     campo1 = tela_planos.lineEdit.text()
     campo2 = tela_planos.lineEdit_2.text()
     campo3 = tela_planos.lineEdit_3.text()
     print(campo1, campo2, campo3)
     cursor = banco.cursor()
     comando_sql = "INSERT INTO plano (nome, valores, descricao) VALUES (%s,%s,%s)"
     dados = (str(campo1), str(campo2), str(campo3))
     cursor.execute(comando_sql, dados)
     banco.commit()
     QMessageBox.information(tela_planos, "SUCESSO", "Plano cadastrado com sucesso!")
     tela_planos.lineEdit.setText("")
     tela_planos.lineEdit_2.setText("")
     tela_planos.lineEdit_3.setText("")

def tela_planos_voltar():
    tela_planos.hide()
    tela_principal.show()

def abrir_tela_listar_plano():
    tela_listar_planos.show()

def editar_plano():
    global editar_id

    linha = tela_listar_planos.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM plano")
    dados_lidos = cursor.fetchall()
    plano_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM plano WHERE id="+ str(plano_id))
    produtos = cursor.fetchall()
    tela_editar_planos.show()

    tela_editar_planos.lineEdit_4.setText(str(produtos[0][0]))
    tela_editar_planos.lineEdit.setText(str(produtos[0][1]))
    tela_editar_planos.lineEdit_2.setText(str(produtos[0][2]))
    tela_editar_planos.lineEdit_3.setText(str(produtos[0][3]))
    editar_id = plano_id
    
def salvar_editar_planos():
    global editar_id
    #ler dados do lineEdit
    nome = tela_editar_planos.lineEdit.text()
    valores = tela_editar_planos.lineEdit_2.text()
    descricao = tela_editar_planos.lineEdit_3.text()
   
    #atualizar os dados no banco
    cursor = banco.cursor()
    
    cursor.execute(f"UPDATE plano SET nome = '{nome}', valores = '{valores}', descricao ='{descricao}' WHERE id = '{editar_id}'")
    banco.commit()

    
    #atualizar as janelas 
    tela_editar_planos.close()
    tela_listar_planos.close()
    listar_planos()


def abrir_tela_editar_plano():
    tela_editar_planos.show()

def tela_listar_planos_voltar():
    tela_listar_planos.hide()
    tela_planos.show()

def tela_editar_planos_voltar():
    tela_editar_planos.hide()
    tela_listar_planos.show()

def excluir_dados_planos():
    linha = tela_listar_planos.tableWidget.currentRow()
    tela_listar_planos.tableWidget.removeRow(linha)


    cursor = banco.cursor()
    cursor.execute("SELECT id FROM plano")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos [linha][0]
    cursor.execute("DELETE FROM plano WHERE id =" + str(valor_id))
    banco.commit()

#************* Funcionalidades MATRICULA****************
def abrir_tela_editar_matricula():
    tela_editar_matricula.show()

def listar_matricula():
    tela_principal.hide()
    tela_listar_matriculas.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM matricula"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    print(dados_lidos)
    
    tela_listar_matriculas.tableWidget.setRowCount(len(dados_lidos))#definir o nº de linhas da tabela
    tela_listar_matriculas.tableWidget.setColumnCount(5)#definir o nº de colunas da tabela

    for i in range(0,len(dados_lidos)):
        for j in range(0,5):
            tela_listar_matriculas.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def abrir_tela_editar_matriculas():
    tela_listar_matriculas.show()

def abrir_tela_matricula():
    tela_matricula.show()
    tela_matricula.lineEdit_4.setText(str(data_formatada))

def buscar_clienteMatricula():
     global numero_id
     linha = tela_listar_clientes.tableWidget.currentRow()

     cursor = banco.cursor()
     cursor.execute("SELECT id FROM cliente")
     dados_lidos = cursor.fetchall()
     valor_id = dados_lidos[linha][0]
     cursor.execute("SELECT * FROM cliente WHERE id=" + str (valor_id))
     cliente = cursor.fetchall()
     tela_matricula.show()
     tela_listar_clientes.close()

     tela_matricula.lineEdit.setText(str(cliente[0][0]))
     tela_matricula.lineEdit_2.setText(str(cliente[0][1]))
     
     numero_id = valor_id   

def buscar_vendaMatricula():
     global numero_id
     linha = tela_listar_clientes.tableWidget.currentRow()

     cursor = banco.cursor()
     cursor.execute("SELECT id FROM cliente")
     dados_lidos = cursor.fetchall()
     valor_id = dados_lidos[linha][0]
     cursor.execute("SELECT * FROM venda WHERE id=" + str (valor_id))
     cliente = cursor.fetchall()
     tela_matricula.show()
     tela_listar_vendas.close()

     tela_matricula.lineEdit_3.setText(str(cliente[0][0]))
     
     
     numero_id = valor_id   

def salvar_matricula():
    campo1 = tela_matricula.lineEdit.text()
    campo2 = tela_matricula.lineEdit_3.text()
    campo3 = data_formatada
    campo4 = tela_matricula.lineEdit_5.text()
    campo5 = tela_matricula.comboBox.currentText()
    
    print(campo1, campo2, campo3, campo4, campo5)
    cursor = banco.cursor()
    comando_sql = "INSERT INTO matricula (id_cliente, id_venda, dt_matricula, validade, tp_pagamento ) VALUES (%s,%s,%s,%s,%s)"
    dados = (str(campo1),str (campo2),data_formatada, str(campo4), str(campo5))
    cursor.execute(comando_sql, dados)
    banco.commit()
    QMessageBox.information(tela_matricula, "SUCESSO", "Matrícula realizada com sucesso!")
    tela_matricula.lineEdit.setText("")
    tela_matricula.lineEdit_2.setText("")
    tela_matricula.lineEdit_3.setText("")
    tela_matricula.lineEdit_4.setText("")
    tela_matricula.lineEdit_5.setText("")
    

def tela_matricula_voltar():
    tela_matricula.hide()
    tela_principal.show()

def tela_listar_matriculas_voltar():
    tela_listar_matriculas.hide()
    tela_matricula.show()

def tela_editar_matricula_voltar():
    tela_editar_matricula.hide()
    tela_listar_matriculas.show()

def excluir_dados_matricula():
    linha = tela_listar_matriculas.tableWidget.currentRow()
    tela_listar_matriculas.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM matricula")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos [linha][0]
    cursor.execute("DELETE FROM matricula WHERE id =" + str(valor_id))
    banco.commit()

#************* Funcionalidades VENDAS****************
    
def abrir_tela_editar_vendas():
    tela_listar_vendas.show()

def listar_vendas():
    tela_principal.hide()
    tela_listar_vendas.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM venda"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    print(dados_lidos)
    
    tela_listar_vendas.tableWidget.setRowCount(len(dados_lidos))#definir o nº de linhas da tabela
    tela_listar_vendas.tableWidget.setColumnCount(6)#definir o nº de colunas da tabela

    for i in range(0,len(dados_lidos)):
        for j in range(0,6):
            tela_listar_vendas.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def abrir_tela_editar():
    tela_editar_vendas.show()

global data
data = datetime.datetime.now()
data_formatada = data.strftime("%d/%m/%Y")

def abrir_tela_vendas():
    tela_vendas.show()
    tela_vendas.lineEdit_5.setText(str(data_formatada))

    
    
def buscar_cliente():
     global numero_id
     linha = tela_listar_clientes.tableWidget.currentRow()

     cursor = banco.cursor()
     cursor.execute("SELECT id FROM cliente")
     dados_lidos = cursor.fetchall()
     valor_id = dados_lidos[linha][0]
     cursor.execute("SELECT * FROM cliente WHERE id=" + str (valor_id))
     cliente = cursor.fetchall()
     tela_vendas.show()
     tela_listar_clientes.close()

     tela_vendas.lineEdit_0.setText(str(cliente[0][0]))
     tela_vendas.lineEdit.setText(str(cliente[0][1]))
     
     numero_id = valor_id    

def buscar_plano():
     global numero_id
     linha = tela_listar_planos.tableWidget.currentRow()

     cursor = banco.cursor()
     cursor.execute("SELECT id FROM plano")
     dados_lidos = cursor.fetchall()
     valor_id = dados_lidos[linha][0]
     cursor.execute("SELECT * FROM plano WHERE id=" + str (valor_id))
     cliente = cursor.fetchall()
     tela_vendas.show()
     tela_listar_planos.close()

     tela_vendas.lineEdit_1.setText(str(cliente[0][0]))
     tela_vendas.lineEdit_2.setText(str(cliente[0][1]))
     
     numero_id = valor_id    

def buscar_modalidade():
     global numero_id
     linha = tela_listar_modalidades.tableWidget.currentRow()

     cursor = banco.cursor()
     cursor.execute("SELECT id FROM modalidades")
     dados_lidos = cursor.fetchall()
     valor_id = dados_lidos[linha][0]
     cursor.execute("SELECT * FROM modalidades WHERE id=" + str (valor_id))
     cliente = cursor.fetchall()
     tela_vendas.show()
     tela_listar_modalidades.close()

     tela_vendas.lineEdit_3.setText(str(cliente[0][0]))
     tela_vendas.lineEdit_4.setText(str(cliente[0][1]))
     
     numero_id = valor_id    

def salvar_vendas():###########################################
    campo1 = tela_vendas.lineEdit_0.text()
    campo2 = tela_vendas.lineEdit_1.text()
    campo3 = tela_vendas.lineEdit_3.text()    
    campo4 = tela_vendas.comboBox.currentText()
    campo5 = tela_vendas.lineEdit_5.text()

    print(campo1, campo2, campo3, campo4, campo5)
    cursor = banco.cursor()
    comando_sql = "INSERT INTO venda (id_cliente, id_planos, Id_modalidade, tipo_pgto, data) VALUES (%s,%s,%s,%s,%s)"
    dados = (str(campo1),str (campo2), str(campo3), str(campo4), str(campo5))
    cursor.execute(comando_sql, dados)
    banco.commit()
    QMessageBox.information(tela_vendas, "SUCESSO", "Venda finalizada com sucesso!")
    tela_vendas.lineEdit_0.setText("")
    tela_vendas.lineEdit.setText("")
    tela_vendas.lineEdit_1.setText("")
    tela_vendas.lineEdit_2.setText("")       
    tela_vendas.lineEdit_3.setText("")
    tela_vendas.lineEdit_4.setText("")
    tela_vendas.lineEdit_5.setText("")

    
def tela_vendas_voltar():
    tela_vendas.hide()
    tela_principal.show()

def tela_listar_vendas_voltar():
    tela_listar_vendas.hide()
    tela_vendas.show()

def tela_editar_vendas_voltar():
    tela_editar_vendas.hide()
    tela_listar_vendas.show()

def excluir_dados_vendas():
    linha = tela_listar_vendas.tableWidget.currentRow()
    tela_listar_vendas.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM venda")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos [linha][0]
    cursor.execute("DELETE FROM venda WHERE id =" + str(valor_id))
    banco.commit()

#******** FECHAR APP ******************
def sair ():
    tela_principal.close()

#************ TELA PRINCIPAL PUSHBUTTON ************
app=QtWidgets.QApplication([])
tela_login=uic.loadUi('tela_login.ui')
tela_principal=uic.loadUi('tela_principal.ui')
tela_cadastro=uic.loadUi('tela_cadastro.ui')
tela_cadastro_clientes=uic.loadUi('tela_cadastro_clientes.ui')
tela_listar_clientes=uic.loadUi('tela_listar_cliente.ui')
tela_modalidades=uic.loadUi('tela_modalidades.ui')
tela_listar_modalidades=uic.loadUi('tela_listar_modalidade.ui')
tela_planos=uic.loadUi('tela_planos.ui')
tela_matricula=uic.loadUi('tela_matricula.ui')
tela_vendas=uic.loadUi('tela_vendas.ui')
tela_editar_cliente = uic.loadUi('tela_editar_cliente.ui')
tela_editar_modalidade = uic.loadUi('tela_editar_modalidade.ui')
tela_listar_planos = uic.loadUi('tela_listar_planos.ui')
tela_editar_planos = uic.loadUi('tela_editar_planos.ui')
tela_listar_vendas = uic.loadUi('tela_listar_vendas.ui')
tela_editar_vendas = uic.loadUi('tela_editar_vendas.ui')
tela_listar_matriculas = uic.loadUi('tela_listar_matriculas.ui')
tela_editar_matricula = uic.loadUi('tela_editar_matricula.ui')



#*********** TELA PRINCIPAL PUSHBUTTON ******************
tela_principal.pushButton.clicked.connect(abrir_tela_matricula)
tela_principal.pushButton_2.clicked.connect(abrir_tela_vendas)
tela_principal.pushButton_3.clicked.connect(abrir_tela_planos)
tela_principal.pushButton_4.clicked.connect(abrir_tela_modalidades)
tela_principal.pushButton_5.clicked.connect(abrir_tela_cadastro_clientes)
tela_principal.pushButton_6.clicked.connect(sair)

#*********** TELA LOGIN E CADASTRO PUSHBUTTON ******************
tela_login.pushButton.clicked.connect(login_dados)
tela_login.pushButton_2.clicked.connect(abrir_cadastro)
tela_cadastro.pushButton.clicked.connect(cadastro_usuario)

#*********** TELA CLIENTE PUSHBUTTON ******************
tela_cadastro_clientes.pushButton.clicked.connect(salvar_cadastro_clientes)
tela_cadastro_clientes.pushButton_3.clicked.connect(abrir_listar_cliente) 
tela_listar_clientes.pushButton_3.clicked.connect(editar_cliente)
tela_cadastro_clientes.pushButton_2.clicked.connect(tela_cadastro_clientes_voltar)
tela_listar_clientes.pushButton_4.clicked.connect(tela_listar_clientes_voltar)
tela_listar_clientes.pushButton_5.clicked.connect(buscar_cliente)
tela_listar_clientes.pushButton_6.clicked.connect(buscar_clienteMatricula)
tela_editar_cliente.pushButton_3.clicked.connect(tela_editar_cliente_voltar)
tela_listar_clientes.pushButton_2.clicked.connect(excluir_dados_clientes)
tela_editar_cliente.pushButton_2.clicked.connect(salvar_editar_clientes)

#*********** TELA MODALIDADE PUSHBUTTON ******************
tela_modalidades.pushButton.clicked.connect(salvar_modalidades)
tela_modalidades.pushButton_2.clicked.connect(listar_modalidades)
tela_modalidades.pushButton_3.clicked.connect(tela_modalidades_voltar)
tela_listar_modalidades.pushButton_2.clicked.connect(editar_modalidade)
tela_listar_modalidades.pushButton_2.clicked.connect(tela_listar_modalidades_voltar)
tela_editar_modalidade.pushButton_3.clicked.connect(tela_editar_modalidades_voltar)
tela_listar_modalidades.pushButton_4.clicked.connect(editar_modalidades_voltar)
tela_listar_modalidades.pushButton_4.clicked.connect(editar_modalidades_voltar)
tela_listar_modalidades.pushButton_5.clicked.connect(buscar_modalidade)
tela_editar_modalidade.pushButton.clicked.connect(salvar_editar_modalidades)


#*********** TELA PLANOS PUSHBUTTON ******************
tela_planos.pushButton_2.clicked.connect(tela_planos_voltar)
tela_planos.pushButton.clicked.connect(salvar_planos)


tela_listar_planos.pushButton_2.clicked.connect(editar_plano)
tela_listar_planos.pushButton_4.clicked.connect(tela_listar_planos_voltar)
tela_editar_planos.pushButton_2.clicked.connect(tela_editar_planos_voltar)
tela_editar_planos.pushButton.clicked.connect(salvar_editar_planos)
tela_planos.pushButton_3.clicked.connect(listar_planos)
tela_listar_planos.pushButton_3.clicked.connect(excluir_dados_planos)
tela_listar_planos.pushButton_5.clicked.connect(buscar_plano)

#*********** TELA MATRÍCULA PUSHBUTTON ******************
tela_matricula.pushButton.clicked.connect(salvar_matricula)
tela_matricula.pushButton_2.clicked.connect(tela_matricula_voltar)
tela_matricula.pushButton_3.clicked.connect(abrir_tela_editar_matriculas)
tela_matricula.pushButton_4.clicked.connect(abrir_listar_cliente)
tela_matricula.pushButton_5.clicked.connect(listar_vendas)
tela_listar_matriculas.pushButton_2.clicked.connect(abrir_tela_editar_matricula)
tela_listar_matriculas.pushButton_4.clicked.connect(tela_listar_matriculas_voltar)
tela_editar_matricula.pushButton_2.clicked.connect(tela_editar_matricula_voltar)
tela_matricula.pushButton_3.clicked.connect(listar_matricula)
tela_listar_matriculas.pushButton_3.clicked.connect(excluir_dados_matricula)
#*********** TELA VENDAS PUSHBUTTON ******************
tela_vendas.pushButton.clicked.connect(salvar_vendas)
tela_vendas.pushButton_2.clicked.connect(tela_vendas_voltar)
tela_vendas.pushButton_3.clicked.connect(abrir_tela_editar_vendas)
tela_vendas.pushButton_5.clicked.connect(listar_planos)
tela_vendas.pushButton_6.clicked.connect(listar_modalidades)
tela_listar_vendas.pushButton_3.clicked.connect(abrir_tela_editar)
tela_listar_vendas.pushButton_2.clicked.connect(tela_listar_vendas_voltar)
tela_listar_vendas.pushButton_4.clicked.connect(buscar_vendaMatricula)
tela_editar_vendas.pushButton_3.clicked.connect(tela_editar_vendas_voltar)
tela_vendas.pushButton_3.clicked.connect(listar_vendas)
tela_listar_vendas.pushButton.clicked.connect(excluir_dados_vendas)

tela_vendas.pushButton_4.clicked.connect(abrir_listar_cliente)
#*********** TELA LISTAR MODALIDADE PUSHBUTTON ******************

tela_login.show()
app.exec()

