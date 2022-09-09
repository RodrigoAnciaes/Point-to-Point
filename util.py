import time
import numpy as np

def create_package(head, comando, end):
    package = []
    for i in head:
        package.append(i)
    for i in comando:
        package.append(i)
    for i in end:
        package.append(i)
    return package

def send_package(com1, package):
    for c in package:
        com1.sendData(np.asarray(b'\xCC'))
        time.sleep(.05)
        com1.sendData(np.asarray(c))
        time.sleep(.05)
def get_separeted_package(com1):
    head, nh = com1.getData(10)
    body_size = head[3] # No client foi definido que o tamanho do body é o 4º byte do head (adicionado os \xCC). Nessa linha ainda existe um erro ao receber o tamanho do body
    body, nb = com1.getData(body_size)
    end, ne = com1.getData(4)
    return [head, body, end, nh, nb, ne]

def tamanho_real(size):
    return size  #Utlizado para resolver um bug que acontecia em certas ocasioes

def split_In_lists(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

handshake_head = [b'\xFF',b'\x05',b'\x00',b'\x00',b'\x00']
error_head = [b'\xFA',b'\x05',b'\x00',b'\x00',b'\x00']
ok_head = [b'\xFB',b'\x05',b'\x00',b'\x00',b'\x00']
head = [b'\x00',b'\x00',b'\x00',b'\x00',b'\x00']

end = [b'\xFF',b'\xFF']

