import socket
import time
from datetime import datetime
from variables import TCP_PORT, OPC_ADDR, TCP_ADDR

def main():
    # Configurar socket e conectar ao servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_ADDR, TCP_PORT))

    # Dicionário para armazenar o status dos motores
    status_motores = {f'Motor {i}': {'Ativo': False, 'Velocidade': 0, 'Torque': 0, 'Velocidade Angular': 0} for i in range(1, 11)}

    # Número máximo de motores ativos permitidos
    max_motores_ativos = 4

    # Imprimir o texto de atualização e horário apenas uma vez
    atualizacao_motor = 1

    # Abrir o arquivo de histórico
    with open('historiador.txt', 'w') as arquivo:
        arquivo.write("--------------------------------------\n")
        arquivo.write("            HISTORICO DA\n")
        arquivo.write("      TELA DE CONTROLE DOS MOTORES\n")
        arquivo.write("--------------------------------------\n")

        while True:
            motor_id = input("Digite o ID do motor (de 1 a 10): ")
            motor_voltage = input("Digite o valor da tensão de entrada: ")

            # Verificar se a tensão é zero para desligar o motor
            if float(motor_voltage) == 0:
                print(f"MOTOR {motor_id} DESLIGADO")

                # Atualizar o status do motor para "Desligado" e zerar as informações
                status_motores[f'Motor {motor_id}'] = {'Ativo': False, 'Velocidade': 0, 'Torque': 0, 'Velocidade Angular': 0}
            else:
                # Verificar regra: Não pode haver mais de 4 motores ativos
                motores_ativos = sum(valores['Ativo'] for valores in status_motores.values())
                if motores_ativos >= max_motores_ativos:
                    print("Erro: Não pode haver mais de 4 motores ativos.")
                else:
                    # Verificar regra: Não pode haver dois motores consecutivos ativos
                    motor_id_int = int(motor_id)
                    if motor_id_int > 1 and status_motores[f'Motor {motor_id_int - 1}']['Ativo']:
                        print("Erro: Não pode haver dois motores consecutivos ativos.")
                    else:
                        # Montar a mensagem para o servidor no formato "motor_id,voltage"
                        message = f"{motor_id},{motor_voltage.replace(',', '.')}"
                        s.sendall(message.encode())

                        # Aguardar e receber o resultado da simulação do motor
                        result = s.recv(TCP_PORT)

                        if not result:
                            print("Conexão encerrada pelo servidor.")
                            break

                        # Atualizar o status do motor no dicionário
                        resultados_motores = result.decode().split(',')
                        for i in range(0, len(resultados_motores), 4):
                            motor_info = resultados_motores[i:i+4]
                            motor_id = motor_info[0].split(':')[0]
                            wm = motor_info[1].split(':')[1]
                            tau0 = motor_info[2].split(':')[1]
                            w0 = motor_info[3].split(':')[1]

                            # Atualizar apenas as informações relevantes do motor no dicionário
                            status_motores[f'Motor {motor_id}'].update({'Ativo': True, 'Velocidade': wm, 'Torque': tau0, 'Velocidade Angular': w0})

            # Imprimir status de todos os motores
            horario_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Atualização: {atualizacao_motor} - Horário: {horario_atual}")
            print("--------------------------------------\n")

            for motor, valores in status_motores.items():
                print(f"{motor} - {'Ativo' if valores['Ativo'] else 'Desligado'}")
                if valores['Ativo']:
                    print(f"Velocidade: {valores['Velocidade']}, Torque: {valores['Torque']}, Velocidade Angular: {valores['Velocidade Angular']}")
                print("--------------------------------------\n")

                # Escrever no arquivo de histórico
                arquivo.write(f"--------------------------------------\n")
                arquivo.write(f"Atualização: {atualizacao_motor} - Horário: {horario_atual}\n")
                arquivo.write(f"{motor} - {'Ativo' if valores['Ativo'] else 'Desligado'}\n")
                if valores['Ativo']:
                    arquivo.write(f"Velocidade: {valores['Velocidade']}, Torque: {valores['Torque']}, Velocidade Angular: {valores['Velocidade Angular']}\n")
                arquivo.write(f"Tensão de entrada: {motor_voltage}\n")
                arquivo.write("--------------------------------------\n")

            atualizacao_motor += 1
            time.sleep(0.5)

    # Fechar o socket
    s.close()

if __name__ == "__main__":
    main()
