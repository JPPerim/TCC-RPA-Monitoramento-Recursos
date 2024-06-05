import psutil
import time
import csv
from datetime import datetime 
import os
from tqdm import tqdm
import platform
# Intervalo de tempo em segundos para registrar os dados
INTERVAL = 1

# Nome do arquivo CSV
now = datetime.now()
csv_filename = f"recursos_computador_PS6_{now.strftime("%Y%m%d%H%M%S")}.csv"

# Função para obter dados de uso de recursos
def obter_dados():
    cpu_percent = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    uso_memoria_percent = memoria.percent
    disco = psutil.disk_usage('/')
    uso_disco_percent = disco.percent

    return {
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'cpu_percent': cpu_percent,
        'uso_memoria_percent': uso_memoria_percent,
        'uso_disco_percent': uso_disco_percent
    }

# Função para registrar os dados em um arquivo CSV
def registrar_dados(dados):
    file_exists = False
    try:
        with open(csv_filename, 'x', newline='') as csvfile:
            file_exists = True
    except FileExistsError:
        pass

    with open(csv_filename, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'cpu_percent', 'uso_memoria_percent', 'uso_disco_percent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(dados)

def clear_terminal():
    # Identifica o sistema operacional
    os_name = platform.system()

    if os_name == "Windows":
        os.system('cls')
    else:
        os.system('clear')
def desenhar_barra_progresso(nome, porcentagem, comprimento=30):
    # Calcula o número de blocos cheios
    num_blocos_preenchidos = int(porcentagem / 100 * comprimento)
    # Cria a barra de progresso com blocos cheios e vazios
    barra = '|' * num_blocos_preenchidos + ' ' * (comprimento - num_blocos_preenchidos)
    # Formata a string final
    barra_formatada = f"{nome} [{barra}] {porcentagem:.1f}%"
    return barra_formatada
if __name__ == "__main__":
    while True:
        dados = obter_dados()
        clear_terminal()
        print(desenhar_barra_progresso('CPU    ', dados['cpu_percent']))
        print(desenhar_barra_progresso('Memória', dados['uso_memoria_percent']))
        print(desenhar_barra_progresso('Disco  ', dados['uso_disco_percent']))
        registrar_dados(dados)
        time.sleep(INTERVAL - 1)