import numpy as np
from opcua import Client
TCP_PORT = 52550
TCP_ADDR = "127.0.0.1"
OPC_ADDR = "opc.tcp://127.0.0.1:53530/OPCUA/SimulationServer"
LA = 1.0
RA = 1.0
Km = 1.0
Kb = 1.0
Jm = 1.0
B = 1.0
Ki = 20
Kp = 100

client = Client(OPC_ADDR)
client.connect()

node_referencia = client.get_node("ns=3;i=1008")
node_velocidade = client.get_node("ns=3;i=1009")
node_acao_controle = client.get_node("ns=3;i=1010")
