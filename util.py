import time
from turtle import pen
import numpy as np

handshake_head = [b'\x01',b'\x00',b'\x00',b'\x01',b'\x00',b'\x80', b'\x00', b'\x00', b'\x00', b'\x00']
head3 = [b'\x02',b'\x00',b'\x00',b'\x00',b'\x00', b'\x00',b'\x00',b'\x00',b'\x00',b'\x00']
error_head = [b'\xFA',b'\x04',b'\x00',b'\x00',b'\x00', b'\x04',b'\x00',b'\x00',b'\x00',b'\x00']
ok_head = [b'\xFB',b'\x04',b'\x00',b'\x00',b'\x00', b'\x04',b'\x00',b'\x00',b'\x00',b'\x00']
head = [b'\x00',b'\x00',b'\x00',b'\x00',b'\x00', b'\x00',b'\x00',b'\x00',b'\x00',b'\x00']

end = [b'\xAA',b'\xBB',b'\xCC',b'\xDD']

codigo_server = 128

#tipo1head = [b'\x01',b'\x00',b'\x00',b'\x00',b'\x00'] #Cliente --> servidor Handshake, indentificador de server e quantidade de pacotes que prtendem ser enviados
#tipo2head = [b'\x02',b'\x00',b'\x00',b'\x00',b'\x00'] # Servidor --> cliente (servidor está pronto para receber pacotes
#tipo3head = [b'\x03',b'\x00',b'\x00',b'\x00',b'\x00'] # Cliente --> servidor (pacote de dados), com o indentificador de número de pacote em cada um
#tipo4head = [b'\x04',b'\x00',b'\x00',b'\x00',b'\x00'] # Servidor --> cliente Verificador (numero do pacote e tamanho do pacote)
#tipo5head = [b'\x05',b'\x00',b'\x00',b'\x00',b'\x00'] # Timeout
#tipo6head = [b'\x06',b'\x00',b'\x00',b'\x00',b'\x00'] # Erro no pacote
#tipo7 = 'pacote recebido com sucesso'
EOP = [b'\xAA',b'\xBB',b'\xCC',b'\xDD']

def create_package(head, comando, end):
    package = []
    package.extend(head)
    package.extend(comando)
    package.extend(end)
    return package

def send_package(com1, package):
    for c in package:
        com1.sendData(np.asarray(c))
        time.sleep(.05)

def get_separeted_package(com1): 
    head, nh = com1.getData(10)
    body_size = head[5] 
    if head[0] == 1 or head[0] == 2:
        body_size = 4
    elif head[0] == 4:
        body_size = 1
    body, nb = com1.getData(body_size)
    end, ne = com1.getData(4)
    return [head, body, end, nh, nb, ne]

def tamanho_real(size):
    return size  #Utlizado para resolver um bug que acontecia em certas ocasioes

def split_In_lists(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))
