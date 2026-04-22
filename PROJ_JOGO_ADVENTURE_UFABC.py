# ==========================================================
#
# JOGO DESENVOLVIDO EM PYTHON PARA A DISCIPLINA DE P.I.
# PROCESSAMENTO DA INFORMAÇÃO - PROF. DR. AMAURY KRUEL BUDRI
# JEAN CARLOS MARTINS DO VALE
#
# ==========================================================

# ==========================================================
# LISTA DE PENDÊNCIAS:
# FUNCIONALIDADES DOS ITENS
#   Mapa / Mochila / Chave grifo / Registro de água / Papel com senha / Molho de chaves
# INTERAÇÕES ENTRE ITENS
# MISSÕES
# CONCLUSÃO DAS MISSÕES
# ==========================================================

import random
import json
import os
import pyfiglet

# =========================
# CORES
# =========================

AMARELO = "\033[33m"     # Item selecionado
MAGENTA = "\033[35m"     # Missão cumprida
VERMELHO = "\033[31m"    # Pegar item
VERDE = "\033[92m"       # Título e descobrir item
RESET = "\033[0m"        # Remove a cor

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
# ARVORES
# =========================

def distribuir_arvores():
    base = {i:4 for i in [1,2,3,4,5,6,7,9,10,12]}
    restante = 100 - sum(base.values())

    while restante > 0:
        amb = random.choice(list(base.keys()))

        limite = 7 if amb in [1,3,4,7] else 15

        if base[amb] < limite:
            base[amb] += 1
            restante -= 1

    return base

quant_arvores = distribuir_arvores()

arvores_descobertas = {i: False for i in quant_arvores}
arvores_irrigadas = {i: 0 for i in quant_arvores}

sistema_irrigacao = False
# =========================
# ITENS
# =========================

def criar_itens():

    #------------------------------------------------------------------------
    #DICIONÁRIO:
    #req = quantidade de "Explorar" necessários para descobrir o item (tornar o item visível)
    #cont = contador para atingir req
    #desc = o item está visível ou não para o usuário
    #inv: o item está no invetário do usário
    #------------------------------------------------------------------------

    return [
        {"nome":"Carteirinha da UFABC","tipo":"habilitavel","ambiente":10,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Caderno de anotações","tipo":"habilitavel","ambiente":4,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Estojo com canetas","tipo":"habilitavel","ambiente":6,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Garrafa d'água","tipo":"habilitavel","ambiente":9,"req":2,"cont":0,"desc":False,"inv":False,"quant_agua":0,"max_agua":3},
        {"nome":"Mochila","tipo":"habilitavel","ambiente":12,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Celular","tipo":"habilitavel","ambiente":7,"req":1,"cont":0,"desc":False,"inv":False,"carregado":False,"internet":False},
        {"nome":"Carregador","tipo":"habilitavel","ambiente":7,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Placa com a senha do wi-fi 85265","tipo":"fixo","ambiente":13,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Papel com senha 555943","tipo":"habilitavel","ambiente":5,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Registro de água","tipo":"fixo","ambiente":8,"req":2,"cont":0,"desc":False,"inv":False},
        {"nome":"Chave grifo","tipo":"habilitavel","ambiente":11,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Molho de chaves","tipo":"habilitavel","ambiente":3,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Regador","tipo":"habilitavel","ambiente":11,"req":4,"cont":0,"desc":False,"inv":False,"quant_agua":0,"max_agua":6},
        {"nome":"Tomada","tipo":"fixo","ambiente":4,"req":2,"cont":0,"desc":False,"inv":False},
        {"nome":"Tomada","tipo":"fixo","ambiente":11,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Tomada","tipo":"fixo","ambiente":13,"req":3,"cont":0,"desc":False,"inv":False},
        {"nome":"Bebedouro","tipo":"fixo","ambiente":4,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Bebedouro","tipo":"fixo","ambiente":11,"req":2,"cont":0,"desc":False,"inv":False},
        {"nome":"Bebedouro","tipo":"fixo","ambiente":12,"req":1,"cont":0,"desc":False,"inv":False},
        {"nome":"Bebedouro","tipo":"fixo","ambiente":13,"req":1,"cont":0,"desc":False,"inv":False}
        
    ]

# =========================
# VARIÁVEIS GLOBAIS
# =========================

ambientes_iniciais = [1,3,5,7]

ambiente_atual = None
ambiente_anterior = None

ambientes_anotados = set()

inventario = []
registro_eventos = []
itens = criar_itens()

# =========================
# AÇÕES
# =========================

def acao_celular_carregador_tomada():
    celular = buscar_item("Celular")
    if not item_visivel_ambiente("Tomada", ambiente_atual):
        print("Algo está errado, você pode tentar usar de novo.")
        return
    celular["carregado"] = True
    print("Agora o celular está carregado.")

def acao_celular_solo():
    celular = buscar_item("Celular")
    if not celular["carregado"]:
        print("O celular está descarregado.")
        return
    
    if not celular["internet"]:
        senha = input("Você pode se conectar ao Wi-fi. Qual é a senha? ")
        if senha.strip() == "85265":
            celular["internet"] = True
            print("Você se conectou ao Wi-fi e baixou o app UFABC ARBO.")
        return
    
    if ambiente_atual not in quant_arvores:
        print(f"{ambientes[ambiente_atual]} não possui árvores.")
        return
    
    if arvores_descobertas[ambiente_atual]:
        print(f"Você já localizou todas as árvores de {ambientes[ambiente_atual]}.")
        return
    
    arvores_descobertas[ambiente_atual] = True
    print(f"""
Parabéns, você localizou todas as {quant_arvores[ambiente_atual]} árvores de {ambientes[ambiente_atual]}!
""")

def acao_caderno_solo():
    pass  # lógica futura

def acao_garrafa_bebedouro():
    garrafa = buscar_item_inventario("Garrafa d'água")

    if not item_visivel_ambiente("Bebedouro", ambiente_atual):
        print("Não há bebedouro visível neste ambiente.")
        return

    if garrafa["quant_agua"] == garrafa["max_agua"]:
        print("Garrafa d'água já está cheia.")
        return

    garrafa["quant_agua"] = garrafa["max_agua"]
    print(f"""
Você encheu a Garrafa d'água.

Volume atual: {garrafa['quant_agua']}/{garrafa['max_agua']}
""")

def acao_garrafa_solo():
    garrafa = buscar_item_inventario("Garrafa d'água")

    if garrafa["quant_agua"] == 0:
        print("Garrafa d'água está sem água.")
        return
    
    if ambiente_atual not in quant_arvores:
        print(f"{ambientes[ambiente_atual]} não possui árvores.")
        return
    
    ja_irrigadas = arvores_irrigadas[ambiente_atual]
    total = quant_arvores[ambiente_atual]

    if not arvores_descobertas[ambiente_atual]:
        print(f"Não há árvores descobertas em {ambientes[ambiente_atual]}.")
        return

    if ja_irrigadas >= total:
        print(f"Todas as árvores de {ambientes[ambiente_atual]} já foram irrigadas.")
        return

    falta_irrigar = total - ja_irrigadas
    disponivel    = garrafa["quant_agua"]

    print(f"""
Árvores descobertas:  {total}
Já irrigadas:         {ja_irrigadas}
Faltam irrigar:       {falta_irrigar}
Água disponível:      {disponivel}
""")

    volume = input(f"Quanto volume deseja usar? (1 a {min(disponivel, falta_irrigar)}): ")

    if not volume.isdigit():
        print("Entrada inválida.")
        return

    volume = int(volume)

    if volume < 1 or volume > min(disponivel, falta_irrigar):
        print("Volume inválido.")
        return

    garrafa["quant_agua"]              -= volume
    arvores_irrigadas[ambiente_atual]  += volume

    print(f"""
{volume} unidades de água utilizadas.
Garrafa d'água: {garrafa["quant_agua"]}/{garrafa["max_agua"]}
Árvores irrigadas em {ambientes[ambiente_atual]}: {arvores_irrigadas[ambiente_atual]}/{total}
""")

def acao_regador_bebedouro():
    regador = buscar_item_inventario("Regador")

    if not item_visivel_ambiente("Bebedouro", ambiente_atual):
        print("Não há bebedouro visível neste ambiente.")
        return

    if regador["quant_agua"] == regador["max_agua"]:
        print("Regador já está cheio.")
        return

    regador["quant_agua"] = regador["max_agua"]
    print(f"""
Você encheu o Regador.
Volume atual: {regador['quant_agua']}/{regador['max_agua']}
""")

def acao_regador_solo():
    regador = buscar_item_inventario("Regador")

    if regador["quant_agua"] == 0:
        print("Regador está sem água.")
        return
    
    if ambiente_atual not in quant_arvores:
        print(f"{ambientes[ambiente_atual]} não possui árvores.")
        return

    ja_irrigadas = arvores_irrigadas[ambiente_atual]
    total = quant_arvores[ambiente_atual]

    if not arvores_descobertas[ambiente_atual]:
        print(f"Não há árvores descobertas em {ambientes[ambiente_atual]}.")
        return

    if ja_irrigadas >= total:
        print(f"Todas as árvores de {ambientes[ambiente_atual]} já foram irrigadas.")
        return

    falta_irrigar = total - ja_irrigadas
    disponivel    = regador["quant_agua"]

    print(f"""
Árvores descobertas:  {total}
Já irrigadas:         {ja_irrigadas}
Faltam irrigar:       {falta_irrigar}
Água disponível:      {disponivel}
""")

    volume = input(f"Quanto volume deseja usar? (1 a {min(disponivel, falta_irrigar)}): ")

    if not volume.isdigit():
        print("Entrada inválida.")
        return

    volume = int(volume)

    if volume < 1 or volume > min(disponivel, falta_irrigar):
        print("Volume inválido.")
        return

    regador["quant_agua"] -= volume
    arvores_irrigadas[ambiente_atual] += volume

    print(f"""
Regador: {regador["quant_agua"]}/{regador["max_agua"]}
Árvores irrigadas em {ambientes[ambiente_atual]}: {arvores_irrigadas[ambiente_atual]}/{total}
""")

def acao_mapa_solo():
    pass  # lógica futura

def acao_grifo_registro():
    pass  # lógica futura

#Dicionário de combinações válidas de itens
COMBINACOES_VALIDAS = [
    {"conjunto": {"Celular", "Carregador", "Tomada"}, "acao": acao_celular_carregador_tomada},
    {"conjunto": {"Celular"}, "acao": acao_celular_solo},
    {"conjunto": {"Caderno de anotações"}, "acao": acao_caderno_solo},
    {"conjunto": {"Garrafa d'água", "Bebedouro"}, "acao": acao_garrafa_bebedouro},
    {"conjunto": {"Garrafa d'água"}, "acao": acao_garrafa_solo},
    {"conjunto": {"Regador", "Bebedouro"}, "acao": acao_regador_bebedouro},
    {"conjunto": {"Regador"}, "acao": acao_regador_solo},
    {"conjunto": {"Mapa"}, "acao": acao_mapa_solo},
    {"conjunto": {"Chave grifo", "Registro de água"}, "acao": acao_grifo_registro},
]

# =========================
# AUXILIARES
# =========================

def item_visivel_ambiente(nome, amb):
    for item in itens:
        if item.get("nome") == nome and item.get("ambiente") == amb and item.get("desc"):
            return True
    return False

# Itens fixos descobertos no ambiente atual
def itens_disponiveis_usar():
    disponiveis = list(inventario)

    for item in itens:
        if item.get("ambiente") == ambiente_atual and item.get("desc"):
            if item["nome"] not in disponiveis:
                disponiveis.append(item["nome"])

    return disponiveis

def buscar_item(nome, amb=None):
    for item in itens:
        if item.get("nome") == nome:
            if amb is None or item.get("ambiente") == amb:
                return item
    return None

def buscar_item_inventario(nome):
    for item in itens:
        if item.get("nome") == nome and item.get("inv"):
            return item
    return None

def tem_item(nome):
    return nome in inventario

def itens_no_ambiente(amb):
    lista = []
    
    for item in itens:
        
        if "ambiente" in item:
            if item["ambiente"] == amb and not item["inv"]:
                lista.append(item)
 
    return lista

def itens_visiveis(amb):
    resultado = []

    for i in itens:
        #Itens normais
        if "ambiente" in i:
            if i["ambiente"] == amb and i["desc"] and not i["inv"]:
                resultado.append(i)

    return resultado

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
    global ambiente_atual, ambiente_anterior, inventario, itens, ambientes_anotados, quant_arvores, arvores_descobertas, arvores_irrigadas

    ambiente_atual = random.choice(ambientes_iniciais)
    ambiente_anterior = None
    inventario = []
    itens = criar_itens()
    ambientes_anotados  = set()
    quant_arvores       = distribuir_arvores()
    arvores_descobertas = {i: False for i in quant_arvores}
    arvores_irrigadas   = {i: 0     for i in quant_arvores}

    mostrar_estado()
    loop()

def loop():
    while True:
        print("\n1 - Mover \n2 - Explorar \n3 - Usar \n4 - Salvar \n5 - Menu")
        op = input("Escolha: ")

        if op == "1":
            mover()
        elif op == "2":
            explorar()
        elif op == "3":
            usar()
        elif op == "4":
            print("""
Você quer salvar o jogo?
1 - Sim
2 - Não
""")
            confirma = input("Escolha: ")
            if confirma == "1":
                salvar()
            elif confirma == "2":
                print("Salvamento do jogo cancelado.")
        
        elif op == "5":
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
# REGISTRO DE AMBIENTE PARA MAPA
# =========================

def registrar_amb_caderno():
    global ambientes_anotados

    if not (tem_item("Caderno de anotações") and tem_item("Estojo com canetas")):
        return

    if ambiente_atual in ambientes_anotados:
        return

    ambientes_anotados.add(ambiente_atual)
    print(f"""
{ambientes[ambiente_atual]} foi anotado no caderno.
Ambientes registrados: {len(ambientes_anotados)} de {len(ambientes)}.
          """)

    if ambientes_anotados == set(ambientes.keys()):
        inventario.remove("Caderno de anotações")
        inventario.remove("Estojo com canetas")
        inventario.append("Mapa")
        print("""
Parabéns!
              
Você registrou todos os ambientes do Campus Santo André da UFABC.
              
Agora você tem o Mapa do Campus.
              """)

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
        registrar_amb_caderno()

# =========================
# EXPLORAR
# =========================

def explorar():
    
        # BLOQUEIO CARTEIRINHA
    if ambiente_atual in [4,6,8,9,11,13] and not tem_item("Carteirinha da UFABC"):
        print(f"{VERMELHO}Acesso restrito!{RESET} Você não tem a Carteirinha da UFABC")
        return

    locais = itens_no_ambiente(ambiente_atual)

    if not locais:
        print("Nada foi encontrado.")
        return

    encontrou = False

    for item in locais:
        acabou_de_descobrir = False

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

            print(f"{VERDE}Você localizou {item['nome']} em {ambientes[item['ambiente']]}{RESET}")

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
# USAR
# =========================

def usar():
    disponiveis = itens_disponiveis_usar()

    if not disponiveis:
        print("Nenhum item disponível para usar.")
        return

    selecionados = set()

    while True:
        print("\nItens disponíveis:")
        for i, nome in enumerate(disponiveis):
            marcado = f"{AMARELO}[X]{RESET}" if nome in selecionados else "[ ]"
            print(f"{i+1} - {marcado} {nome}")
        print("Digite o número do item para selecionar")

        op = input("Após selecionar o item, digite 0 para confirmar: ")

        if op == "0":
            break
        if not op.isdigit():
            print("Entrada inválida.")
            continue

        idx = int(op) - 1
        if idx < 0 or idx >= len(disponiveis):
            print("Entrada inválida.")
            continue

        nome = disponiveis[idx]
        if nome in selecionados:
            selecionados.remove(nome)
        else:
            selecionados.add(nome)

    if not selecionados:
        print("Nenhum item selecionado.")
        return

    for combo in COMBINACOES_VALIDAS:
        if selecionados == combo["conjunto"]:
            combo["acao"]()
            return

    print("Algo está errado, você pode tentar usar de novo.")

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
        "ambientes_anotados": list(ambientes_anotados),  # set → list
        "quant_arvores": quant_arvores,
        "arvores_descobertas": arvores_descobertas,
        "arvores_irrigadas": arvores_irrigadas,
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
    global ambiente_atual, ambiente_anterior, inventario, itens,ambientes_anotados, quant_arvores, arvores_descobertas, arvores_irrigadas

    with open(caminho, "r", encoding="utf-8") as f:
        d = json.load(f)

    ambiente_atual = d["ambiente_atual"]
    ambiente_anterior = d["ambiente_anterior"]
    inventario = d["inventario"]
    itens = d["itens"]
    ambientes_anotados = set(d["ambientes_anotados"])
    quant_arvores = {int(k): v for k, v in d["quant_arvores"].items()}
    arvores_descobertas = {int(k): v for k, v in d["arvores_descobertas"].items()}
    arvores_irrigadas = {int(k): v for k, v in d["arvores_irrigadas"].items()}

    mostrar_estado()
    loop()

# =========================
# RESET
# =========================

def resetar():
    global ambiente_atual, ambiente_anterior, inventario, itens, ambientes_anotados, quant_arvores, arvores_descobertas, arvores_irrigadas

    ambiente_atual = None
    ambiente_anterior = None
    inventario = []
    itens = criar_itens()
    ambientes_anotados = set()
    quant_arvores = distribuir_arvores()
    arvores_descobertas = {i: False for i in quant_arvores}
    arvores_irrigadas = {i: 0 for i in quant_arvores}

    print("Jogo resetado.")

# =========================
# COMO JOGAR
# =========================

def como_jogar():
    titulo("COMO JOGAR", "small")
    print("""
Bem vindo aluno da UFABC!

Você é um estudante explorador e aqui vai poder conhecer o Campus de Santo André.

Ao caminhar pelo mapa você pode encontrar itens ocultos que são essenciais nas missões.

Seja persistente e tenha atenção por onde caminhar, uma busca rápida pode deixar passar muita coisa.

Objetivos:
Encontrar os itens ocultos
Descobrir todos os ambientes
Mapear as árvores que existem no campus
Irrigar toda a vegetação

Regras:
Use o teclado numérico e o enter para as ações
""")

# =========================
# EXECUÇÃO
# =========================

menu()