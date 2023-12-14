import threading
import time
import socket
from opcua import Client
from variables import *

mutex = threading.Lock()
velocidadeRotor = 0

def controlador(stop_event):
    global mutex, velocidadeRotor, qin, qout
    print("CLP iniciado")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_ADDR, TCP_PORT))

    s.listen()
    print("Esperando conexoes...")

    conn, addr = s.accept()
    with conn:
        print(f"Conectado por {addr}")
        mutex.acquire()
        while not stop_event.is_set():
            try:
                time.sleep(0.5)
                href = conn.recv(TCP_PORT)
                if not href:
                    break
                href = float(href.decode())
                node_referencia.set_value(href)
                velocidadeRotor = node_velocidade.get_value()
                data = str(velocidadeRotor).encode("utf-8")
                conn.sendall(data)
            except Exception as e:
                print(f"Erro na execução: {e}")
                break
        mutex.release()
stop_event = threading.Event()
thread = threading.Thread(target=controlador, args=(stop_event,))
thread.start()
thread.join()
