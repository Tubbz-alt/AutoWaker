import socket
import urlparse
import logging
import os

from AutoWakerHandler import ServerRequestHandler
from ConfigHandler import getPath
from TimeHandler import today


#  Puts log into a relative location, and adds a day stamp.
def setupLogger():
    today_as_dt = today()
    logging.basicConfig(filename='ServerLogs.log',level=logging.INFO, filemode ='w')
    
    # ~/Logs/sleepLogs*date*.log
    relative_log_location = [getPath(), 'Logs', 'ServerLogs' + today_as_dt + '.log']
    hdlr = logging.FileHandler(os.path.join(*relative_log_location))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    
    hdlr.setFormatter(formatter)
    hdlr.setLevel(logging.INFO)
    LOG = logging.getLogger(name = "ServerLogs")
    LOG.addHandler(hdlr)
    LOG.setLevel(logging.INFO)
    return LOG

LOG = setupLogger()


# TODO: Clean this up a lot.
def parseDateAndUser(request):
    try:
        information = request.split('\n')
        print information
        print 'What we want: ' + information[0]
        data = str.split(information[0])
        print 'Attempt 1:' + data[1]
        params = data[1].split('?')[1].split('&') #Get rid of the /?
        for element in params:
            parameter_parsing = element.split('=')
            if parameter_parsing[0]=='date':
                date = parameter_parsing[1]
            elif parameter_parsing[0]=='user':
                user = parameter_parsing[1]
        return date, user
    except:
        return "","-"

def getHostAndPort():
    return socket.getfqdn(), 8888

def assembleHttpResponse(user, date):
    http_ok = "HTTP/1.1 200 OK\n\n"
    our_result_maker = ServerRequestHandler(user = user, date = date)
    json_information = "{\"wakeTime\": \"" + our_result_maker.getWakeTime() + "\"}"
    return http_ok + json_information

def getListenSocket():
    HOST, PORT = getHostAndPort()
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    LOG.info('Serving HTTP on port ' + str(PORT) + ' ...')
    return listen_socket

def startServer():
    listen_socket = getListenSocket()

    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)

        print request
        
        date, user = parseDateAndUser(request)
        LOG.info("date is: " + date + " and the user is: " + user)
        
        http_response = assembleHttpResponse(user, date)
    
        client_connection.sendall(http_response)
        client_connection.close()
    
startServer()