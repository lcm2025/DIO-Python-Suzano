def menu():
    print("\n" + "=" * 30)
    print("Bem-vindo ao Banco Python")
    print("=" * 30)
    print("1. Depositar")
    print("2. Sacar")
    print("3. Ver Extrato")
    print("4. Consultar Limite de Saque")
    print("5. Criar Novo Usuário")
    print("6. Criar Nova Conta")
    print("7. Listar Contas")
    print("8. Sair")
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

def consultar_limite(limite):
    print("\n" + "=" * 30)
    print("Consultar Limite de Saque")
    print("=" * 30)
    print(f"Seu limite atual de saque é: R$ {limite:.2f}")
    print("=" * 30)

def criar_usuario(usuarios):
    print("\n" + "=" * 30)
    print("Criar Novo Usuário")
    print("=" * 30)
    cpf = input("Digite o CPF (somente números): ")
    
    # Verifica se o CPF já está cadastrado
    if any(usuario["cpf"] == cpf for usuario in usuarios):
        print("CPF já cadastrado!")
        return usuarios
    
    nome = input("Digite o nome completo: ")
    data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Digite o endereço (logradouro, número - bairro - cidade/estado): ")
    
    # Adiciona o novo usuário à lista de usuários
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    
    print("Usuário criado com sucesso!")
    return usuarios

def criar_conta(contas, usuarios):
    print("\n" + "=" * 30)
    print("Criar Nova Conta")
    print("=" * 30)
    cpf = input("Digite o CPF do usuário (somente números): ")
    
    # Verifica se o usuário existe
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)
    if not usuario:
        print("Usuário não encontrado. Crie um usuário primeiro.")
        return contas
    
    # Gera o número da conta (sequencial simples)
    numero_conta = len(contas) + 1
    contas.append({
        "agencia": "0001",  # Agência imutável
        "numero_conta": numero_conta,
        "usuario": usuario
    })
    
    print(f"Conta criada com sucesso! Número da conta: {numero_conta}")
    return contas

def listar_contas(contas):
    print("\n" + "=" * 30)
    print("Listar Contas")
    print("=" * 30)
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print(f"Agência: {conta['agencia']} | Número da conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")
    print("=" * 30)

def main():
    saldo = 0
    limite = 500
    extrato_conta = []
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []  # Lista para armazenar usuários
    contas = []    # Lista para armazenar contas

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
            consultar_limite(limite)
        elif opcao == "5":
            usuarios = criar_usuario(usuarios)
        elif opcao == "6":
            contas = criar_conta(contas, usuarios)
        elif opcao == "7":
            listar_contas(contas)
        elif opcao == "8":
            print("Saindo... Obrigado por usar nosso banco!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
