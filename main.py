import kivy
kivy.require ('1.0.1')
import sqlite3 
from kivy.core import window
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import  RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


# As classes vazias mas importantes para o projeto:

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    pass
class SelectableButton(RecycleDataViewBehavior, Button):
    pass

class menu(Screen):
    pass

#A classe da tela RecycleView onde vai receber os dados:

class rv(Screen):
    col1 = ListProperty()
    col2 = ListProperty()
    conexao = sqlite3.connect("org_livros.db")
    def pegar_livros(self):
        self.col1 = []
        self.col2 = []
        with self.conexao:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT id, titulo  FROM tb_livros ORDER BY id ASC")
            self.conexao.commit()
            rows = cursor.fetchall()
            for row in rows:
                print(row)
                self.col1.append(row[0])
                self.col2.append(row[1])

#A classe da tela com os campos para inserção de dados:

class create_sc(Screen):
    txt_id = ObjectProperty(None)
    txt_tit = ObjectProperty(None)
    txt_aut = ObjectProperty(None)
    txt_pag = ObjectProperty(None)
    txt_dat = ObjectProperty(None)
    txt_npg = ObjectProperty(None)
    lbl_resposta = ObjectProperty(None)


# A classe da tela de leitura de detalhes dos dados:


class read_sc(Screen):
    titulo = ObjectProperty(None)
    autor = ObjectProperty(None)
    patual = ObjectProperty(None)
    datal = ObjectProperty(None)
    tpags = ObjectProperty(None)
    cid = ObjectProperty(None)
    def atualizar_form(self, t1, t2, t3, t4, t5):
        self.ids.titulo.text = "Titulo: " + t1
        self.ids.autor.text = "Autor: " + t2
        self.ids.datal.text = "Data da Leitura: " + t3
        self.ids.patual.text = "Página atual: "+ t4
        self.ids.tpags.text = "Quant. de Páginas: " + t5


# A classe da tela de atualização dos dados com método e parâmetros:

class update_sc(Screen):
    upd_id = ObjectProperty(None)
    upd_tit = ObjectProperty(None)
    upd_aut = ObjectProperty(None)
    upd_dat = ObjectProperty(None)
    upd_pat = ObjectProperty(None)
    upd_tpg = ObjectProperty(None)
    lbl_resposta = ObjectProperty(None)
    def atualizar_form(self, t1, t2, t3, t4, t5):
        self.ids.upd_tit.text = t1
        self.ids.upd_aut.text = t2
        self.ids.upd_dat.text = t3
        self.ids.upd_pat.text = t4
        self.ids.upd_tpg.text = t5


# A classe da tela de exclusão de dados por determinado id:

class delete_sc(Screen):
    del_id = ObjectProperty(None)
    del_tit = ObjectProperty(None)
    del_aut = ObjectProperty(None)
    lbl_resposta = ObjectProperty(None)
    def atualizar_form(self, t1, t2):
        self.ids.del_tit.text = "Título: " + t1
        self.ids.del_aut.text = "Autor: " + t2


# Importação da interface gráfica e adição do ScreenManager:


Builder.load_string(open("gui.kv", encoding="utf-8").read(), rulesonly=True)

sm = ScreenManager(transition=WipeTransition())
sm.add_widget(rv(name='rv'))
sm.add_widget(menu(name='menu'))
sm.add_widget(create_sc(name='create'))
sm.add_widget(read_sc(name='read'))
sm.add_widget(update_sc(name='update'))
sm.add_widget(delete_sc(name='delete'))
sm.current = "menu"


# Estrutura das classes principal do projeto e sua execução:

class CrudKivy(App):
    
    # O Método criar_tabela() da classe CrudKivy()

    def criar_tabela(self):
        self.conexao = sqlite3.connect("org_livros.db")
        self.cursor =  self.conexao.cursor()
        sql = """ CREATE TABLE IF NOT EXISTS tb_livros( id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT (50) NOT NULL, autor TEXT (50), data_leitura DATE, pagina_atual INTEGER, n_paginas INTEGER)"""
        self.cursor.execute(sql) 


    # O Método selecionar_todos_livros() da classe CrudKivy()


    def selecionar_todos_livros(self):       
        rv = sm.get_screen('rv')       
        rv.pegar_livros()
        sm.current = 'rv'  


    # O Método inserir_livro() da classe CrudKivy()


    def inserir_livro(self, txt_tit, txt_aut, txt_dat, txt_pag, txt_npg):
        edt = sm.get_screen('create')
        try:
            if txt_tit != "" and txt_aut != "" and txt_dat != "" and txt_pag != "" and txt_npg != "":
                self.cursor.execute("""INSERT INTO tb_livros (titulo, autor, data_leitura, pagina_atual, n_paginas) VALUES (?,?,?,?,?)""", (txt_tit, txt_aut, txt_dat, txt_pag, txt_npg))
                self.conexao.commit()
                edt.lbl_resposta.text = "Livro Cadastrado com Sucesso!"
                print("Dados Inseridos com Sucesso!")
            else:
                edt.lbl_resposta.text = "Todos campos devem ser preenchidos."
                print("Todos campos devem ser preenchidos")
        except sqlite3.Error as error:
            edt.lbl_resposta.text = "Algum erro ocorreu"
            print("Algum erro ocorreu", error)
            self.conexao.rollback()
    

    # O Método selecionar_livro() da classe CrudKivy()


    def selecionar_livro(self, cid, sc):
        try:
            self.cursor.execute("SELECT * FROM tb_livros WHERE id = ?", (cid))
            self.conexao.commit()
            records = self.cursor.fetchall()
            slc = sm.get_screen('read')
            upd = sm.get_screen('update')
            dlt = sm.get_screen('delete')
            for row in records:
                if sc == 'selecionar':
                    slc.atualizar_form(str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]))
                elif sc == 'atualizar':
                    upd.atualizar_form(str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]))
                elif sc == 'excluir':
                    dlt.atualizar_form(str(row[1]), str(row[2]))
        except sqlite3.Error as error:
            print("Algum erro ocorreu.", error)
    

    # O Método atualizar_livro() da classe CrudKivy()


    def atualizar_livro(self, upd_id, upd_tit, upd_aut, upd_dat, upd_pat, upd_tpg):
        upd = sm.get_screen('update')
        try:
            if upd_tit != "" and upd_aut != "" and upd_dat != "" and upd_pat != "" and upd_tpg != "":
                self.cursor.execute("UPDATE tb_livros SET (titulo, autor, data_leitura, pagina_atual, n_paginas) = (?,?,?,?,?) WHERE id = ?", (upd_tit, upd_aut, upd_dat, upd_pat, upd_tpg, upd_id,))
                self.conexao.commit()
                upd.lbl_resposta = "Livro Atualizado com Sucesso!"
                print("Dados atualizados com Sucesso!")
            else:
                upd.lbl_resposta.text = "Todos campos devem ser preenchidos"
        except sqlite3.Error as error:
            print("Algum erro ocorreu.", error)

    
    # O Método deletar_livro() da classe CrudKivy()
    
    def deletar_livro(self, id):
        if id != "":
            sql = 'DELETE FROM tb_livros WHERE id = ?'
            self.cursor.execute(sql, (id,))
            self.conexao.commit()
            dlt = sm.get_screen('delete')
            dlt.lbl_resposta.text = 'Livro Excluído com Sucesso!'
            print('Dados Excluído com Sucesso!')
            

    # O Método construtor() da classe CrudKivy()

    
    def build(self):
        App.title = "Organizador de leituras"
        window.size = (320, 480)
        self.criar_tabela()
        return sm

CrudKivy().run()


#`id` int NOT NULL AUTO_INCREMENT,
