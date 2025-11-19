from dotenv import load_dotenv
import json
import os
import re
import google.generativeai as genai

# Criação da classe "Máquina"
class Maquina:

    def __init__(self, codigo, nome_maquina, capacidade):
        self.codigo = codigo
        self.nome_maquina = nome_maquina
        self.capacidade = capacidade
        self.status = False
        self.cliente = Cliente

    def getDados(self):
        print(f"Código: {self.codigo}")
        print(f"Nome: {self.nome_maquina}")
        print(f"Capacidade: {self.capacidade}kg")
        print(f"Status: {self.status}\n")

#Criação da classe "Cliente"
class Cliente:

    def __init__(self, codigo, nome_cliente, email):
        self.codigo = codigo
        self.nome_cliente = nome_cliente
        self.email = email
    
    def getDados(self):
        print(f"Código: {self.codigo}")
        print(f"Nome: {self.nome_cliente}")
        print(f"Email: {self.email}\n")

#Função para criar uma nova máquina
def nova_maquina():
    #Comando que será enviado para IA
    prompt = (
        "Retorne APENAS um objeto JSON com os campos:\n"
        '{"codigo", "nome_maquina":, "capacidade":}\n'
    "Sem texto adicional. Codigo deve ser inteiro e ÚNICO para cada solicitação; capacidade deve ser inteiro e um valor entre 10 a 20;\n"
    'e o nome_maquina deve ser um dos três seguintes: "Toshiba", "Panasonic", "Electrolux"'
    )

    #Escolha do modelo da IA, armazenamento da resposta e, por fim, a formatação da resposta
    modelo_IA = genai.GenerativeModel("gemini-2.5-flash")
    gerar_resposta_ia = modelo_IA.generate_content(prompt)
    formatação_resposta_ia = gerar_resposta_ia.text.strip()

    #Uso da RegEX para a procura do JSON
    procura_json = re.search(r"\{.*\}", formatação_resposta_ia, flags=re.DOTALL)
    if procura_json:
        try:
            data = json.loads(procura_json.group(0))
        except json.JSONDecodeError:
            raise ValueError("Texto extraído não é JSON válido.")

    #Atribuição do JSON para os atributos da Máquina
    codigo_maquina = int(data["codigo"])
    nome_maquina = str(data["nome_maquina"])
    capacidade_maquina = int(data["capacidade"])
    return Maquina(codigo_maquina, nome_maquina, capacidade_maquina)

#Função para a criação de um novo cliente, semelhante ao da criação da máquina
def novo_cliente():
    prompt = (
        "Retorne APENAS um objeto JSON com os campos:\n"
        '{"codigo", "nome_cliente":, "email":}\n'
    "Sem texto adicional. Codigo deve ser inteiro e ÚNICO para cada solicitação; nome_cliente deve ser qualquer nome genérico (Pedro, Gabriel, etc);\n"
    'e o email deve seguir esse padrão: "(nome_cliente completamente minúsculo)@gmail.com"'
    )

    modelo_IA = genai.GenerativeModel("gemini-2.5-flash")
    gerar_resposta_ia = modelo_IA.generate_content(prompt)
    formatação_resposta_ia = gerar_resposta_ia.text.strip()

    procura_json = re.search(r"\{.*\}", formatação_resposta_ia, flags=re.DOTALL)
    if procura_json:
        try:
            data = json.loads(procura_json.group(0))
        except json.JSONDecodeError:
            raise ValueError("Texto extraído não é JSON válido.")
    
    codigo_cliente = int(data["codigo"])
    nome_cliente = str(data["nome_cliente"])
    email = str(data["email"])
    return Cliente(codigo_cliente, nome_cliente, email)

#Função que limpa o terminal
def limpar_sistema():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

opcao = 1
lista_maquinas = []
lista_clientes = []

#Configuração da IA
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("A variável GEMINI_API_KEY não foi encontrada no .env!")

genai.configure(api_key=api_key)

#Menu
while opcao != 0:
    print("1. Cadastrar nova máquina")
    print("2. Cadastrar novo cliente")
    print("3. Utilizar máquina")
    print("4. Mostrar lista de máquinas")
    print("5. Mostrar lista de clientes")
    print("0. Sair")
    opcao = int(input("Informe a opção desejada: "))

    #Geração da máquina
    if opcao == 1:
        try:
            maquina = nova_maquina()
        except:
            raise ValueError("Erro ao criar nova máquina!")
        lista_maquinas.append(maquina)
        print("Máquina gerada com sucesso!\n"
              "(Aperte Enter para sair)")
        input()
    
    #Geração do cliente
    if opcao == 2:
        try:
            cliente = novo_cliente()
        except:
            raise ValueError("Erro ao criar novo cliente!")
        lista_clientes.append(cliente)
        print("Cliente gerado com sucesso!\n"
              "(Aperte Enter para sair)")
        input()

    #Ver disponibilidade da máquina e alocar o cliente a ela
    if opcao == 3:
        for cliente in lista_clientes:
            cliente.getDados()
        
        cod_cliente = int(input("Informe o código do cliente: "))
        
        validar = False
        for cliente in lista_clientes:
            if cliente.codigo == cod_cliente:
                validar = True
                break
        
        if not validar:
            raise ValueError("Código do cliente não se encontra no sistema!")

        carga_cliente = int(input("Informe quantos quilos de roupa ele quer lavar: "))

        for maquina in lista_maquinas:
            if maquina.status == True:
                print(f"Máquina {maquina.codigo} está ocupada por {maquina.cliente.nome_cliente}!\n"
                      "(Aperte Enter para sair)")
            elif maquina.capacidade < carga_cliente:
                print(f"Máquina {maquina.codigo} não suporta {carga_cliente}kg de roupa!\n"
                      "(Aperte Enter para sair)")        
            else:
                print(f"Máquina {maquina.codigo} agora está sendo usada!\n"
                      "(Aperte Enter para sair)")

                for i in range(len(lista_clientes)):
                    if lista_clientes[i].codigo == cod_cliente:
                        maquina.cliente = lista_clientes[i]
                        break

                maquina.status = True
                input()
                break

    if opcao == 4:
        for maquina in lista_maquinas:
            maquina.getDados()
        print("(Aperte Enter para sair)")
        input()

    if opcao == 5:
        for cliente in lista_clientes:
            cliente.getDados()
        print("(Aperte Enter para sair)")
        input()

    limpar_sistema()
