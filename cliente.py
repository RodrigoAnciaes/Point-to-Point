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

serialName = "COM4"

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
        com1.sendData(b'00')
        time.sleep(0.1)
        handshake_head[3] = n.to_bytes(1, byteorder='big')
        com1.rx.clearBuffer()
        handshake_recebido = False
        while not handshake_recebido:
            handshake = create_package(handshake_head, b'\x00', end)
            send_package(com1, handshake)
            time.sleep(5)

            if com1.rx.getIsEmpty() == False:
                response = get_separeted_package(com1)
                print("response: ",response)
                if response[0][0] == 2:
                    print("Handshake recebido\n\n")
                    handshake_recebido = True
                time.sleep(0.2)
            else:
                print("Handshake não recebido")
                com1.rx.clearBuffer()

        cont = 1
        for i in lista_listas:
            print("Enviando pacote {0}".format(cont))
            
            response = [[]]
            pacote_enviado_com_sucesso = False
            numero_certo = False
            while pacote_enviado_com_sucesso == False:
                print("Enviando comando")
                time.sleep(.1)
                total_size = 0
                for c in i:
                    total_size += len(c)
                head[5] = total_size.to_bytes(1, byteorder='little')
                head[4] = cont.to_bytes(1, byteorder='little')
                head[3] = n.to_bytes(1, byteorder='big')
                head[0] = b"\x03"
                package = create_package(head, i, end)
                print(package)
                send_package(com1, package)
                timer1 = time.time() #timer de reenvio 
                timer2 = time.time() #timer timeout
                print("Enviou os dados")
                time.sleep(0.2)

                if com1.rx.getIsEmpty() == False:
                    response = get_separeted_package(com1) #ESSA DEVE SER A MSG T4 
                    print("Recebeu a resposta: {0}".format(response))
                    if response[0][0] == 4: #DEVE SER USADO PARA CONFIRMAR SE O PACOTE FOI RECEBIDO COM SUCESSO
                        print("tudo certo")
                        print("response: ",response)
                        pacote_enviado_com_sucesso = True
                        numero_certo = True
                    elif response[0][0] == 6:
                        print("numero errado")
                        print(response[0])
                        numero_certo = False
                else:
                    print("????????????????? Não recebeu a resposta")
        
                time.sleep(.5)
                #LOOP PARA TRATAR ERROS 
                while numero_certo == False:
                    
                    if time.time() - timer1 > 5:
                        print("Enviando comando novamente")
                        time.sleep(.1)
                        print(i)
                        package = create_package(head, i, end)
                        print(package)
                        send_package(com1, package)
                        timer1 = time.time()
                    if time.time() - timer2 > 20:
                        #ENVIA MSG T5
                        head[0] = b"\x05"
                        package = create_package(head, b'\x00', end)
                        send_package(com1, package)
                        print("Timeout :-(")
                        com1.disable()
                        break
                    if com1.rx.getIsEmpty() == False:
                        response1 = get_separeted_package(com1)
                    if response1[0][0] == 6:
                        print("numero errado1")
                        package = create_package(head, i, end)
                        send_package(com1, package)
                        timer1 = time.time() 
                        timer2 = time.time()
                        
                cont += 1
                time.sleep(0.4)
            
        print("Fechando a comunicação")
        com1.disable()


    except Exception as erro:
        print(erro)
        com1.disable()
        
if __name__ == "__main__":
    main()
