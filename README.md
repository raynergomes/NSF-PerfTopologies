# NSF-PerfTopologies
Network Service Function Chaining: A Performance Study Varying Topologies

# Basic topology
The line below represents a sequence of seven hosts, each running a specific code. The topology is sequential, and the localhost, target host, and port variables need to be updated in all files. The next blocks will explain these functions, executions, and their goals.

Host1[SendDatagram] -> Host2[RTBilling] -> Host3[RTBilling] -> Host4[RTCripter] -> Host5[RTLogging] -> Host6[RTTAnalysis] -> Host7[ServerUDP]

# Execution
All files are Python's code, so you can run them using the command python <filename.py>

# Code variables
The files contain three variables (localhost, listenPort, and targetHost) that need to be updated according to the topology used. The localhost host refers to the IP address of the host on which the files are located. ListenPort is the port on which the process listens to the connections. Finally, the variable targetHost is the IP address of the host to which the datagrams will be sent.
Therefore, depending on the topology, the coder needs to update these three variables in all files before the execution.

## Example
localhost = "10.0.0.32"
listenPort = 4444
targetHost = "10.0.0.33"

# Thread in the code
We will explain the execution structure of the codes' functions just for clarity. Users do not need to be concerned about this; it is just for programmers who like to change the code. To avoid bottlenecks related to receiving messages, carry on a function and deliver the messages to the following function, which has three internal threads. They are:

1. threadListen: This thread is responsible for receiving a datagram and forwards to thread<Function>
2. threadForward: This thread is responsible for sending a datagram to another process; it can be another function or the final host.
3. thread<Funtion>: This function represents the particular nature of the function. The <Function> label will change depending on the file; if it is the file related to billing, then the thread will call threadBilling. 


# Descripton about the files used in the simulation

1. RTBilling.py: Implements a function to calculate a bill of the quantity of messages sent.
2. RTCripter.py: Implements a function to encrypt the received message.
3. RTLogging.py: Implements a function to check if the user and password present in the received message are correct.
4. RTTAnalysis.py: Implements a function to count and save the number of characters received over time.
5. SendDatagram.py: The client program is used to start sending messages. 
6. ServerUDP.py: The final point of all messages. It is responsible for saving all messages and creating statics in the final execution.

# GNS3 Topologies

In the link below, there are three GNS3 projects were used to simulate three different topologies. Each host is a docker container; thus, to carry on the simulation, we need to copy each Python file and update the IP address in the files.

https://drive.google.com/file/d/1c2YZpzwauLiOcZo7AtWZ5m30KJ-P4yp2/view?usp=drive_link
