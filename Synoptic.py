import socket
import threading
import time
from variables import TCP_PORT, OPC_ADDR, TCP_ADDR

setpoint = "0"
setpoint_lock = threading.Lock()

def velocimetro(valor):
    if valor >= 100:
        valor = 100

    num_underlines = round(valor / 100 * 10)
    string_formatada = f"[{'#' * num_underlines}{'_' * (10 - num_underlines)}] {valor}, set-point: {setpoint}"
    if valor < 100 and valor > 90:
        print("Alerta Velocidade muito alta")
    elif valor == 100:
        print("Limite de velocidade atingido")
    print(string_formatada)
    with open('data.txt', 'a') as file:
        print(string_formatada, file=file)

def controle_loop(socket):
    while True:
        # velocidade = socket.recv(TCP_PORT)
        velocimetro(round(float(socket.recv(TCP_PORT))))
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
