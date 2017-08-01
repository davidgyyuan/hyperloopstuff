from Tkinter import *
import Tkinter
import ttk
import threading
import struct
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM

measurementList = "Distance Speed Acceleration - - - - - - -".split()
defaultValues = [0] * len(measurementList)

PORT_NUMBER = 3000
SIZE = 1024
hostName = gethostbyname('0.0.0.0')
mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))
SERVER_IP = ''


class Frame(Tkinter.Frame):
    def __init__(self, parent):
        """ Sets up instance variables"""
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.tree = ttk.Treeview(self.parent, columns='data')
        self.button = Button(self.parent, text="Emergency Stop", command=cmdStop)
        self.initialize_user_interface()
        self.init_data()

    def initialize_user_interface(self):
        """ Sets up user interface"""
        self.parent.title("512 Hyperloop Display Panel: No client connected")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.config(background="white")

        self.tree.heading('#0', text='Feature')
        self.tree.heading('#1', text='Data')
        self.tree.column("#0", stretch=Tkinter.YES)
        self.tree.column("#1", stretch=Tkinter.YES, anchor='e')
        self.tree.grid(row=0, columnspan=1, sticky='new')
        self.button.grid(row=1, columnspan=1, sticky='n')

    def init_data(self):
        """ Initializes treeview with default numbers"""
        for i in range(len(measurementList)):
            self.tree.insert('', 'end', iid=i+1, text=measurementList[i], values=defaultValues[i])


def updateData(frame, newData):
    """
    Updates the treeview in the frame with data found in newData.

    :param frame: The Tkinter frame with a treeview to display the data.
    :param newData: List with numbers to be displayed.
    """
    for i in range(len(measurementList)):
            frame.tree.set(i+1, column="#1", value=newData[i])


def cmdStop():
    """Function used to send stop signal"""
    mySocket.sendto('s'*35, (SERVER_IP, PORT_NUMBER))


def count():
    """Continuously receives data from client"""
    global SERVER_IP
    while not root.state() == 'normal':
        pass
    while root.state() == 'normal':
        unpacker = struct.Struct('! B B i i i i i i i I')
        (data, addr) = mySocket.recvfrom(unpacker.size)
        receivedList = unpacker.unpack(data)
        mainFrame.parent.title("512 Hyperloop Display Panel: Client Connected")
        SERVER_IP = addr
        updateData(mainFrame, receivedList)

root = Tkinter.Tk()
mainFrame = Frame(root)
threading.Thread(target=count).start()
root.mainloop()

