import json
import sys

def carregar_json(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        return json.load(arquivo)

def carregar_txt(arquivo_entrada):
    with open(arquivo_entrada, "r") as arquivo_txt:
        return arquivo_txt.readlines()

def buscar_transicao(estado_atual, maquina_turing, simbolo_lido):
    for transicao in maquina_turing['transitions']:
        if transicao['from'] == estado_atual and transicao['read'] == simbolo_lido:
            return (transicao["to"], transicao["write"], transicao["dir"])
    return None

def simular_maquina_turing(maquina_turing, entrada):
    estado_atual = maquina_turing['initial']
    indice = 0
    fita = list(entrada)
    simbolo_branco = maquina_turing['white']

    while estado_atual not in maquina_turing['final']:
        simbolo_lido = fita[indice]

        transicao = buscar_transicao(estado_atual, maquina_turing, simbolo_lido)
        if transicao is None:
            break

        estado_atual, simbolo_escrito, direcao = transicao
        fita[indice] = simbolo_escrito

        if direcao == 'R':
            indice += 1
        elif direcao == 'L':
            indice -= 1

        if indice < 0:
            fita.insert(0, simbolo_branco)
            indice = 0
        elif indice >= len(fita):
            fita.append(simbolo_branco)

    if estado_atual in maquina_turing['final']:
        print(1)
    else:
        print(0)

    return "".join(fita).strip()

def principal(arquivo_maquina_turing, arquivo_entrada, arquivo_saida):
    maquina_turing = carregar_json(arquivo_maquina_turing)
    entradas = carregar_txt(arquivo_entrada)

    if not entradas:
        return

    try:
        with open(arquivo_saida, 'w', newline='') as arquivo_saida:
            for entrada in entradas:
                entrada = entrada.strip()
                resultado = simular_maquina_turing(maquina_turing, entrada)
                arquivo_saida.write(f"{resultado}\n")
    except Exception as erro:
        print(f"Erro no arquivo de saída {arquivo_saida}: {erro}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python simulador.py <arquivo_maquina_turing.json> <arquivo_entrada.txt> <arquivo_saida.txt>")
        sys.exit(1)

    arquivo_maquina_turing = sys.argv[1]
    arquivo_entrada = sys.argv[2]
    arquivo_saida = sys.argv[3]
    principal(arquivo_maquina_turing, arquivo_entrada, arquivo_saida)
