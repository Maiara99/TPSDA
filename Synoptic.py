import socket
import threading
import time
from variables import TCP_PORT, OPC_ADDR, TCP_ADDR

setpoint = "0"
setpoint_lock = threading.Lock()

def velocimetro(valor):
    # Verificar se o valor está no intervalo permitido
    if 0 <= valor <= 100:
        # Calcular a quantidade de underlines a serem substituídos por #
        num_underlines = round(valor / 100 * 10)

        # Formatar a string
        string_formatada = f"[{'#' * num_underlines}{'_' * (10 - num_underlines)}] {valor}"

        # Imprimir a string formatada
        print(string_formatada)
    else:
        print("Alerta, velocidade muito alta")

def controle_loop(socket):
    while True:
        velocidade = socket.recv(TCP_PORT)
        velocidade = round(float(velocidade))
        velocimetro(velocidade)
        time.sleep(0.5)

def aguardar_input():
    global setpoint
    while True:
        print("\nSet-Point Velocidade(0-100): ")
        novo_setpoint = input()
        with setpoint_lock:
            setpoint = novo_setpoint

def envia_setpoint(socket):
    global setpoint
    while True:
        with setpoint_lock:
            socket.sendall(setpoint.encode())
        time.sleep(0.5)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_ADDR, TCP_PORT))

controle_thread = threading.Thread(target=controle_loop, args=(s,))
input_thread = threading.Thread(target=aguardar_input)
envia_thread = threading.Thread(target=envia_setpoint, args=(s,))

controle_thread.start()
input_thread.start()
envia_thread.start()

try:
    controle_thread.join()
    input_thread.join()
    envia_thread.join()
except KeyboardInterrupt:
    print("\nEncerrando threads...")
