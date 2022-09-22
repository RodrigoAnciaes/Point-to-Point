#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from distutils.log import error
from enlace import *
import time
import numpy as np
from util import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()

        ocioso = True
        while ocioso:
            print("esperando 1 byte de sacrifício")
            #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
            print("Abriu a comunicação")
        
            #txBuffer = b'\xFA'  #isso é um array de bytes
            if com1.rx.getIsEmpty() == False:  
                handshake_client =  get_separeted_package(com1)
                time.sleep(0.1)
                print(handshake_client)
                novo_n = handshake_client[0][3]
                print('dado recebido')
                if handshake_client[0][0] == 1:
                    print("Handshake recebido")
                    if handshake_client[0][5] == codigo_server: #É para mim?
                        ocioso = False
                        handshake_head[0] = [b'\x02']
                        my_handshake = create_package(handshake_head, b'\x00', end)
                        send_package(com1, my_handshake)
                        time.sleep(0.1)
                        print("Handshake enviado")
                else:
                    print("Handshake não recebido")

            time.sleep(1)


        #pack_n = get_separeted_package(com1)
        #print(pack_n)
        #n = pack_n[1][0]
        #print(n)
        #print("novo n recebido: ", novo_n)

        i = 1
        comandos_recebidos = []

        while i <= novo_n:
            prosseguir = False
            while prosseguir == False:
                com1.rx.clearBuffer()
                timer1 = time.time()
                timer2 = time.time()



                print("Recebendo pacote {0} de {1}".format(i, novo_n))
                package_received = get_separeted_package(com1)
                time.sleep(0.1)
                numero_pacote = package_received[0][4]
                print("Número do pacote recebido: {0}".format(numero_pacote))
                tamanho_pacote = package_received[0][5]
                print("Tamanho do pacote recebido: {0}".format(tamanho_pacote))
                len_body = len(package_received[1])

                if numero_pacote != i or len_body != tamanho_pacote: #retorna um erro
                    print("Erro no pacote {0}".format(i))
                    print("Pacote repetido ou com numeração incorreta")
                    print("Enviando pacote com o numero para o cliente".format(numero_pacote))
                    error_head[5] = b'\x04'
                    error_head[6] = i.to_bytes(1, byteorder='little')
                    error_head[7] = (i-1).to_bytes(1, byteorder='little')
                    error_package = create_package(error_head, b'\x00', end)
                    send_package(com1, error_package)
                    time.sleep(0.1)
                else:
                    print("Pacote certo recebido")
                    print("Enviando pacote enviando pacote com o numero para o cliente".format(numero_pacote))
                    ok_head[5] = [b'\x04']
                    ok_head[6] = (i).to_bytes(1, byteorder='little')
                    ok_head[7] = (i-1).to_bytes(1, byteorder='little')
                    ok_package = create_package(ok_head, b'\x00', end)
                    print("ok:",ok_package)
                    send_package(com1, ok_package)
                    time.sleep(0.1)
                    prosseguir = True
                    i += 1


#
                ##rxBuffer = package_received[1]
                ##nRx = package_received[4]
                ##time.sleep(.1)
                ##print("Recebeu {} bytes, no body".format(nRx))
                #print("Recebeu {}".format(package_received))
                #print('------------------------DIVISA----------------------------')
                #lista_comandos = rxBuffer.split()
                #for command in lista_comandos:
                #    if command != b'':
                #        print(command)
                #        comandos_recebidos.append(command)
                #    time.sleep(.1)
#
                #time.sleep(1)
                ##send a package with the number of received packages
                #
                #print("Enviando o número de pacotes recebidos")
                #print("Enviando {}".format(nRx))
                ##head[1] = tamanho do payload
                #head[5] = [b'\x04']
                #print("head1: {}".format(head[5]))
                #vpackage = create_package(head, [nRx], end)
                #print("vpackage: {}".format(vpackage))
                #send_package(com1, vpackage)
                #time.sleep(0.5)
                #print('-'*20)
                #print("Esperando confirmação para prosseguir")
                #confirmação = get_separeted_package(com1)                
                #if confirmação[0][0] == 4:
                #    print("Confirmação recebida")
                #    prosseguir = True
                #    i += 1
                #else:
                #    prosseguir = False
#
        #
#
    #
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        print("Comandos recebidos (Juntando os pacotes): ", comandos_recebidos)
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
