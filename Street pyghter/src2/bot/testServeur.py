#!/usr/bin/python3
import time
import socket

hote = ''

port1 = 12800
port2 = 12801

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connexion_principale.bind((hote, port1))


connexion_principale.listen(5)
connexion_principale.settimeout(2)

print("Le serveur écoute à présent sur le port {}".format(port1))


try:
	connexion_avec_client, infos_connexion = connexion_principale.accept()
except socket.timeout:
	print("To late")

print("Client")

connexion_principale.bind((hote, port1))
print("Le serveur écoute à présent sur le port {}".format(port2))

try:
	connexion_avec_client, infos_connexion = connexion_principale.accept()
except socket.timeout:
	print("To late")





msg_recu = b""

while msg_recu != b"fin":

    msg_recu = connexion_avec_client.recv(1024)

    # L'instruction ci-dessous peut lever une exception si le message

    # Réceptionné comporte des accents

    print(msg_recu.decode())

    connexion_avec_client.send(b"5 / 5")


print("Fermeture de la connexion")

connexion_avec_client.close()

connexion_principale.close()
