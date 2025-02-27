class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    def __str__(self):
        return f"Nome: {self.nome}, CPF: {self.cpf}"


class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.extrato_conta = []
        self.limite = 500
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato_conta.append(f"Depósito: R$ {valor:.2f}")
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Valor inválido para depósito.")

    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente.")
        elif valor > self.limite:
            print(f"Valor excede o limite de R$ {self.limite:.2f} por saque.")
        elif self.numero_saques >= self.LIMITE_SAQUES:
            print("Limite diário de saques atingido.")
        elif valor > 0:
            self.saldo -= valor
            self.numero_saques += 1
            self.extrato_conta.append(f"Saque: R$ {valor:.2f}")
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Valor inválido para saque.")
    
    def consultar_limite(self):
        print("\n" + "=" * 30)
        print("Consultar Limite de Saque")
        print("=" * 30)
        print(f"Seu limite atual de saque é: {self.LIMITE_SAQUES} e você já sacou: {self.numero_saques}")
        print("=" * 30)

    def ver_extrato(self):
        print("\n" + "=" * 30)
        print(f"Extrato da Conta {self.numero_conta}")
        print(f"Titular: {self.usuario.nome}")
        print("=" * 30)
        if not self.extrato_conta:
            print("Não foram realizadas movimentações.")
        else:
            for movimento in self.extrato_conta:
                print(movimento)
        print(f"\nSaldo atual: R$ {self.saldo:.2f}")
        print("=" * 30)

    def __str__(self):
        return f"Agência: {self.agencia} | Número da conta: {self.numero_conta} | Titular: {self.usuario.nome}"
    
class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def criar_usuario(self):
        print("\n" + "=" * 30)
        print("Criar Novo Usuário")
        print("=" * 30)
        cpf = input("Digite o CPF (somente números): ")

        # Verifica se o CPF já está cadastrado
        if any(usuario.cpf == cpf for usuario in self.usuarios):
            print("CPF já cadastrado!")
            return

        nome = input("Digite o nome completo: ")
        data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Digite o endereço (logradouro, número - bairro - cidade/estado): ")

        # Adiciona o novo usuário à lista de usuários
        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(novo_usuario)
        print("Usuário criado com sucesso!")

    def criar_conta(self):
        print("\n" + "=" * 30)
        print("Criar Nova Conta")
        print("=" * 30)
        cpf = input("Digite o CPF do usuário (somente números): ")

        # Verifica se o usuário existe
        usuario = next((usuario for usuario in self.usuarios if usuario.cpf == cpf), None)
        if not usuario:
            print("Usuário não encontrado. Crie um usuário primeiro.")
            return

        # Gera o número da conta (sequencial simples)
        numero_conta = len(self.contas) + 1
        nova_conta = Conta("0001", numero_conta, usuario)
        self.contas.append(nova_conta)
        print(f"Conta criada com sucesso! Número da conta: {numero_conta}")

    def listar_contas(self):
        print("\n" + "=" * 30)
        print("Listar Contas")
        print("=" * 30)
        if not self.contas:
            print("Nenhuma conta cadastrada.")
        else:
            for conta in self.contas:
                print(conta)
        print("=" * 30)

    def depositar(self):
        print("\n" + "=" * 30)
        print("Depósito")
        print("=" * 30)
        cpf = input("Digite o CPF do usuário (somente números): ")

        # Verifica se o usuário existe
        usuario = next((usuario for usuario in self.usuarios if usuario.cpf == cpf), None)
        if not usuario:
            print("Usuário não encontrado.")
            return

        # Lista as contas associadas ao usuário
        contas_usuario = [conta for conta in self.contas if conta.usuario.cpf == cpf]
        if not contas_usuario:
            print("Nenhuma conta encontrada para este usuário.")
            return

        print("\nContas associadas a este usuário:")
        for i, conta in enumerate(contas_usuario):
            print(f"{i + 1}. Agência: {conta.agencia} | Número da conta: {conta.numero_conta}")

        # Solicita que o usuário escolha uma conta
        try:
            escolha = int(input("Escolha o número da conta para depósito: ")) - 1
            if escolha < 0 or escolha >= len(contas_usuario):
                print("Escolha inválida. Digite um número correspondente a uma das contas listadas.")
                return
        except ValueError:
            print("Entrada inválida. Digite um número.")
            return

        conta_escolhida = contas_usuario[escolha]

        # Realiza o depósito
        valor = float(input("Digite o valor a depositar: "))
        conta_escolhida.depositar(valor)

    def ver_extrato(self):
        print("\n" + "=" * 30)
        print("Extrato")
        print("=" * 30)
        cpf = input("Digite o CPF do usuário (somente números): ")

        # Verifica se o usuário existe
        usuario = next((usuario for usuario in self.usuarios if usuario.cpf == cpf), None)
        if not usuario:
            print("Usuário não encontrado.")
            return

        # Lista as contas associadas ao usuário
        contas_usuario = [conta for conta in self.contas if conta.usuario.cpf == cpf]
        if not contas_usuario:
            print("Nenhuma conta encontrada para este usuário.")
            return

        print("\nContas associadas a este usuário:")
        for i, conta in enumerate(contas_usuario):
            print(f"{i + 1}. Agência: {conta.agencia} | Número da conta: {conta.numero_conta}")

        # Solicita que o usuário escolha uma conta
        try:
            escolha = int(input("Escolha o número da conta para ver o extrato: ")) - 1
            if escolha < 0 or escolha >= len(contas_usuario):
                print("Escolha inválida. Digite um número correspondente a uma das contas listadas.")
                return
        except ValueError:
            print("Entrada inválida. Digite um número.")
            return

        conta_escolhida = contas_usuario[escolha]

        # Exibe o extrato da conta escolhida
        conta_escolhida.ver_extrato()

    def consultar_limite(self):
        print("\n" + "=" * 30)
        print("LIMITE DE SAQUES")
        print("=" * 30)
        cpf = input("Digite o CPF do usuário (somente números): ")

        # Verifica se o usuário existe
        usuario = next((usuario for usuario in self.usuarios if usuario.cpf == cpf), None)
        if not usuario:
            print("Usuário não encontrado.")
            return

        # Lista as contas associadas ao usuário
        contas_usuario = [conta for conta in self.contas if conta.usuario.cpf == cpf]
        if not contas_usuario:
            print("Nenhuma conta encontrada para este usuário.")
            return

        print("\nContas associadas a este usuário:")
        for i, conta in enumerate(contas_usuario):
            print(f"{i + 1}. Agência: {conta.agencia} | Número da conta: {conta.numero_conta}")

        # Solicita que o usuário escolha uma conta
        try:
            escolha = int(input("Escolha o número da conta para ver o extrato: ")) - 1
            if escolha < 0 or escolha >= len(contas_usuario):
                print("Escolha inválida. Digite um número correspondente a uma das contas listadas.")
                return
        except ValueError:
            print("Entrada inválida. Digite um número.")
            return

        conta_escolhida = contas_usuario[escolha]

        # Exibe quantos saques ainda podem ser realizados no dia
        conta_escolhida.consultar_limite()

    def sacar(self):
        print("\n" + "=" * 30)
        print("SAQUE")
        print("=" * 30)
        cpf = input("Digite o CPF do usuário (somente números): ")

        # Verifica se o usuário existe
        usuario = next((usuario for usuario in self.usuarios if usuario.cpf == cpf), None)
        if not usuario:
            print("Usuário não encontrado.")
            return

        # Lista as contas associadas ao usuário
        contas_usuario = [conta for conta in self.contas if conta.usuario.cpf == cpf]
        if not contas_usuario:
            print("Nenhuma conta encontrada para este usuário.")
            return

        print("\nContas associadas a este usuário:")
        for i, conta in enumerate(contas_usuario):
            print(f"{i + 1}. Agência: {conta.agencia} | Número da conta: {conta.numero_conta}")

        # Solicita que o usuário escolha uma conta
        try:
            escolha = int(input("Escolha o número da conta para depósito: ")) - 1
            if escolha < 0 or escolha >= len(contas_usuario):
                print("Escolha inválida. Digite um número correspondente a uma das contas listadas.")
                return
        except ValueError:
            print("Entrada inválida. Digite um número.")
            return

        conta_escolhida = contas_usuario[escolha]

        # Realiza o saque
        valor = float(input("Digite o valor a sacar: "))
        conta_escolhida.sacar(valor)

    def menu(self):
        print("\n" + "=" * 30)
        print("Bem-vindo ao Banco LCM")
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

    def main(self):
        while True:
            self.menu()
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.depositar()
            elif opcao == "2":
                self.sacar()
            elif opcao == "3":
                self.ver_extrato()
            elif opcao == "4":
                self.consultar_limite()
            elif opcao == "5":
                self.criar_usuario()
            elif opcao == "6":
                self.criar_conta()
            elif opcao == "7":
                self.listar_contas()
            elif opcao == "8":
                print("Saindo... Obrigado por usar nosso banco!")
                break
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    banco = Banco()
    banco.main()