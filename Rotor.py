import time
from scipy.integrate import odeint
import numpy as np
from variables import *
from opcua import Client
client = Client(OPC_ADDR)

client.connect()

def motor_eq(y, t, velocidade, tau_L):
    tau_motor, omega_m = y

    dtau_motor = (Km * velocidade - (Km * Kb) * omega_m - LA * tau_motor) / RA
    domega_m = (tau_motor - B * omega_m - tau_L) / Jm
    return [dtau_motor, domega_m]

def integrar_EDO(y, t, velocidade, tau_L, tempo_passo=0.1):
    sol = odeint(motor_eq, y, [t, t + tempo_passo], args=(velocidade, tau_L))
    return sol[1, :]

tempo = 0.0
y_atual = [0.0, 0.0] 
erro_integral = 0.0;
velocidade_proximo_instante = 0
velocidade_controle = 0
# Realizando integração em tempo real
while True:  # Por exemplo, 10 iterações
    referencia = node_referencia.get_value()
    erro = referencia - velocidade_proximo_instante;
    erro_integral += erro;
    
    velocidade_controle = erro*Ki + Kp;

    y_proximo = integrar_EDO(y_atual, tempo, velocidade_controle, np.random.uniform(0, 1))
    velocidade_proximo_instante = y_proximo[1];
    
    tempo += 0.1  # Ajuste conforme necessário
    y_atual = y_proximo
    node_velocidade.set_value(velocidade_proximo_instante)

