class ContaBancaria:
    # TODO: Inicialize a conta bancária com o nome do titular, saldo 0 e  liste para armazenar as operações realizadas:
    def __init__(self, nome_titular):
        self.nome_titular = nome_titular
        self.saldo = 0
        self.transacoes = []

    # TODO: Implemente o método para realizar um depósito, adicione o valor ao saldo e registre a operação:
    def depositar(self, valor):
        self.saldo += valor
        self.transacoes.append(f"+{valor}")
        return self.saldo

    # TODO: Implemente o método para realizar um saque:
    def sacar(self, valor):
        # TODO: Verifique se há saldo suficiente para o saque
        valor_positivo = abs(valor)
        if self.saldo >= valor_positivo:
            # TODO: Subtraia o valor do saldo (valor já é negativo)
            self.saldo += valor
            # TODO: Registre a operação e retorne a  mensagem de saque negado
            self.transacoes.append(f"{valor}")
            return self.saldo
        else:
            self.transacoes.append("Saque não permitido")    

    # TODO: Crie o método para exibir o extrato da conta e junte as operações no formato correto:
    def extrato(self):
        print(f"Operações: {', '.join(self.transacoes)}; Saldo: {self.saldo}")
        

nome_titular = input().strip()  
conta = ContaBancaria(nome_titular)  

entrada_transacoes = input().strip() 
transacoes = [int(valor) for valor in entrada_transacoes.split(",")]  

for valor in transacoes:
    if valor > 0:
        conta.depositar(valor)  
    else:
        conta.sacar(valor)  

conta.extrato()