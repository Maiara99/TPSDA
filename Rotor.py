import numpy as np
from opcua import Client
import time
from variables import OPC_ADDR, TCP_ADDR, TCP_PORT

def Motor(u, tau0, w0):
    # Definição da equação a diferenças
    tauL = np.random.uniform(0, 10)
    deltat=0.1
    tau_next = tau0 + deltat * (u - w0 - tau0)
    w_next = w0 + deltat * (tau0 - tauL - w0)

    # Retornar a velocidade de rotação
    if np.isnan(tau_next) or np.isnan(w_next):
        # Verificar por NaN e tratar a situação
        return 0, tau0, w0

    wm_next = (tau_next - tau0) / deltat
    return wm_next, tau_next, w_next

##################
# Cria o client
client = Client(OPC_ADDR)
client.connect()

##################
node_h = client.get_node("ns=3;i=1008")
node_q_in = client.get_node("ns=3;i=1009")
node_h_ref = client.get_node("ns=3;i=1010")

# Condição inicial para a simulação do tanque
tau0 = 0
w0 = 0

while True:
    href = node_h_ref.get_value()
    # Valor de controle em malha aberta (ajuste conforme necessário)
    control = href

    wm, tau0, w0 = Motor(control, tau0, w0)

    node_q_in.set_value(control)
    node_h.set_value(wm)
