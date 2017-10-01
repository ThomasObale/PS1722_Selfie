import urllib.request, requests, json, os, socket
from time import sleep

#Broadcast UDP packet using this IP and port number

#Variables that are used in functions
global UDP_PORT, UDP_IP, projectID
UDP_PORT = 5016 # Random UDP port selected
UDP_IP="192.168.0.255" #Broadcast address to send sockets to all Pi's
projectID = ""
MESSAGE = "Catch"
RELEASE = "Release"

# Create the socket connection
sock = socket.socket(socket.AF_INET, 
            socket.SOCK_DGRAM) 
sock.bind(('',0))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


def displayExistingProjects():
    
    projects = urllib.request.urlopen("http://localhost:8000/selfie/v1/projects")

    data = json.loads(projects.read().decode())

    print("ID \t Project Name")
    print("-------------------------------")
    for project in data:
        print(str(project['id']) + " \t " + project['name'])


def addNewProject():
    name = input("Please enter the name of the project")
    
    post = requests.post('http://localhost:8000/selfie/v1/projects', data = {'name': name})
    
    displayExistingProjects()

    print("Created successfully")

def deleteProject():
    name = input("What is the ID of the project you want to delete? ")



def postImages():
    #Looping variables
    allowCapture = True
    captureNumber = 1

    while(allowCapture):

        projectID = input("\nWhat is the project ID? ")

        keyInput = input("\nEnter to Capture, or R key to release images: ")
        if keyInput=="":
            #Reset the text file counter every time a capture is required
            # Send project ID to Raspberry Pi
            sock.sendto(projectID, (UDP_IP, UDP_PORT))
            # Send a message to the Raspberry Pi
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


            print ("Image set capture: ", captureNumber)
            captureNumber+=1


        elif keyInput == "r":   
            print ('Release initiated')
            sock.sendto(RELEASE, (UDP_IP, UDP_PORT))

            allowCapture = False
            print ("The script has ended.")
    

def mainMenu():    
    print("\nMain Menu")
    print("----------------------------")
    print("1. Display Existing Projects")
    print("2. Create a new Project")
    print("3. Delete project by ID")
    print("4. Post Images")
    print("5. Exit")

mainMenu()
menuOption = int(input("\nSelect a Menu Option: (1, 2, 3, or 5) "))

print(menuOption)

while menuOption != 5:
    
    if menuOption == 1:
        displayExistingProjects()
    elif menuOption == 2:
        addNewProject()
    elif menuOption == 3:
        deleteProject()
    elif menuOption == 4:
        postImages()
    elif menuOption == 5:
        exit()

    mainMenu()
    menuOption = int(input("Select a menu Option "))