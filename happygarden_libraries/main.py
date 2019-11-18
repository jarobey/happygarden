from happygarden.ahk import GardenHub
import socket

hub = GardenHub('{0} Bridge'.format(socket.gethostname()),'pi','10.0.10.200')
hub.start()