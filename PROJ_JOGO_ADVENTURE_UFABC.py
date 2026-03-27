# ==========================================================
#
# JOGO DESENVOLVIDO EM PYTHON PARA A DISCIPLINA DE P.I.
# PROCESSAMENTO DA INFORMAÇÃO - PROF. AMAURY KRUEL
# JEAN CARLOS MARTINS DO VALE
#
# ==========================================================

# ==========================================================
# LISTA DE PENDÊNCIAS:
# FUNCIONALIDADES DOS ITENS
# INTERAÇÕES ENTRE ITENS
# MISSÕES
# CONCLUSÃO DAS MISSÕES
# ==========================================================

import random
import json
import os
import pyfiglet

# =========================
# CONFIG VISUAL
# =========================

AMARELO = "\033[33m"     # História do item
MAGENTA = "\033[35m"     # Missão cumprida
VERMELHO = "\033[31m"    # Pegar item
VERDE = "\033[92m"       # Título
RESET = "\033[0m"

def titulo(texto="UFABC ARBO", fonte="slant"):
    print(VERDE + pyfiglet.figlet_format(texto, font=fonte) + RESET)

# =========================
# PASTA DE SAVE
# =========================

#Descobre a pasta onde o arquivo do jogo está
PASTA_JOGO = os.path.dirname(os.path.abspath(__file__))

#Cria a pasta de salvamento dentro da pasta do jogo
PASTA_SAVES = os.path.join(PASTA_JOGO, "SAVES")

def garantir_pasta():
    if not os.path.exists(PASTA_SAVES):
        os.makedirs(PASTA_SAVES)

# =========================
# AMBIENTES
# =========================

ambientes = {
1:"Portaria Avenida dos Estados",
2:"Parada de Ônibus",
3:"Portaria Torre do Relógio",
4:"Biblioteca",
5:"Portaria Rua Abolição",
6:"Bloco L",
7:"Portaria Rua Oratório",
8:"Bloco K",
9:"Restaurante Universitário",
10:"Estacionamento",
11:"Bloco A",
12:"Bloco Esportivo",
13:"Bloco B"
}

conexoes = {
1:[2,8,11,13],
2:[1,3],
3:[2,11,4],
4:[3,5,11,12],
5:[4,6,9,11],
6:[5,7,9],
7:[6,8,9],
8:[1,7,9,10],
9:[5,6,7,8,10,11],
10:[8,9,11],
11:[1,3,4,5,9,10,12],
12:[4,11],
13:[1]
}

# =========================
# ITENS
# =========================

def criar_itens():

    #------------------------------------------------------------------------
    #DICIONARIO:
    #req = quantidade de "Explorar" necessários para descobrir o item
    #cont = contador para atingir req
    #desc = o item foi descoberto pelo usuário
    #inv: o item está no invetário do ambiente
    #------------------------------------------------------------------------

    return [
        {"nome":"Carteirinha da UFABC","tipo":"habilitavel","ambiente":10,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Caderno de anotações","tipo":"habilitavel","ambiente":4,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Estojo com canetas","tipo":"habilitavel","ambiente":6,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Garrafa d'água","tipo":"habilitavel","ambiente":9,"req":2,"cont":0,"desc":False,"inv":False},
        {"nome":"Mochila","tipo":"habilitavel","ambiente":12,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Celular","tipo":"habilitavel","ambiente":6,"req":2,"cont":0,"desc":False,"inv":False},
        {"nome":"Carregador","tipo":"habilitavel","ambiente":7,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Placa com a senha do wi-fi 85265","tipo":"fixo","ambiente":13,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Papel com anotação 555943","tipo":"habilitavel","ambiente":5,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Registro de água","tipo":"fixo","ambiente":8,"req":2,"cont":0,"desc":False,"inv":False},
        {"nome":"Chave grifo","tipo":"habilitavel","ambiente":11,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Molho de chaves","tipo":"habilitavel","ambiente":3,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Tomada 1","tipo":"fixo","ambiente":4,"req":2,"cont":0,"desc":False,"inv":False},
        {"nome":"Tomada 2","tipo":"fixo","ambiente":11,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Tomada 3","tipo":"fixo","ambiente":13,"req":1,"cont":0,"desc":False,"inv":False}
    ]

# =========================
# ESTADO
# =========================

ambientes_iniciais = [1,3,5,7]

ambiente_atual = None
ambiente_anterior = None

inventario = []
registro_eventos = []
itens = criar_itens()
dificuldade = None

# =========================
# AUXILIARES
# =========================

def tem_item(nome):
    return nome in inventario

def itens_no_ambiente(amb):
    return [i for i in itens if i["ambiente"] == amb and not i["inv"]]

def itens_visiveis(amb):
    return [i for i in itens if i["ambiente"] == amb and i["desc"] and not i["inv"]]

# =========================
# MENU
# =========================

def menu():
    while True:
        titulo()
        print("1 - Como jogar")
        print("2 - Jogar")
        print("3 - Salvar")
        print("4 - Carregar")
        print("5 - Resetar")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1": como_jogar()
        elif op == "2": iniciar_jogo()
        elif op == "3": salvar()
        elif op == "4": menu_load()
        elif op == "5": resetar()
        elif op == "0": break

# =========================
# JOGO
# =========================

def iniciar_jogo():
    global ambiente_atual, ambiente_anterior, inventario, itens

    escolher_dificuldade()

    ambiente_atual = random.choice(ambientes_iniciais)
    ambiente_anterior = None
    inventario = []
    itens = criar_itens()

    mostrar_estado()
    loop()

def loop():
    while True:
        print("\n1-Mover \n2-Explorar \n3-Menu")
        op = input("Escolha: ")

        if op == "1":
            mover()
        elif op == "2":
            explorar()
        elif op == "3":
            break

# =========================
# ESTADO ATUAL
# =========================

def mostrar_estado():
    print("\n-------------------")
    print(f"\nVocê está em: {ambientes[ambiente_atual]}")

    vis = itens_visiveis(ambiente_atual)
    if vis:
        print("Itens disponíveis:")
        for i in vis:
            print("-", i["nome"])

    if inventario:
        print("Inventário:")
        print("- " + "\n- ".join(inventario))
    else:
        print("Inventário: vazio")

    print("\n-------------------")

# =========================
# MOVIMENTO
# =========================

def mover():
    global ambiente_atual, ambiente_anterior

    print(f"\nLocalização atual: {ambientes[ambiente_atual]} \nAmbientes próximos:")
    for d in conexoes[ambiente_atual]:
        print(d, ambientes[d])

    escolha = input("Destino escolhido: ")

    if not escolha.isdigit():
        print("Entrada inválida")
        return

    destino = int(escolha)

    if destino in conexoes[ambiente_atual]:
        ambiente_anterior = ambiente_atual
        ambiente_atual = destino
        mostrar_estado()

# =========================
# EXPLORAR
# =========================

def explorar():
    acabou_de_descobrir = False

    # BLOQUEIO CARTEIRINHA
    if ambiente_atual in [4,6,8,9,11,13] and not tem_item("Carteirinha da UFABC"):
        print("Acesso restrito! Você não tem a Carteirinha da UFABC")
        return

    locais = itens_no_ambiente(ambiente_atual)

    if not locais:
        print("Nada foi encontrado.")
        return

    encontrou = False

    for item in locais:

        # REGRA: Registro precisa chave grifo
        if item["nome"] == "Registro de água" and not tem_item("Chave grifo"):
            continue

        # REGRA: Chave grifo depende do ambiente anterior
        if item["nome"] == "Chave grifo":
            if ambiente_anterior not in [3,4,12]:
                continue

        # SOMA CONTAGEM
        item["cont"] += 1

        # DESCOBERTA
        if item["cont"] >= item["req"] and not item["desc"]:
            item["desc"] = True
            acabou_de_descobrir = True

            print(f"Você localizou {item['nome']} em {ambientes[item['ambiente']]}")

            if item["tipo"] == "fixo":
                print("Esse item é fixo.")

            encontrou = True

        if item["desc"] and not item["inv"]:
            encontrou = True

            if not acabou_de_descobrir:
                print(f"{item['nome']} está aqui.")
            
            if item["tipo"] != "fixo":
                op = input("Quer pegar o item? 1-Sim ou 2-Não: ")
                if op == "1":
                  inventario.append(item["nome"])
                  item["inv"] = True
                  print(f"{VERMELHO}{item['nome']} adicionado ao inventário{RESET}")


    if not encontrou:
        print("Nada foi encontrado.")

# =========================
# SAVE
# =========================

def salvar():
    if ambiente_atual is None:
        print("Nenhum jogo em andamento.")
        return
    
    garantir_pasta()

    nome = input("Nome do save: ").strip()
        
    if nome == "":
        print("Nome inválido.")
        return

    caminho = os.path.join(PASTA_SAVES, nome + ".json")

    dados = {
        "ambiente_atual": ambiente_atual,
        "ambiente_anterior": ambiente_anterior,
        "inventario": inventario,
        "itens": itens,
        "dificuldade": dificuldade
    }

    with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    print("Jogo salvo em: ", caminho)

def menu_load():
    garantir_pasta()

    arquivos = [a for a in os.listdir(PASTA_SAVES) if a.endswith(".json")]

    if not arquivos:
        print("Nenhum save encontrado.")
        return

    print("\nSaves disponives: \n")

    for i,a in enumerate(arquivos):
        print(i+1, "- ", a.replace(".json",""))

    op = input("Escolha o save: ")
    if not op.isdigit():
        return

    indice = int(op) - 1

    if indice < 0 or indice >= len(arquivos):
        return

    caminho = os.path.join(PASTA_SAVES,arquivos[indice])

    carregar(caminho)

def carregar(caminho):
    global ambiente_atual, ambiente_anterior, inventario, itens, dificuldade

    with open(caminho, "r", encoding="utf-8") as f:
        d = json.load(f)

    ambiente_atual = d["ambiente_atual"]
    ambiente_anterior = d["ambiente_anterior"]
    inventario = d["inventario"]
    itens = d["itens"]
    dificuldade = d["dificuldade"]

    mostrar_estado()
    loop()

# =========================
# RESET
# =========================

def resetar():
    global ambiente_atual, ambiente_anterior, inventario, itens

    ambiente_atual = None
    ambiente_anterior = None
    inventario = []
    itens = criar_itens()

    print("Jogo resetado.")

# =========================
# OUTROS
# =========================

def escolher_dificuldade():
    global dificuldade
    dificuldade = "Normal"

def como_jogar():
    titulo("COMO JOGAR", "small")
    print("""
Bem vindo aluno da UFABC!

Você é um estudante explorador e aqui vai poder conhecer o Campus de Santo André.

Ao caminhar pelo mapa você pode encontrar itens ocultos que são essenciais nas missões.

Seja persistente e tenha atenção por onde caminhar, uma busca rápida pode deixar passar muita coisa.

Objetivos:
Descobrir todos os ambientes
Conhecer os caminhos que conectam os edifícios
Encontrar os itens ocultos
Mapear as árvores que existem no campus
Irrigar toda a vegetação

Regras:
Use o teclado numérico e o enter para as ações

""")

# =========================
# EXECUÇÃO
# =========================

menu()