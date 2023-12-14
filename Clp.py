import threading
import time
import socket
from opcua import Client
from Variables import *
mutex = threading.Lock()
velocidadeRotor = 0
def controlador(stop_event):
    global mutex, velocidadeRotor, qin, qout
    print("Inicialização CLP feita com sucesso.\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_ADDR, TCP_PORT))

    sock.listen()
    print("Aguardando clientes...")

    userconnection, useraddress = sock.accept()
    with userconnection:
        print(f"Novo cliente, endereço: {useraddress}")
        mutex.acquire()
        while not stop_event.is_set():
            try:
                time.sleep(0.5)
                href = userconnection.recv(TCP_PORT)
                if not href:
                    break
                href = float(href.decode())
                node_referencia.set_value(href)
                velocidadeRotor = node_velocidade.get_value()
                data = str(velocidadeRotor).encode("utf-8")
                userconnection.sendall(data)
            except Exception as e:
                print(f"Erro na execução: {e}")
                break
        mutex.release()
stop_event = threading.Event()
thread = threading.Thread(target=controlador, args=(stop_event,))
thread.start()
thread.join()
