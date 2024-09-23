import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if not conta.pode_realizar_transacao():
            print("\n--- Operação não concluída! Você já atingiu o limite máximo de saques diários! ---")
            return
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._agencia = "0001"
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def pode_realizar_transacao(self):
        transacoes_hoje = self.historico.transacoes_do_dia()
        return len(transacoes_hoje) < 10

    def sacar(self, valor):
        if not self.pode_realizar_transacao():
            return False
        if valor > self.saldo:
            print("\n--- Operação não concluída! O valor do saque excede o saldo disponível. ---")
            return False
        if valor > 0:
            self._saldo -= valor
            print("\n*** Saque realizado com sucesso! ***")
            return True
        print("\n--- Operação não concluída! O valor informado é inválido. ---")
        return False

    def depositar(self, valor):
        if not self.pode_realizar_transacao():
            return False
        if valor > 0:
            self._saldo += valor
            print("\n*** Depósito realizado com sucesso! ***")
            return True
        print("\n--- Operação falhou! O valor do depósito é inválido... ---")
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500):
        super().__init__(numero, cliente)
        self._limite = limite

    def sacar(self, valor):
        if valor > self._limite:
            print("\n--- Operação falhou! O valor do saque excede o limite. ---")
            return False
        return super().sacar(valor)

    def __str__(self):
        return f"""\ 
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def transacoes_do_dia(self):
        hoje = datetime.now().strftime("%d-%m-%Y")
        return [transacao for transacao in self._transacoes if transacao["data"].startswith(hoje)]

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """\n
    ***************= MENU =***************
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNovo Cliente
    [5]\tNova Conta
    [6]\tListar Contas
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n--- Este usuário não possui contas bancárias cadastradas! ---")
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]

    print("\n--- Selecione a conta ---")
    for index, conta in enumerate(cliente.contas, start=1):
        print(f"[{index}] Conta número: {conta.numero} - Agência: {conta.agencia}")
    while True:
        opcao = input("Escolha o número da conta: ")
        try:
            indice = int(opcao) - 1
            if 0 <= indice < len(cliente.contas):
                return cliente.contas[indice]
            else:
                print("\n--- Opção inválida! Por favor, tente novamente. ---")
        except ValueError:
            print("\n--- Entrada inválida, por favor insira um número. ---")

def validar_cpf(cpf):
    if len(cpf) == 11 and cpf.isdigit():
        return True
    print("\n--- Usuário não encontrado ou dados estão incorretos...---")
    return False

def validar_data_nascimento(data_nascimento):
    try:
        datetime.strptime(data_nascimento, "%d/%m/%Y")
        return True
    except ValueError:
        print("\n--- Data de nascimento inválida! Use o formato DD/MM/AAAA. ---")
        return False

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n--- Usuário não encontrado ou dados estão incorretos... ---")
        return
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n--- Cliente não encontrado! ---")
        return
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n--- Cliente não encontrado! ---")
        return
    conta = recuperar_conta_cliente(cliente)
    if conta:
        print("\n***************= EXTRATO =***************")
        transacoes = conta.historico.transacoes
        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\n\tData: {transacao['data']}"
        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("******************************************")

def criar_cliente(clientes):
    while True:
        cpf = input("Informe o CPF (somente número): ")
        if validar_cpf(cpf):
            break
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\n--- Já existe cliente com esse CPF! ---")
        return
    nome = input("Informe o nome completo: ")
    while True:
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        if validar_data_nascimento(data_nascimento):
            break
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade-sigla estado): ")
    novo_cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(novo_cliente)
    print("\n*** Cliente criado com sucesso! ***")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n--- Usuário não encontrado, encerrando acesso. Tente novamente ---")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n*** Conta criada com sucesso! ***")

def listar_contas(contas):
    if not contas:
        print("\n--- Nenhuma conta cadastrada! ---")
        return

    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()
        if opcao == "1":
            depositar(clientes)
        elif opcao == "2":
            sacar(clientes)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            criar_cliente(clientes)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "0":
            print("\n--- Saindo do sistema. ---")
            break
        else:
            print("\n--- Operação inválida, por favor selecione novamente a operação desejada. ---")

if __name__ == "__main__":
    main()
