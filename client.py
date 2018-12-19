from socket import *
from sys import *

resumeFlag = False
numberOfConnections = None
intervalMetricReport = None
connectionType = None
fileAddress = None
outputLocation = None


def parseArguments(argv):
    for i in range(len(argv)):
        if argv[i] == "-r":
            global resumeFlag
            resumeFlag = True
            print("there is -r in arguments")
        if argv[i] == "-n":
            global numberOfConnections
            numberOfConnections = int(argv[i + 1])
            print("num connections are: ", numberOfConnections)
        if argv[i] == "-i":
            global intervalMetricReport
            intervalMetricReport = float(argv[i + 1])
            print("Time interval between metric reporting is: ", intervalMetricReport)
        if argv[i] == "-c":
            global connectionType
            connectionType = argv[i + 1]
            print("The connection type is : " + connectionType)
        if argv[i] == "-f":
            global fileAddress
            fileAddress = argv[i + 1]
            print("The file location is: " + fileAddress)
        if argv[i] == "-o":
            global outputLocation
            outputLocation = argv[i + 1]
            print("This is location on client where file is downloaded: " + outputLocation)


def TCP_connection(fileAddress):
    resume = False
    cl = 0
    headDic = {}
    serverPort = 80
    string = fileAddress
    # split file, extension and domain
    string = fileAddress
    split1 = string.split('//')
    string1 = split1[1]
    split2 = string1.split('/')
    split3 = split2[-1].split('.')
    domain = split2[0]
    file = split3[0]
    ext = split3[1]
    # connect to html or local server
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('%s'%(domain), serverPort))  # '%s'%(domain) #'10.7.44.121'
    # GET query
    output = "GET /%s.%s HTTP/1.1\r\nHOST: %s\r\n\r\n" % (file, ext, domain)
    s.sendall(output.encode())
    # retrieve header and split header
    reply = s.recv(1024)
    header = reply.split(b'\r\n\r\n')[0]
    # decode header to str
    dHeader = header.decode('utf-8')
    # header
    splitHeader = dHeader.split('\r\n')
    # get image size
    for line in splitHeader:
        if "Accept-Ranges:" in line:
            resume = True
            print(resume)
        if "Content-Length:" in line:
            cl = line.split(':')[1]
            print("Content-Length:", cl)
            break
    splitData = reply.split(b'\r\n\r\n')[1]
    # save image and append image in bytes
    f = open('%s.%s' % (file, ext), 'wb')
    f.close()
    f = open('%s.%s' % (file, ext), 'ab')
    f.write(splitData)
    # select([s], [], [], 3)[0]
    # receive data in loop and write it in file
    while 1:
        data = s.recv(1024)
        if not data:
            break
        f.write(data)
    s.close()


if __name__ == '__main__':
    parseArguments(argv)
    TCP_connection(fileAddress)
