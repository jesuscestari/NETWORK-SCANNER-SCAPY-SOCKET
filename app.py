from scapy.all import ARP, Ether, srp
import socket
from tkinter import *

root = Tk()
root.geometry("300x350")
root.title('Escaner de red')

lblsep = Label(root, text="-"*55).pack()
lbl1 = Label(root, text="Dispositivos conectados a la red").pack()
lblsep = Label(root, text="-"*55).pack()
lbl2 = Label(root, text="IP" + " "*18+"MAC").pack()
    
def obtenerIp():
    sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sc.connect(("8.8.8.8", 80)) 
    ip = sc.getsockname()
    ipLocal = ip[0] 
    sc.close()
    return(ipLocal)

IpRango = obtenerIp()+'/24'

arp = ARP(pdst = IpRango)

ether = Ether(dst="ff:ff:ff:ff:ff:ff")

packet = ether/arp

result = srp(packet, timeout=3, verbose=0)[0]

clientes = []

for sent, received in result:

    clientes.append({'ip': received.psrc, 'mac': received.hwsrc})


for client in clientes:
    valores = ("{:16}    {}".format(client['ip'], client['mac']))
    sv = StringVar()
    lbl = Label(root, width="100", height="2",textvariable=sv).pack()
    sv.set(valores)

lblsep = Label(root, text="-"*55).pack()
lblsep = Label(root, text="Puertos Abiertos", width=800).pack()
lblsep = Label(root, text="-"*55).pack()

ipp = obtenerIp()
for i in range(1, 1000):
    s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
    conexion = s.connect_ex((ipp, i))
    if(conexion == 0) :       
        resultados = ('Puerto %d: Abierto' % (i,))
        puertos = StringVar()
        lblport = Label(root, textvariable=puertos,  bg="#7fff00").pack()
        puertos.set(resultados)
    s.close()

mainloop()