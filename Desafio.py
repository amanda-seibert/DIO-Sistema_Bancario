saldo = 0
limite_saque = 500
numero_saques = 0
LIMITE_SAQUES = 3
extrato_bancario = []
usuarios = []
contas = []
agencia = "0001"

def menu():
    print("\n===== MENU =====")
    print("1. Cadastro de Usuário")
    print("2. Cadastro Conta Bancária")
    print("3. Depósito")
    print("4. Saque")
    print("5. Extrato")
    print("6. Buscar usuário")
    print("7. Listar usuários")
    print("8. Sair")
    print("================")
    return input("Escolha uma das opções acima: ")

def criar_usuario():
    while True:
        cpf = input("Nos informe o CPF (somente números): ")
        if cpf.isdigit():
            break
        else:
            print("CPF inválido. Por favor, insira somente números.")

    usuario_existente = next((usuario for usuario in usuarios if usuario['cpf'] == cpf), None)
    if usuario_existente:
        print("Operação inválida. Usuário já cadastrado com este CPF!")
        return

    while True:
        nome = input("Nos informe seu nome completo: ")
        if nome.replace(" ", "").isalpha():
            break
        else:
            print("Nome inválido. Por favor, insira apenas letras e espaços.")

    while True:
        data_nascimento = input("Nos informe sua data de nascimento (dd/mm/aaaa): ")
        if data_nascimento.replace("/", "").isdigit() and len(data_nascimento) == 10:
            break
        else:
            print("Data de nascimento inválida. Por favor, siga o formato dd/mm/aaaa e insira somente números.")

    endereco = input("Nos informe seu endereço (logradouro, n° - bairro - cidade/sigla estado): ")

    novo_usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }
    usuarios.append(novo_usuario)
    print("Usuário cadastrado com sucesso!")

def consultar_usuario():
    while True:
        cpf = input("Nos informe o CPF para consulta (somente números): ")
        if cpf.isdigit():
            break
        else:
            print("CPF inválido. Por favor, insira somente números.")

    while True:
        data_nascimento = input("Nos informe a data de nascimento (dd/mm/aaaa): ")
        if data_nascimento.replace("/", "").isdigit() and len(data_nascimento) == 10:
            break
        else:
            print("Data de nascimento inválida. Por favor, siga o formato dd/mm/aaaa e insira somente números.")

    usuario = next((usuario for usuario in usuarios if usuario['cpf'] == cpf and usuario['data_nascimento'] == data_nascimento), None)

    if usuario:
        print("\n==== Usuário encontrado! ====")
        print(f"Nome: {usuario['nome']}")
        print(f"Endereço: {usuario['endereco']}")

        contas_do_usuario = [conta for conta in contas if conta['cpf'] == cpf]
        if contas_do_usuario:
            print("\nContas Bancárias Ativas:")
            for conta in contas_do_usuario:
                print(f"Agência: {conta['agencia']}, Conta: {conta['numero']}")
        else:
            print("\nEste usuário não possui contas bancárias cadastradas!")
    else:
        print("Usuário não encontrado ou dados estão incorretos...")

def cadastrar_conta():
    cpf = input("Nos informe o CPF do usuário (somente números): ")
    usuario = next((usuario for usuario in usuarios if usuario['cpf'] == cpf), None)
    if not usuario:
        print("Usuário não encontrado. Por favor, cadastre o usuário primeiro.")
        return

    agencia = "0001"
    numero_conta = len(contas) + 1
    contas.append({
        "agencia": agencia,
        "numero": numero_conta,
        "cpf": cpf
    })

    print(f"Conta cadastrada com sucesso! Número da conta: {numero_conta}, Agência: {agencia}")

def listar_usuarios(agencia, usuarios, contas):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        print("\n===== LISTA DE USUÁRIOS =====")
        for usuario in usuarios:
            cpf = usuario['cpf']
            contas_do_usuario = [
                f"Conta: {conta['numero']} (Agência: {conta['agencia']})"
                for conta in contas
                if conta['cpf'] == cpf
            ]
            contas_str = ", ".join(contas_do_usuario) if contas_do_usuario else "Nenhuma conta bancária cadastrada."
            print(f"CPF: {cpf}, Nome: {usuario['nome']}, Contas: {contas_str}")
        print("=================================")

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ============")
    print("Nenhum depósito ou saque realizado." if not extrato else "\n".join(extrato))
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=====================================")

def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
    else:
        print("Operação falhou! O valor do depósito é inválido...")
    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    if numero_saques >= LIMITE_SAQUES:
        print("Operação não concluída! Você já atingiu o limite máximo de saques diários.")
        return saldo, extrato, numero_saques  
    elif valor <= 0:
        print("Valor inválido para saque. Por favor, insira um valor positivo.")
        return saldo, extrato, numero_saques  
    elif valor > saldo:
        print("Operação não concluída! O valor do saque excede o saldo disponível.")
        return saldo, extrato, numero_saques  
    elif valor > limite:
        print(f"Operação não concluída! O valor máximo para saque é de R$ {limite:.2f}.")
        return saldo, extrato, numero_saques 
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print(f"Saque realizado com sucesso! Você sacou R$ {valor:.2f} reais.")
        return saldo, extrato, numero_saques


def main():
    global saldo, numero_saques, extrato_bancario, agencia, LIMITE_SAQUES

    while True:
        opcao = menu()

        if opcao == "1":
            criar_usuario()

        elif opcao == "2":
            cadastrar_conta()

        elif opcao == "3":
            valor = float(input("Nos informe o valor do depósito: "))
            saldo, extrato_bancario = deposito(saldo, valor, extrato_bancario)
            print(f"Depósito realizado com sucesso! Você depositou R$ {valor:.2f} reais.")

        elif opcao == "4":
            valor = float(input("Nos informe o valor do saque: "))
            saldo, extrato_bancario, numero_saques = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato_bancario,
                limite=limite_saque,
                numero_saques=numero_saques,
                LIMITE_SAQUES=LIMITE_SAQUES
            )
            

        elif opcao == "5":
            exibir_extrato(saldo, extrato_bancario)

        elif opcao == "6":
            consultar_usuario()

        elif opcao == "7":
            listar_usuarios(agencia, usuarios, contas)

        elif opcao == "8":
            print("Saindo...")
            break

        else:
            print("Operação inválida! Por favor, selecione novamente a operação desejada.")

main()
