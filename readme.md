# Controle de Tanque - Documentação

**Desenvolvido por:**
- Igor Duarte Amoras Dos Santos (2019056920)
- Maiara Cristina Silva Lima (2018014565)

**Última Atualização:** 14.12.2023

---
Este arquivo foi escrito em .md, para uma melhor experiência do leitor. Caso esteja usando Visual Studio Code, digite Ctrl+K V para visualizá-lo. Caso não, use a plataforma que lhe for melhor. 

## Pré-requisitos

O sistema opera e conexões TCP e OPC, além de performar integrações numéricas, então, é nessário que as devidas bibliotecas estejam instaladas. Executando o seguinte comando no prompt de comando as biblioteas serão instaladas:

```bash
pip install numpy scipy socket opcua
```

# Instruções de execução
Primeiramente é necessário que o <strong>servidor OPC</strong> esteja ativo, no caso deste sistema, ele foi feito com o auxílio do Software<em> Prosys OPC UA Simulation Server</em>, e o servidor tem o seguinte endereço
```python
OPC_ADDR = "opc.tcp://127.0.0.1:53530/OPCUA/SimulationServer"

```
Caso o servidor OPC esteja em um endereço diferente, altere-o no arquivo <em>Variables.py</em>. O sistema utiliza três variáveis do OPC, denominadas, <em>velocidade, acao_controle e referencia</em>, portanto assegure o servidor está devidamente configurado. 
Com isto feito, a única restrição à execução do sistema é que o arquivo <em>Clp.py</em> seja executado antes do arquivo <em>Synoptic.py</em>, isto pois, o Clp é o servidor e o Synoptic é o cliente. Portanto, em terminais diferentes, execute:
```bash
# Terminal 1
python Rotor.py
# Terminal 2
python Clp.py
# Terminal 3
python Synoptic.py
```