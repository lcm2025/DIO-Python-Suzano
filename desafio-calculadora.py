def menu():
    print("\n" + "=" * 30)
    print("Bem-vindo ao Banco Python")
    print("=" * 30)
    print("1. Depositar")
    print("2. Sacar")
    print("3. Ver Extrato")
    print("4. Sair")
    print("=" * 30)

def deposito(saldo):
    print("\n" + "=" * 30)
    print("Depósito")
    print("=" * 30)
    valor = float(input("Digite o valor a depositar: "))
    if valor > 0:
        saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor inválido para depósito.")
    return saldo, valor  # Retorna o saldo atual e o valor do depósito

def saque(saldo, limite, numero_saques, LIMITE_SAQUES):
    print("\n" + "=" * 30)
    print("Saque")
    print("=" * 30)
    valor = float(input("Digite o valor a sacar: "))

    if valor > saldo:
        print("Saldo insuficiente.")
    elif valor > limite:
        print(f"Valor excede o limite de R$ {limite:.2f} por saque.")
    elif numero_saques >= LIMITE_SAQUES:
        print("Limite diário de saques atingido.")
    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor inválido para saque.")

    return saldo, numero_saques, valor  # Retorna o saldo atual, número de saques e o valor do saque

def extrato(saldo, extrato_conta):
    print("\n" + "=" * 30)
    print("Extrato")
    print("=" * 30)
    if not extrato_conta:
        print("Não foram realizadas movimentações.")
    else:
        for movimento in extrato_conta:
            print(movimento)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=" * 30)

def main():
    saldo = 0
    limite = 500
    extrato_conta = []
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            saldo, valor_deposito = deposito(saldo)
            extrato_conta.append(f"Depósito: R$ {valor_deposito:.2f}")  # Adiciona o valor do depósito ao extrato
        elif opcao == "2":
            saldo, numero_saques, valor_saque = saque(saldo, limite, numero_saques, LIMITE_SAQUES)
            extrato_conta.append(f"Saque: R$ {valor_saque:.2f}")  # Adiciona o valor do saque ao extrato
        elif opcao == "3":
            extrato(saldo, extrato_conta)
        elif opcao == "4":
            print("Saindo... Obrigado por usar nosso banco!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
