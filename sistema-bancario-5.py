import sqlite3
from pathlib import Path

# Definir o caminho do banco de dados
ROOT_PATH = Path(__file__).parent
conexao = sqlite3.connect(ROOT_PATH / "banco_lcm.sqlite")
cursor = conexao.cursor()

# Ativar o suporte a FK no SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# Criando as tabelas do banco
cursor.execute(
    "CREATE TABLE IF NOT EXISTS clientes ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "nome_user TEXT, "
    "cpf TEXT UNIQUE NOT NULL)"
)
conexao.commit()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS conta ("
    "num_conta INTEGER PRIMARY KEY AUTOINCREMENT, "
    "cpf TEXT NOT NULL, "
    "saldo REAL DEFAULT 0, "
    "FOREIGN KEY (cpf) REFERENCES clientes(cpf) ON DELETE CASCADE)"
)
conexao.commit()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS historico ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "num_conta INTEGER, "
    "operacao TEXT, "
    "valor REAL,"
    "data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "FOREIGN KEY (num_conta) REFERENCES conta(num_conta))" 
)
conexao.commit()

# Fechando a conexão com o banco de dados
#conexao.close()

class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        
    def __str__(self):
        return f"nome {self.nome}, CPF: {self.cpf}"

# classe conta onde são realizadas as operações
class Conta:
    def __init__(self, num_conta, usuario, saldo=0):
        self.num_conta = num_conta
        self.usuario = usuario
        self.LIMITE_NUM_SAQUE = 3
        self.limite_saque = 500
        self.saldo = saldo  
        self.numero_saque = 0
        
    def sacar(self, conexao, cursor, valor):
        self.valor = valor
        cursor.execute("SELECT saldo FROM conta WHERE num_conta=?", (self.num_conta,))
        resultado = cursor.fetchone()
        saldo_atual = resultado[0]
        if self.valor > saldo_atual:
            print("\n" + "=" * 30)
            print("Saldo insuficiente")
        elif self.valor > self.limite_saque:
            print("\n" + "=" * 30)
            print("Valor maior do que permitido para saque")
        elif self.numero_saque >= self.LIMITE_NUM_SAQUE:
            print("\n" + "=" * 30)
            print("Numeros máximos de saque diários atingido")
        elif self.valor > 0:
            novo_saldo = saldo_atual - self.valor
            cursor.execute(
                "UPDATE conta SET saldo =?"
                "WHERE num_conta=?", (novo_saldo, self.num_conta)
            )
            conexao.commit()
            self.numero_saque += 1
            operacao = f"Saque realizado no valor de R$: {self.valor: .2f}"
            cursor.execute(
                "INSERT INTO historico (num_conta, operacao, valor)"
                "VALUES (?, ?, ?)", (self.num_conta, operacao, self.valor)
            )
            conexao.commit()
        else:
            print("Valor inválido para saque!")

    
    def depositar(self, conexao, cursor, valor):
        self.valor = valor
        if valor <= 0:
            print("Informe o valor válido para o depósito!")
            return
        # Buscar saldo atual da conta no banco
        cursor.execute("SELECT saldo from conta WHERE num_conta=?", (self.num_conta,))
        resultado = cursor.fetchone()

        if resultado is None:
            print("Conta não encontrada!")
            return
        saldo_atual = resultado[0]
        novo_saldo = saldo_atual + self.valor
        
        # Atualizar o saldo no banco
        cursor.execute(
            "UPDATE conta SET saldo =?"
            "WHERE num_conta=?", (novo_saldo, self.num_conta)
            )
        conexao.commit()

        print(f"Deposito de R$: {self.valor: .2f} realizado")
        operacao = f"Deposito realizado no valor de R$: {valor: .2f}"
        cursor.execute(
            "INSERT INTO historico (num_conta, operacao, valor)"
            "VALUES (?, ?, ?)", (self.num_conta, operacao, self.valor)
            )
        conexao.commit()

    def exibir_extrato(self):
        pass
# Classe onde será feita a validação de usuários e contas e chamada de operações
class Banco:
    def __init__(self):
        self.conexao = sqlite3.connect(ROOT_PATH / "banco_lcm.sqlite")
        self.cursor = self.conexao.cursor()

    def criar_cliente(self):
        print("\n" + "=" * 30)
        print("Criar novo cliente")
        print("\n" + "=" * 30)
        cpf = input("Digite o cpf do Cliente: ")
        if self.buscar_cpf(cpf):
            print("CPF já cadastrado, favor conferir o CPF informado.")
            return
        nome = input("Digite o nome do Cliente: ")
        cursor.execute(
            "INSERT INTO clientes (nome_user, cpf)"
            "VALUES (?,?)", (nome, cpf)
        )
        conexao.commit()
        print("Novo Cliente criado")
            
    def criar_conta(self):
        print("\n" + "=" * 30)
        print("Criar nova conta")
        print("\n" + "=" * 30)
        conta_cpf = input("Digite o cpf do Cliente: ")

        if not self.buscar_cpf(conta_cpf):
            print("CPF inválido, favor informar um CPF existente.")
            return
        
        cursor.execute(
            "INSERT INTO conta (cpf)"
            "VALUES (?)", (conta_cpf,)
        )
        conexao.commit()

# Obtendo o número da conta criada
        cursor.execute("SELECT last_insert_rowid()")
        num_conta = cursor.fetchone()[0]

        print(f"Conta criada com sucesso! Números da Conta: {num_conta}")


    def buscar_cpf(self, cpf):
        cursor.execute("SELECT cpf FROM clientes WHERE cpf=?", (cpf,))
        return cursor.fetchone() is not None
    
    def buscar_conta(self, num_conta):
        cursor.execute("SELECT num_conta, cpf, saldo FROM conta WHERE num_conta=?", (num_conta,))
        return cursor.fetchone()

    def depositos(self):
        print("\n" + "=" * 30)
        print("Depósito")
        print("\n" + "=" * 30)
        cpf_cliente = input("Digite o seu CPF (Somente números): ")
        if not self.buscar_cpf(cpf_cliente):
            print("Cliente não encontrado. Verifique o CPF e tente novamente.")
            return
        
        num_conta = input("Informe a conta que irá receber o depósito: ")
        conta_info = self.buscar_conta(num_conta)

        if not conta_info:
            print("Conta não encontrada")
            return
        
        num_conta, cpf, saldo = conta_info
        
        try:
            valor = float(input("Digite o valor a ser depositado: "))
            if valor <= 0:
                print("Valor inválido! Informe um valor maior que zero.")
                return
        except ValueError:
            print("Valor inválido! Digite um número válido.")
            return
        conta = Conta(num_conta, cpf, saldo)
        conta.depositar(self.conexao, self.cursor, valor)

    def saque(self):
        print("\n" + "=" * 30)
        print("SAQUE")
        print("\n" + "=" * 30)
        cpf_cliente = input("Digite o seu CPF (Somente números): ")
        if not self.buscar_cpf(cpf_cliente):
            print("Cliente não encontrado. Verifique o CPF e tente novamente.")
            return

        num_conta = input("Informe o número da conta que sera realizado o saque: ")
        conta_info = self.buscar_conta(num_conta)
        if not conta_info:
            print("Conta não encontrada.")
            return
        
        num_conta, cpf, saldo = conta_info
        valor = float(input("Informa o valor para saque: "))
        conta = Conta(num_conta, cpf, saldo)
        conta.sacar(self.conexao, self.cursor, valor)
    
    def extrato(self):
        pass

    def menu(self):
        print("\n" + "=" * 30)
        print("Bem vindo ao nosso banco")
        print("=" * 30)
        print("1 - Depositar")
        print("2 - Sacar")
        print("3 - Ver Extrato")
        print("4 - Criar novo cliente")
        print("5 - Criar nova conta")
        print("6 - Sair")

    def main(self):
        while True:
            self.menu()
            opcao = input("Escolha uma opção: ")
            conexao = sqlite3.connect(ROOT_PATH / "banco_lcm.sqlite")
            cursor = conexao.cursor()
            if opcao == "1":
                self.depositos()
            elif opcao == "2":
                self.saque()
            elif opcao == "3":
                self.extrato()
            elif opcao == "4":
                self.criar_cliente()
            elif opcao == "5":
                self.criar_conta()
            elif opcao == "6":
                print("Saindo do sistema")
                conexao.close()
                break
            else:
                print("Opção inválida, favor selecionar uma opção válida.")

    def fechar_conexão(self):
        self.conexao.close()
        print("Conexão com o banco fechada.")


if __name__ == "__main__":
   banco = Banco()
   banco.main()


