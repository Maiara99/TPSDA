def velocimetro(valor):
    # Verificar se o valor está no intervalo permitido
    if 0 <= valor <= 100:
        # Calcular a quantidade de underlines a serem substituídos por #
        num_underlines = round(valor/100*10)

        # Formatar a string
        string_formatada = f"[{'#' * num_underlines}{'_' * (10 - num_underlines)}] {valor}"

        # Imprimir a string formatada
        print(string_formatada)
    else:
        print("Alerta, velocidade muito alta")

velocimetro(10)