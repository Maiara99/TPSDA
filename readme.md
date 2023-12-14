# Controle de Tanque - README

**Desenvolvido por:**
- Igor Duarte Amoras Dos Santos (2019056920)
- Maiara Cristina Silva Lima (2018014565)

**Última Atualização:** 14.12.2023

---

## Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes bibliotecas instaladas em sua máquina. Caso contrário, você pode instalá-las executando o seguinte comando no prompt de comando:

```bash
pip install simple_pid numpy scipy socket opcua
```

# Instruções de execução
Primeiramente é necessário que o servidor <em>OPC<em> esteja ativo. Além disso, é importante que a porta do sistema esteja especificada. Neste projeto o endereço padrão do sistema está definido em <em>Variables.py<em>