menu = """

[d] Depositar na conta
[s] Sacar o dinheiro
[e] Extrato da conta
[k] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Nenhum depósito ou saque realizado." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

while True:
    opcao = input(menu)
   
    if opcao == "d":
        valor = float(input("Nos informe o valor do depósito:"))
        
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito realizado com sucesso! Você depositou R$ {valor:.2f} reais.")
        else:
            print("O valor do depósito é inválido.")
   
    elif opcao == "s":
        valor = float(input("Nos informe o valor do saque:"))
        
        verifica_valor = valor <= 0
        verifica_saldo = saldo < valor
        verifica_saque = numero_saques >= LIMITE_SAQUES
        
        if verifica_valor:
            print("O valor do saque é inválido.")
        elif verifica_saldo:
            print("Seu saldo é insuficiente.")
        elif verifica_saque:
            print("Ação não concluída! Número máximo de saques excedido.")
        elif valor > limite:
            print("Ação não concluída! O valor do saque excede o limite.")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"Saque realizado com sucesso! Você sacou R$ {valor:.2f} reais.")
   
    elif opcao == "e":
        exibir_extrato(saldo, extrato)
   
    elif opcao == "k":
        print("Você saiu da conta.")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

      

      


    
      

      

   
