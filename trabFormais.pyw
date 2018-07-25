import tkinter as tk
from tkinter import ttk, Menu, scrolledtext
from tkinter import messagebox as msg
from tkinter.filedialog import askopenfilename, asksaveasfilename
from time import sleep
from threading import Thread
import copy
import itertools

# Estrutura da árvore
# contém informação do nodo, nodos a sua direita e esquerda, o seu pai, e tamanho (apenas para resolver um bug do programa)
class Tree():
    def __init__(self, info, left=None, right=None, up=None, size=1):
        self.info = info
        self.left = left
        self.right = right
        self.up = up
        self.size = size

# Adiciona o nodo à esquerda
    def new_left(self, new):
        self.left = new
        add_size(self)
        new.up = self

# Adiciona o nodo à direita
    def new_right(self, new):
        self.right = new
        add_size(self)
        new.up = self

# Classe do aplicativo -> Janela do programa
class APP():
    dict_gramatica = {}
    dict_regras = {}
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry("805x600")  # tamanho pré-definido e não alterável
        self.win.resizable(False, False)


        #define nome da Janela
        self.win.title("Trabalho Final - LinguagensFormais")
        self.create_widgets()
        self.win.iconbitmap('icon8.ico') # icone da janela

    # abaixo temos algumas mensagens de Erro ou Aviso na tela do programa
    def Info_Trab(self):
        msg.showinfo('Grupo', 'Guilherme Bazzo\nNicolas Duranti\nThiago Oliveira')

    def Erro_Leitura_Arquivo(self):
        msg.showwarning('Erro', 'Erro na leitura do arquivo!')

    def Erro_semGramatica(self):
        msg.showwarning('Erro', 'Por favor, insira uma gramatica.')

    def Erro_Gramatica_Virou_Vazia(self):
        msg.showwarning('Erro', 'Atenção!\nGramática ficou vazia durante o processo')

    def save_sucesso(self):
        msg.showinfo('Info', 'Arquivo salvo!')

    def save_erro(self):
        msg.showwarning('Erro', 'Erro ao salvar arquivo')

    # sai do programa / fecha janela
    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    # Cria todos os widgets que aparecem na tela, como botões, labels ...
    def create_widgets(self):
        #label de inicio - pede arquivo
        self.a_label = ttk.Label(self.win, text="Digite o nome do arquivo:")
        self.a_label.grid(column=0, row=0)

        # label - pede palavra
        self.label_palavra = ttk.Label(self.win, text="Digite a palavra para ser verificada:")
        self.label_palavra.grid(column=0, row=12)

        # label - verificacao da palavra
        self.label_verificacao = ttk.Label(self.win, text="")
        self.label_verificacao.grid(column=0, row=14)

        # botão - manda fazer leitura do arquivo digitado
        self.button_leitura = ttk.Button(self.win, text="Ler", command=self.le_e_formata)
        self.button_leitura.grid(column=1,row=1)
        # self.button_leitura.configure(state='disabled')

        # botão - manda fazer a simplificação
        self.button_simplifica = ttk.Button(self.win, text="Simplifica/FNC", command=lambda : self.simplificacao_inicial_gramatica(self.dict_gramatica, self.dict_regras))
        self.button_simplifica.grid(column=1,row=10)

        # botão verificar palavra
        self.button_verifica = ttk.Button(self.win, text="Verificar", command=lambda : self.Verifica_CYK(self.dict_gramatica, self.dict_regras, self.palavra.get()))
        self.button_verifica.grid(column = 1, row = 13)
        self.button_verifica.configure(state='disabled')

        # botão salva tela em txt
        self.salva_txt = ttk.Button(self.win, text="Save", command=lambda: self.save_in_file())
        self.salva_txt.grid(column=1, row=16)
        self.salva_txt.configure(state='disabled')

        # janela para escrita do nome do arquivo
        self.name = tk.StringVar()
        # win.update()
        # int(win.winfo_width()/7)
        self.name_entered = ttk.Entry(self.win, width=118, textvariable=self.name)
        self.name_entered.grid(column=0, row=1)
        self.name_entered.focus() #inicia cursor nessa janela

        # janela para escrita da palavra
        self.palavra = tk.StringVar()
        self.palavra_entered = ttk.Entry(self.win, width=118, textvariable=self.palavra)
        self.palavra_entered.grid(column=0, row=13)

        # aba de output
        self.scr = scrolledtext.ScrolledText(self.win, width=97, height = 20, wrap=tk.WORD)
        self.scr.grid(column = 0, row=5, sticky='WE', columnspan = 10)
        # self.scr.configure(state='disabled')

        # cria barra de menu
        self.menu_bar = Menu(self.win)
        self.win.config(menu = self.menu_bar)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command = self. open_file_menu)

        # cria 'About'
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command = self.Info_Trab)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Quit", command = self._quit)

    # Não está sendo usado na versão final do trabalho, mas no inicio era usado para testes (essa função e as três abaixo)
    def create_thread(self):
        self.run_thread = Thread(target=self.method_in_a_thread)
        self.run_thread.start() # start the thread
        print(self.run_thread)

    def create_thread(self):
        self.run_thread = Thread(target=self.method_in_a_thread)
        self.run_thread.start() # start the thread
        # Button callback

    def click_me(self):
        self.button_leitura.configure(text='Hello ' + self.name.get())
        self.create_thread()

    def method_in_a_thread(self):
        print('Hi, how are you?')
        for idx in range(10):
            sleep(5)
            self.scr.insert(tk.INSERT, str(idx) + 'n')

    # Abre janela do Diretório para usuário procurar arquivo para ser aberto
    def open_dir_file(self):
        name = askopenfilename(initialdir="/", # "C:/Users",
                               filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                               title="Choose a file."
                               )
        name = name[::-1]
        name = name[:name.find('/')]
        name = name[::-1]
        self.name.set(name)
        return name

    # Abre janela do Diretório para usuário procurar arquivo para ser salvo ou poder criar novo, dando o nome desejado
    def save_dir_file(self):
        name = asksaveasfilename(initialdir="/",
                               filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                               title="Choose a file."
                               )
        return name

    def open_file_menu(self):
        self.name.set("")
        self.le_e_formata()

    # lê arquivo e formata para imprimir na tela formalmente
    def le_e_formata(self):
        # quando lê arquivo, como não está simplificado ainda, proibe a verificação da palavra
        self.button_verifica.configure(state='disabled')
        self.palavra.set("")
        self.label_verificacao.configure(text="")
        quebra_linha = '\n'
        self.dict_gramatica = {}
        self.dict_regras = {}
        flag_atual = 0

        nome_arq = self.name.get()
        if len(nome_arq) == 0:
            nome_arq = self.open_dir_file()
        if '.txt' not in nome_arq:
            nome_arq += '.txt'

        self.scr.configure(state='normal')
        self.clear_scrolled_screen()

        try:
            with open(nome_arq, "r") as arq_in:
                for line in arq_in:
                    if line[0] == '#':
                        if '#Terminais' in line:
                            flag_atual = 'Terminal'
                        elif '#Variaveis' in line:
                            flag_atual = 'Variavel'
                        elif '#Inicial' in line:
                            flag_atual = "Inicial"
                        else:
                            flag_atual = "Regras"
                    else:
                        if flag_atual is not "Regras":
                            self.dict_gramatica.setdefault(flag_atual, [])
                            aux = line[line.find("[")+2:line.find(" ]")]
                            if aux == '':
                                aux = ']'
                            self.dict_gramatica[flag_atual].append(aux)
                        else:
                            estado = (line[line.find("[")+2:line.find(" ]")])
                            produc = []
                            self.dict_regras.setdefault(estado, [])
                            if '#' not in line:
                                produc = self.transicao_regra(line[line.find(">") + 1:])
                                # self.dict_regras[estado].append(self.transicao_regra(line[line.find(">")+1:]))
                            else:
                                produc = self.transicao_regra(line[line.find(">")+1:line.find("#")])
                                # self.dict_regras[estado].append(self.transicao_regra(line[line.find(">")+1:line.find("#")]))
                            if produc not in self.dict_regras[estado]:
                                self.dict_regras[estado].append(produc)


            self.Imprime_Gramatica(self.dict_gramatica, self.dict_regras)

            self.salva_txt.configure(state='normal')
        except:
            self.Erro_Leitura_Arquivo()
            self.salva_txt.configure(state='disabled')

        self.scr.configure(state='disabled')

    # lê do arquivo as produções
    def transicao_regra(self, linha):
        saida_linha = []
        while(len(linha)!=0):
            linha = linha.replace(" ", "")
            linha = linha.replace("\t", "")
            linha = linha.replace("\n", "")
            l_superior = linha.find("]")
            terminal = linha[linha.find("[") + 1:linha.find("]")]
            if terminal == '':
                terminal = ']'
                linha = linha[l_superior +2:]
            else:
                linha = linha[l_superior+1:]
            saida_linha.append(terminal)

        return saida_linha

    # limpa tela do programa
    def clear_scrolled_screen(self):
        self.scr.delete('1.0', tk.END)

    # imprime na tela a gramática
    def Imprime_Gramatica(self, gramatica, regras):
        #for key in gramatica:
        #self.scr.configure(state='normal')
        self.scr.insert(tk.INSERT, (self.formata_string(gramatica)))

        self.scr.insert(tk.INSERT, "P = {\n")

        for key in regras:
            self.scr.insert(tk.INSERT, (self.formata_string_regras(key, regras[key])))

        self.scr.insert(tk.INSERT, "}")
        #self.scr.configure(state='disabled')

    def formata_string(self, gramatica):
        return "G = ({" + ",".join(gramatica['Variavel']) + "}, {" + ",".join(gramatica['Terminal']) + "}, P, " + ",".join(gramatica['Inicial']) + ")\n"
        #return key + ": " + ",".join(l) + '\n'

    def formata_string_regras(self, key, l):
        s_list_out = ""
        for i in l:
            s_list_out += "".join(i)
            s_list_out += "|"

        s_list_out = s_list_out[:len(s_list_out)-1]

        return ' ' + key + "->" + s_list_out + '\n'

    # faz preparação para a simplificação
    def simplificacao_inicial_gramatica(self, gramatica, regras):
        if len(gramatica) == 0 and len(regras) == 0:
            self.Erro_semGramatica()
        else:
            gramatica, regras = self.simplifica_gramatica(gramatica, regras)
            self.dict_gramatica, self.dict_regras = self.FN_Chomsky(gramatica, regras)

            # Libera botão para verificar palavra
            self.button_verifica.configure(state='enabled')

    def simplifica_gramatica(self, gramatica, regras):
        # if len(self.dict_gramatica) == 0 and len(self.dict_regras) == 0:
        #     self.Erro_semGramatica()
        # else:
        self.scr.configure(state='normal')

        gramatica, regras = simplifica_GLC(gramatica, regras)

        self.scr.insert(tk.INSERT, ("\n\n*Simplificação:\n"))
        self.Imprime_Gramatica(gramatica, regras)

        self.scr.configure(state='disabled')

        return gramatica, regras

    # Forma Normal de Chomsky
    def FN_Chomsky(self, gramatica, regras):

        self.scr.configure(state='normal')

        gramatica, regras = Forma_Normal_Chomsky(gramatica, regras)

        self.scr.insert(tk.INSERT, ("\n\n*Forma Normal de Chomsky:\n"))
        self.Imprime_Gramatica(gramatica, regras)

        self.scr.configure(state='disabled')

        return gramatica, regras

    # Algorítmo CYK
    def Verifica_CYK(self, gramatica, regras, palavra):
        flag_tree = False
        self.scr.configure(state='normal')
        self.label_verificacao.configure(text="")
        if len(palavra) != 0:
            if separa_palavras_terminais(gramatica['Terminal']):
                verifica_palavra = palavra.split()
            else:
                verifica_palavra = palavra
            matriz = CYK(gramatica, regras, verifica_palavra)
                
            if gramatica['Inicial'][0] in matriz[0][0]:
                s = "\n\n" + palavra + " -> PALAVRA ACEITA"
                self.scr.insert(tk.INSERT, s)

                self.label_verificacao.configure(text = palavra + " -> PALAVRA ACEITA")
                self.label_verificacao.configure(foreground = 'green')

                l_tree = Cria_Arvores_Derivacao(matriz, regras, gramatica, verifica_palavra)
                flag_tree = True
            else:
                s = "\n\n" +palavra + " -> PALAVRA NÂO ACEITA"
                self.scr.insert(tk.INSERT, s)

                self.label_verificacao.configure(text = palavra +  " -> PALAVRA NÃO ACEITA")
                self.label_verificacao.configure(foreground = 'red')

            self.imprime_matriz_tela(matriz, palavra)
            if flag_tree:
                self.scr.insert(tk.INSERT, "\n\nÁrvores:")
                for tree in l_tree:
                    self.scr.insert(tk.INSERT, "\n\n")
                    self.print_tree(tree)

        self.scr.configure(state='disabled')

    # imprime matriz na janela do programa
    def imprime_matriz_tela(self, matriz, palavra):
        self.scr.insert(tk.INSERT, "\nMatriz:\nPALAVRA-> ")
        self.scr.insert(tk.INSERT, palavra + '\n')
        for i in range(len(matriz)):
            string_matriz = ""
            for conj in matriz[i][:i+1]:
                string_matriz += '{'
                string_matriz += ",".join(conj)
                string_matriz += '}\t'
            # print(string_matriz)
            self.scr.insert(tk.INSERT, string_matriz)
            self.scr.insert(tk.INSERT, "\n")

    # imprime arvore na tela
    def print_tree(self, arv, mark='  '):
        if arv != None:
            self.scr.insert(tk.INSERT, mark + arv.info + "\n")
            # print(mark + arv.info)
            mark = mark.replace('╚══', '   ')
            mark = mark.replace('╠══', '║  ')
            if arv.right != None:
                self.print_tree(arv.left, mark + '╠══')
                self.print_tree(arv.right, mark + '╚══')
            else:
                self.print_tree(arv.left, mark + '╚══')

    # salva conteúdo da janela em um TXT
    def save_in_file(self):
        self.scr.configure(state='normal')
        s = self.scr.get('1.0', tk.END)
        self.scr.configure(state='disabled')
        nome_arq = self.save_dir_file()
        if len(nome_arq)!=0:
            if ".txt" not in nome_arq:
                nome_arq += ".txt"

            s = s.replace('═', '-')
            s = s.replace('╚', '|')
            s = s.replace('╠', '|')
            s = s.replace('║', '|')

            try:
                file_out = open(nome_arq, "w")
                file_out.write(s)
                file_out.close()
                self.save_sucesso()
            except:
                self.save_erro()
        else:
            self.save_erro()



# Verifica se a a verificação deve ser feita letra a letra ou por palavras
def separa_palavras_terminais(terminais):
    for term in terminais:
        if len(term) > 1:
            return True

#SIMPLIFICAÇÃO DE GLC:
def simplifica_GLC(gramatica, regras):

    vazio = 'V'
    lista_vazios = []
    # simplificação normal - inicial
    conjunto_vazios(gramatica, regras, lista_vazios, vazio)
    app.scr.insert(tk.INSERT, "\n\n1-Conjuntos Vazios:\n")
    app.Imprime_Gramatica(gramatica, regras)

    regras = exclui_vazias(gramatica, regras, lista_vazios, vazio)
    app.scr.insert(tk.INSERT, "\n\n1-Exclui Vazios \ Adiciona Vazio:\n")
    app.Imprime_Gramatica(gramatica, regras)

    regras = fecho_variaveis(gramatica, regras, vazio)
    app.scr.insert(tk.INSERT, "\n\n2-Fecho Variaveis:\n")
    app.Imprime_Gramatica(gramatica, regras)

    gramatica = remove_inuteis(gramatica, regras, vazio)
    app.scr.insert(tk.INSERT, "\n\n3-Remove Inúteis:\n")
    app.Imprime_Gramatica(gramatica, regras)

    remove_inatingivel(gramatica, regras)
    app.scr.insert(tk.INSERT, "\n\n3-Remove Inatingíveis:\n")
    app.Imprime_Gramatica(gramatica, regras)

    # print(gramatica, '\n', regras)
    return gramatica, regras

def remove_inuteis(gramatica, regras, vazio):
    #remove transições que não gerem simbolos terminais
    tamanho_anterior = 0
    lista_var_terminais = []
    while (True):
        for var in regras:
            if var not in lista_var_terminais:
                for transicao in regras[var]:
                    flag_variavel = False
                    for simbolo in transicao:
                        if (simbolo in gramatica['Variavel']) and (simbolo not in lista_var_terminais) and (simbolo != vazio):
                            flag_variavel = True
                        # if (simbolo not in gramatica['Terminal']) and (simbolo not in gramatica['Variavel']):
                        #     flag_variavel=True
                    if not flag_variavel and var not in lista_var_terminais:
                        lista_var_terminais.append(var)

        if len(lista_var_terminais) == tamanho_anterior:
            break

        tamanho_anterior = len(lista_var_terminais)

    # if len(lista_var_terminais) == 0:
    #     app.Erro_Gramatica_Virou_Vazia()

    gramatica['Variavel'] = lista_var_terminais
    lista_var_fora = [x for x in regras if x not in lista_var_terminais]

    #remove possiveis variaveis que estão nas regras porém não foram listadas no conjunto das variaveis
    for var in regras: #pega simbolo_var
        for transicao in regras[var]: #cada variavel contém uma lista de listas(que são as transações), aqui pegamos cada uma dessas listas
            if transicao != list(vazio):
                for simbolo in transicao:
                    if (simbolo not in gramatica['Terminal']) and (simbolo not in gramatica['Variavel']):
                        regras[var].remove(transicao)
                        break
    # print(regras)

    while(len(lista_var_fora)!=0):
        var_out = lista_var_fora.pop()
        regras.pop(var_out, None)

    list_trans_vazio = [x for x in regras if len(regras[x])==0]

    while(len(list_trans_vazio)!=0):
        var_vazio = list_trans_vazio.pop(0)
        if var_vazio in regras:
            regras.pop(var_vazio)
        if var_vazio in gramatica['Variavel']:
            gramatica['Variavel'].remove(var_vazio)

        for var in regras:
            for transicao in regras[var]:
                if var_vazio in transicao:
                    regras[var].remove(transicao)
            if len(regras[var]) == 0:
                list_trans_vazio.append(var)


    return gramatica

#remove variaveis que não são atingíveis a partir da inicial. Assim como os terminais
def remove_inatingivel(gramatica, regras):
    lista_atingiveis_var = []
    lista_atingiveis_ter = []
    lista_atingiveis_var.append(gramatica['Inicial'][0])
    controle = 0
    #cria lista contendo as variaveis que alcançamos a partir da variavel inicial
    if len(regras) != 0:
        while(True):
            for transicao in regras[lista_atingiveis_var[controle]]:
                for simbolo in transicao:
                    if simbolo in gramatica['Variavel']:
                        if simbolo not in lista_atingiveis_var and simbolo in gramatica['Variavel']:
                            lista_atingiveis_var.append(simbolo)
                    else:
                        if simbolo not in lista_atingiveis_ter and simbolo in gramatica['Terminal']:
                            lista_atingiveis_ter.append(simbolo)

            controle += 1

            #criterio de parada
            if controle >= len(lista_atingiveis_var):
                break

    #Remove regras inatingíveis / variaveis
    lista_nao_atingiveis_var = []
    for i in gramatica['Variavel']:
        if i not in lista_atingiveis_var:
            lista_nao_atingiveis_var.append(i)

    # print(lista_nao_atingiveis_var)

    if len(lista_nao_atingiveis_var) != 0:
        for var in lista_nao_atingiveis_var:
            regras.pop(var, None)
            gramatica['Variavel'].remove(var)


    lista_nao_atingiveis_ter = []
    for i in gramatica['Terminal']:
        if i not in lista_atingiveis_ter:
            lista_nao_atingiveis_ter.append(i)

    for ter in lista_nao_atingiveis_ter:
        gramatica['Terminal'].remove(ter)

def conjunto_vazios(gramatica, regras, lista_vazios, vazio):
    tamanho_anterior = 0

    for var in regras:
        for transicao in regras[var]:
            if len(transicao) == 1:
                if transicao[0] == vazio:
                       lista_vazios.append(var)


    while (True):
        for var in regras:
            if var not in lista_vazios:
                for transicao in regras[var]:
                    flag_vazio = False
                    for simbolo in transicao:
                        if ((simbolo in gramatica['Variavel']) and (simbolo not in lista_vazios)): # or (simbolo in gramatica['Terminal']):
                            flag_vazio = True
                        elif simbolo not in gramatica['Variavel']:
                            flag_vazio = True
                    if not flag_vazio and var not in lista_vazios:
                        lista_vazios.append(var)

        if len(lista_vazios) == tamanho_anterior:
            break

        tamanho_anterior = len(lista_vazios)

def exclui_vazias(gramatica, regras, lista_vazios, vazio):
    regras_novo = {}
    nova_transicao = []
    # P_1 = {A -> a | a == vazio e a not in lista_vazios}
    for var in regras:
        for transicao in regras[var]:
            flag_vazio = False
            if len(transicao) == 1:
                    if transicao[0] == vazio: # or transicao[0] in lista_vazios:
                        flag_vazio = True
            if not flag_vazio:
                regras_novo.setdefault(var, [])
                regras_novo[var].append(transicao)

    for var in regras_novo:
        nova_transicao = []
        for transicao in regras_novo[var]:
            lista_indices = []
            for i in range(len(transicao)):
                if transicao[i] in lista_vazios:
                    lista_indices.append(i)
            nova_transicao += gera_transicoes_indices_vazio(transicao,lista_indices)

        for new_trans in nova_transicao:
            if new_trans not in regras_novo[var]:
                regras_novo[var].append(new_trans)

    if len(lista_vazios) != 0 and gramatica['Inicial'][0] in lista_vazios:
        # print(lista_vazios)
        regras_novo[gramatica['Inicial'][0]].append(list(vazio))

    return regras_novo

def gera_transicoes_indices_vazio(transicao, lista_indices):
    novas_transicoes = []
    list_pair_combinacao_indices = []
    # gera as possiveis combinacoes entre os indices que devem ser removidos
    for i in range(len(lista_indices)):
        list_pair_combinacao_indices += list(itertools.combinations(lista_indices, i+1))

    # arruma para criar uma lista de listas com os indices
    lista_comb_indices_final = []
    for i in list_pair_combinacao_indices:
        lista_comb_indices_final.append(i)

    # cria as novas transicoes com os indices criados acima
    for indices in lista_comb_indices_final:
        aux_transicao = copy.deepcopy(transicao)
        for ind in indices[::-1]:
            del aux_transicao[ind]
        if aux_transicao not in novas_transicoes and len(aux_transicao) != 0:
            novas_transicoes.append(aux_transicao)


    return novas_transicoes

def fecho_variaveis(gramatica, regras, vazio):
    fecho = {}
    regras_novo = {}
    #cria dicionario dos fechos para cada variavel
    for var in regras:
        fecho.setdefault(var, [])
        for transicao in regras[var]:
            if len(transicao) == 1:
                if transicao[0] in gramatica['Variavel']:
                    fecho[var].append(transicao[0])
                    for key in fecho:
                        if var in fecho[key]:
                            fecho[key].append(transicao[0])

    for var in regras:
        regras_novo.setdefault(var, [])
        for transicao in regras[var]:
            if len(transicao) == 1:
                if transicao[0] not in gramatica['Variavel']:
                    regras_novo[var].append(transicao)
            else:
                regras_novo[var].append(transicao)

    for var in gramatica['Variavel']:
        if var in fecho:
            for producao in fecho[var]:
                if producao in regras:
                    for transicao in regras[producao]:
                        if transicao not in regras_novo[var]:
                            if len(transicao) != 1:
                                regras_novo[var].append(transicao)
                            elif transicao[0] not in gramatica['Variavel']  and transicao[0] != vazio:
                                regras_novo[var].append(transicao)



    return regras_novo

def elimina_vazia(gramatica, regras):  # eliminação da produção do símbolo vazio pela variável inicial, caso ela exista
    if len(regras) > 0:
        if ['V'] in regras[gramatica['Inicial'][0]]:
            regras[gramatica['Inicial'][0]].remove(['V'])
    return regras

def Forma_Normal_Chomsky(gramatica, regras):
    regras = elimina_vazia(gramatica, regras)

    conj_terminais = extracao_terminais(gramatica, regras)

    etapa2_fnc(conj_terminais, gramatica, regras)
    # regras = substitui_term_maior2(gramatica, regras)
    app.scr.insert(tk.INSERT, ("\n\n1-Substitui Terminais:\n"))
    app.Imprime_Gramatica(gramatica, regras)

    etapa3_fnc(gramatica, regras)
    # regras = prod_maior3(gramatica, regras)
    app.scr.insert(tk.INSERT, ("\n\n2-Substitui Produção Maior que 2:\n"))
    app.Imprime_Gramatica(gramatica, regras)

    return gramatica, regras

def substitui_term_maior2(gramatica, regras):
    regras_novo = {}

    for var in regras:
        for transicao in regras[var]:
            if len(transicao) != 1:
                for simbolo in transicao:
                    if simbolo in gramatica['Terminal']:
                        novo_var = 'C_{}'.format(simbolo)
                        regras_novo.setdefault(novo_var, [])
                        if [simbolo] not in regras_novo[novo_var]:
                            regras_novo[novo_var].append([simbolo])
                        if novo_var not in gramatica['Variavel']:
                            gramatica['Variavel'].append(novo_var)
                        for i in range(len(transicao)):
                            if transicao[i] == simbolo:
                                transicao[i] = novo_var

    if len(regras) != 0:
        if ['V'] in regras[gramatica['Inicial'][0]]:
            regras[gramatica['Inicial'][0]].remove(['V'])


    # print(regras_novo)
    return {**regras, **regras_novo}

def prod_maior3(gramatica, regras):
    regras_novo = copy.deepcopy(regras)
    contador_novas_transicoes = 1
    for var in regras:
        for transicao in regras[var]:
            if len(transicao) > 2:
                transicao_atual = transicao
                variavel_atual = var
                while(True):

                    regras_novo[variavel_atual].remove(transicao_atual)

                    flag_novo_Dx = True
                    for i in range(1, contador_novas_transicoes):
                        procura_transicao = 'D_{}'.format(i)
                        if regras_novo[procura_transicao] == [transicao_atual[1:]]:
                            # print(procura_transicao)
                            transicao_nova = [transicao_atual[0]]
                            transicao_nova.append(procura_transicao)
                            regras_novo[variavel_atual].append(transicao_nova)
                            # contador_novas_transicoes -= 1
                            flag_novo_Dx = False
                            nova_transicao = procura_transicao
                            break

                    if flag_novo_Dx:
                        nova_transicao = 'D_{}'.format(contador_novas_transicoes)
                        contador_novas_transicoes += 1
                        
                        if nova_transicao not in gramatica['Variavel']:
                            gramatica['Variavel'].append(nova_transicao)

                        transicao_nova = [transicao_atual[0]]
                        transicao_nova.append(nova_transicao)
                        regras_novo[variavel_atual].append(transicao_nova)

                        regras_novo.setdefault(nova_transicao, [])
                        regras_novo[nova_transicao].append(transicao_atual[1:])


                    if not len(transicao_atual[1:]) > 2:
                        break
                    else:
                        transicao_atual = transicao_atual[1:]
                        variavel_atual = nova_transicao

    return regras_novo


# T
# coleta terminais de producoes de tamanho > 1 com terminais
def extracao_terminais(gramatica, dictt):
    conjunto_term = []
    for key in dictt:
        for transicao in dictt[key]:
            if len(transicao) > 1:
                for char in transicao:
                    if char in gramatica['Terminal'] and char not in conjunto_term:
                        conjunto_term.append(char)
    return conjunto_term

def etapa2_fnc(conjunto_term, gramatica, dictt):
    while len(conjunto_term) != 0:
        nova_var = "C"
        nova_var = nova_var + "_" + conjunto_term[0] #ajusta o nome da variável de acordo com o terminal ao qual se refere
        gramatica['Variavel'].append(nova_var)
        for key in dictt:
            for transicao in dictt[key]:
                if len(transicao) != 1: #se o tamanho da produção é maior do que 1, procura o terminal a ser substituído
                    for i in range(len(transicao)): #e coloca a nova variável no lugar
                        if transicao[i] == conjunto_term[0]:
                            transicao[i] = nova_var
        dictt[nova_var] = []            #coloca no dicionário a nova regra de produção
        dictt[nova_var].append([conjunto_term[0]])
        del conjunto_term[0]
    return dictt

def etapa3_fnc(gramatica, dictt):
    list_aux_nv = [] #novas variaveis
    list_aux_np = [] #novas producoes
    i = str(0)
    for key in dictt:
        for transicao in dictt[key]:
            while len(transicao) > 2: #substitui duas variaveis por uma só nas produções já existentes
                nova_var = "D_"
                i = str(int(i) + 1)
                nova_var = nova_var + i #ajusta o nome da nova variável D para ter numerações diferentes(D1,D2,D3...)
                gramatica['Variavel'].append(nova_var)
                list_aux_nv.append(nova_var)
                list_aux_np.append(transicao[0])
                list_aux_np.append(transicao[1])
                transicao.remove(transicao[0])
                transicao.remove(transicao[0])
                transicao.insert(0, nova_var)

    list_aux = []
    while len(list_aux_np) != 0 and len(list_aux_nv) != 0: #coloca as novas producoes no dicionario da gramatica
        list_aux.append(list_aux_np[0])
        list_aux.append(list_aux_np[1])
        dictt[list_aux_nv[0]] = [list_aux]
        list_aux_nv.remove(list_aux_nv[0])
        list_aux_np.remove(list_aux_np[0])
        list_aux_np.remove(list_aux_np[0])
        list_aux = []
# T


def CYK(gramatica, regras, palavra):
    tam_palavra = len(palavra)
    matriz_derivacao = [[[] for x in range(tam_palavra)] for y in range(tam_palavra)]
    # etapa 1
    for i in range(tam_palavra):
        for var in regras:
            for transicao in regras[var]:
                if len(transicao) == 1:
                    if transicao[0] == palavra[i] and var not in matriz_derivacao[tam_palavra-1][i]:
                        matriz_derivacao[len(palavra)-1][i].append(var)

    # etapa 2
    for s in range(tam_palavra - 2, -1, -1):
        for r in range(s+1):
            aux_diagonal = 0
            for k in range(tam_palavra-1, s, -1):
                aux_diagonal += 1
                producao_BC = []
                for B in matriz_derivacao[k][r]:
                    for C in matriz_derivacao[s+aux_diagonal][r+aux_diagonal]:
                        if [B, C] not in producao_BC:
                            producao_BC.append([B, C])
                for var in regras:
                    for transicao in regras[var]:
                        if transicao in producao_BC and var not in matriz_derivacao[s][r]:
                            matriz_derivacao[s][r].append(var)


    # print(palavra)
    # # print(matriz_derivacao)
    # imprime_matriz(matriz_derivacao)
    return matriz_derivacao


def Cria_Arvores_Derivacao(matriz, regras, gramatica, palavra):
    dict_arvores = {}
    T = Tree(gramatica['Inicial'][0])
    # dict_arvores['T_0'] = T
    Tree_Rec(T, matriz, regras, len(palavra), (0,0), dict_arvores)

    if len(dict_arvores) == 0:
        dict_arvores['T_0'] = T

    for i in dict_arvores:
        dict_arvores[i] = go_up_tree(dict_arvores[i])

    max_tam = [dict_arvores[i].size for i in dict_arvores]
    max_tam = max(max_tam)
    list_tree = [dict_arvores[i] for i in dict_arvores if dict_arvores[i].size == max_tam]

    for tree in list_tree:
        adiciona_terminais_Tree(tree, palavra)

    return list_tree

def Tree_Rec(T, matriz, regras, tam_palavra, pos=(0,0), dict_arvores={}):
    prod, pos1, pos2 = Encontra_Producao(matriz, T.info, pos, regras, tam_palavra)
    if len(prod) == 1:
        T.new_left(Tree(prod[0][0]))
        T.new_right(Tree(prod[0][1]))

        if pos1[0][0] != tam_palavra - 1:
            Tree_Rec(T.left, matriz, regras, tam_palavra, pos1[0], dict_arvores)
        if pos2[0][0] != tam_palavra - 1:
            Tree_Rec(T.right, matriz, regras, tam_palavra, pos2[0], dict_arvores)
    else:
        for i in range(len(prod)):
            n_T = 'T_{}'.format(len(dict_arvores))
            dict_arvores[n_T] = copy.deepcopy(T)
            # dict_arvores[n_T] = T

            dict_arvores[n_T].new_left(Tree(prod[i][0]))
            dict_arvores[n_T].new_right(Tree(prod[i][1]))

            if pos1[i][0] != tam_palavra-1:
                Tree_Rec(dict_arvores[n_T].left, matriz, regras, tam_palavra, pos1[i], dict_arvores)
            if pos2[i][0] != tam_palavra-1:
                Tree_Rec(dict_arvores[n_T].right, matriz, regras, tam_palavra, pos2[i], dict_arvores)

# pos_tabela é um tupla (x, y), onde é a posição da 'var' recebida
def Encontra_Producao(matriz, var, pos_tabela, regras, tam_palavra):
    list_prod, list_pos1, list_pos2 = [], [], []
    linha, coluna = pos_tabela[0], pos_tabela[1]
    aux_diag = 0
    for k in range(tam_palavra-1, linha, -1):
        aux_diag += 1
        for B in matriz[k][coluna]:
            for C in matriz[linha+aux_diag][coluna+aux_diag]:
                if [B, C] in regras[var]:
                    list_prod.append([B,C])
                    list_pos1.append((k, coluna))
                    list_pos2.append((linha+aux_diag, coluna+aux_diag))

    return list_prod, list_pos1, list_pos2

def adiciona_terminais_Tree(T, palavra, cont=0):
    if T.left == None:
        T.left = Tree(palavra[cont])
        return cont+1
    else:
        cont = adiciona_terminais_Tree(T.left, palavra, cont)
        cont = adiciona_terminais_Tree(T.right, palavra, cont)

    return cont

def go_up_tree(tree):
    while tree.up != None:
        tree = tree.up
    return tree


def add_size(arv):
    if arv.up!=None:
        add_size(arv.up)
    else:
        arv.size += 1

# realiza a impressão da matriz no terminal (usado para testes iniciais)
def imprime_matriz(matrix):
    aux = 1
    for i in range(len(matrix)):
        print(matrix[i][0:aux])
        aux += 1

def aa(s):
    print(s)

    
#Abre Janela
app = APP()
app.win.mainloop()
