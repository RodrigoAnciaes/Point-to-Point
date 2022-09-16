#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
#####################################################
from enlace import *
import time
import numpy as np
from random import randint
from util import *
from enlaceRx import *

serialName = "COM5"

COMANDOS = [b'\x00\xFA\x00\x00', #1
            b'\x00\x00\xFA\x00', #2
            b'\xFA\x00\x00', #3
            b'\x00\xFA\x00', #4
            b'\x00\x00\xFA', #5
            b'\x00\xFA', #6
            b'\xFA\x00', #7
            b'\x00', #8
            b'\xFA'] #9



print("#"*100)

comando = []
total_size = 0
for i in range(randint(10, 30)):
    k = randint(0, 8)
    comando.append(COMANDOS[k])
div_list = split_In_lists(comando, int(len(comando)/5))
n = 0
lista_listas = []
for i in div_list:
    print("Lista: {0}".format(i))
    lista_listas.append(i)
    n += 1
print("n: {0}".format(n))

total_size = len(comando)
for c in comando:
    total_size += len(c)

def main():
    try:
        com1 = enlace(serialName)
        com1.enable()
        time.sleep(1)
        print("Abriu a comunicação")
        
        com1.rx.clearBuffer()
        handshake_recebido = False
        while not handshake_recebido:
            com1.sendData(b'00')
            time.sleep(0.1)
            handshake = create_package(handshake_head, b'\x00', end)
            handshake[5] = 128
            print("handshake: {0}".format(handshake))
            send_package(com1, handshake)
            time.sleep(5)

            if com1.rx.getIsEmpty() == False:
                response = get_separeted_package(com1)
                if response[0][0] == 255:
                    print("Handshake recebido")
                    handshake_recebido = True
                time.sleep(0.2)
            else:
                print("Handshake não recebido")
                com1.rx.clearBuffer()

        #send a package with n as payload
        print("Enviando o tamanho")
        head[5] = [b'\x04']
        package = create_package(head,[n], end)
        print("Package: {0}".format(package))
        send_package(com1, package)
        time.sleep(0.1)

        cont = 1
        for i in lista_listas:
            print("Enviando pacote {0}".format(cont))
            pacote_enviado_com_sucesso = False
            numero_certo = False
            tamanho_certo = False
            while pacote_enviado_com_sucesso == False:
                print("Enviando comando")
                total_size = 0
                for c in i:
                    total_size += len(c)
                #send the command to the server
                head[5] = tamanho_real(total_size).to_bytes(1, byteorder='little')
                head[4] = cont.to_bytes(1, byteorder='little')
                #time.sleep(.1)
                print(i)
                package = create_package(head, i, end)
                print(package)
                send_package(com1, package)
                print("Enviou os dados")

                #get the response from the server
                response = get_separeted_package(com1)
                print("Recebeu a resposta")
                if response[0][0] == 251:
                    print("tudo certo")
                    numero_certo = True
                else:
                    print("numero errado")
                    print(response[0])
                    print(response[0][0])
                    numero_certo = False
                

                #com1.sendData(np.asarray(txBuffer))  
                while com1.tx.getStatus() == 0:
                    txSize = com1.tx.getStatus() 
                
                time.sleep(.1)
                
                print("ENVIADOS {} bytes, {}".format(total_size, hex(total_size)))
                print(f"TAMANHO LEN COMANDOS: {len(i)}")
                print(f"Lista bytes: {i}")

                verification = get_separeted_package(com1)
                ttotal = verification[1].strip(b'\x00\x00\x00')
                print("verificação recebida: {0}".format(verification))
                print("Recebeu {} bytes".format(ttotal))
                print("Recebido: {} bytes".format(int.from_bytes(ttotal, byteorder='big')))

                if int.from_bytes(ttotal, byteorder='big') != tamanho_real(total_size):
                    print("O número de bytes recebidos não é igual ao número de bytes enviados")
                    erro_package = create_package(error_head, b'\x00', end)
                    send_package(com1, erro_package)
                else:
                    print("O número de bytes recebidos é igual ao número de bytes enviados")
                    ok_package = create_package(ok_head, b'\x00', end)
                    send_package(com1, ok_package)
                    tamanho_certo = True
                time.sleep(0.2)
                print("numero do pacote cuja operação foi realizada",cont)
                print("☺"*100)
                print(numero_certo, tamanho_certo)
                if numero_certo == True and tamanho_certo == True:
                    pacote_enviado_com_sucesso = True
                    cont += 1
                else:
                    pacote_enviado_com_sucesso = False
            
        print("Fechando a comunicação")
        com1.disable()


    except Exception as erro:
        print(erro)
        com1.disable()
        
if __name__ == "__main__":
    main()
