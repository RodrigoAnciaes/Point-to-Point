#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


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
serialName = "COM4"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
    
        #txBuffer = b'\xFA'  #isso é um array de bytes

        handshake_client =  get_separeted_package(com1)
        print('dado recebido')
        if handshake_client[0][1] == 255:
            print("Handshake recebido")
            print(handshake_client)
            my_handshake = create_package(handshake_head, b'\x00', end)
            send_package(com1, my_handshake)
            print("Handshake enviado")
        else:
            print("Handshake não recebido")
            com1.disable()
            exit()

        pack_n = get_separeted_package(com1)
        print(pack_n)
        n = pack_n[1][1]
        print(n)
        i = 0

        comandos_recebidos = []
        numero_anterior = -1


        while i < n:
            prosseguir = False
            while prosseguir == False:
                com1.rx.clearBuffer()
                print("Recebendo pacote {0}".format(i))
                package_received = get_separeted_package(com1)
                numero_pacote = package_received[0][5]
                print("Número do pacote recebido: {0}".format(numero_pacote))

                if numero_pacote != i: #retorna um erro
                    print("Erro no pacote {0}".format(numero_pacote))
                    print("Pacote repetido ou com numeração incorreta")
                    print("Enviando pacote com o numero para o cliente".format(numero_pacote))
                    error_package = create_package(error_head, b'\x00', end)
                    send_package(com1, error_package)
                else:
                    print("Pacote certo recebido")
                    print("Enviando pacote enviando pacote com o numero para o cliente".format(numero_pacote))
                    ok_package = create_package(ok_head, b'\x00', end)
                    send_package(com1, ok_package)

                rxBuffer = package_received[1]
                nRx = package_received[4]
                time.sleep(.1)
                print("Recebeu {} bytes, no body".format(nRx))
                print("Recebeu {}".format(package_received))
                print('------------------------DIVISA----------------------------')
                lista_comandos = (rxBuffer.split(b'\xCC'))
                for command in lista_comandos:
                    if command != b'':
                        print(command)
                        comandos_recebidos.append(command)
                    time.sleep(.1)

                time.sleep(1)
                time.sleep(0.5)
                #send a package with the number of received packages
                
                print("Enviando o número de pacotes recebidos")
                print("Enviando {}".format(nRx))
                #head[1] = tamanho do payload
                head[1] = [b'\x05']
                print("head1: {}".format(head[1]))
                vpackage = create_package(head, [nRx], end)
                send_package(com1, vpackage)
                time.sleep(0.5)
                print('-'*20)
                print("Esperando confirmação para prosseguir")
                confirmação = get_separeted_package(com1)
                print("Confirmação recebida")
                if confirmação[0][1] == 251:
                    print("Confirmação recebida")
                    prosseguir = True
                    i += 1
                else:
                    prosseguir = False

        

    
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
