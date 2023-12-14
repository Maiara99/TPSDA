import threading
import time
import socket
import random  
# from opcua import Client  # Comente essa linha para desativar a importação

from variables import OPC_ADDR, TCP_ADDR, TCP_PORT

mutex = threading.Lock()
velocidades_motores = {}

def simular_motor(motor_id, tensao_entrada):
    if tensao_entrada == 0:
        return 0, 0, 0, 0  # Se a tensão de entrada for zero, retornar valores zerados
    else:
        wm = random.uniform(50, 200)
        tau0 = random.uniform(5, 15)
        w0 = random.uniform(100, 300)
        alarme = random.choice([0, 1])
        return wm, tau0, w0, alarme

def servidor_tcp(stop_event):
    global mutex, velocidades_motores
    print("Servidor TCP iniciado")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_ADDR, TCP_PORT))

    s.listen()
    print("Esperando conexoes...")

    conn, addr = s.accept()
    with conn:
        print(f"Conectado por {addr}")

        while not stop_event.is_set():
            try:
                data = conn.recv(TCP_PORT)
                if not data:
                    break
                
                motor_id, tensao_entrada = map(int, data.decode().split(','))

                # Simulação do motor
                wm, tau0, w0, alarme = simular_motor(motor_id, tensao_entrada)

                # Atualizar informações do motor
                with mutex:
                    velocidades_motores[motor_id] = {'Velocidade': wm, 'Torque': tau0, 'Velocidade Angular': w0, 'Alarme': alarme}

                # Montar a mensagem de resposta para o cliente
                result_message = ','.join(f"{motor}: {valor}" for motor, valores in velocidades_motores.items() for valor in valores.values())

                # Enviar resultado para o cliente
                conn.sendall(result_message.encode())

                time.sleep(0.5)
            except Exception as e:
                print(f"Erro na execução do servidor TCP: {e}")
                break

# Comente toda a função do cliente OPC
# def cliente_opc(stop_event):
#     global mutex, velocidadeRotor
#     print("Cliente OPC iniciado")
#
#     client = Client(OPC_ADDR)
#     client.connect()
#
#     node_h = client.get_node("ns=3;i=1008")
#
#     while not stop_event.is_set():
#         try:
#             with mutex:
#                 h_value = node_h.get_value()
#                 print(f"Valor atual de h no servidor OPC: {h_value}")
#
#             time.sleep(1)
#         except Exception as e:
#             print(f"Erro na execução do cliente OPC: {e}")
#             break

# Cria um evento para sinalizar a thread para parar
stop_event = threading.Event()

# Inicia apenas a thread do servidor TCP
thread_tcp = threading.Thread(target=servidor_tcp, args=(stop_event,))
# Comente a linha abaixo para desativar a inicialização da thread do cliente OPC
# thread_opc = threading.Thread(target=cliente_opc, args=(stop_event,))

thread_tcp.start()
# Comente a linha abaixo para desativar o início da thread do cliente OPC
# thread_opc.start()

# Aguarda o encerramento da thread do servidor TCP
thread_tcp.join()
# Comente a linha abaixo para desativar a espera pelo encerramento da thread do cliente OPC
# thread_opc.join()
