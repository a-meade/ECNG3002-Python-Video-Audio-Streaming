# ECNG3002-Python-Video-Audio-Streaming

This project involved researching the various libraries, modules and transport layer protocols used for data transmission, specifically audio and video. The goal was to identify and choose the most suitable options. Following this, a python application was then developed, which enabled users to capture audio and video from their microphone and webcam, respectively and then transmit this live stream to another computer on the same network with negligible delay.

The Python socket modules provided a way to create a network connection and communicate between different computers over a network. 

Stream sockets (TCP) were used to transfer the data, mainly because stream sockets are reliable, bidirectional, sequenced and the data is unduplicated. 

This method is more reliable than Datagram Sockets(UDP) as dropped packets are detected and retransmitted and sequencing means that the data is sent and received in the order it was meant to be. 

# Video Module

For the video capture module, the OpenCV library was utilised due to its simplicity and popularity for this type of application. OpenCV also allowed for the added benefit of displaying a frame counter.

# Audio Module

For the audio capture module, the Pyaudio library as it allowed for the recording and playing of audio in real time across differents OS.

# Use

For this application, the server side must be established first. 

The initial step is to create an IPv4 TCP socket and bind it to the host IP address and a selected port number.

This is followed by the listen function which allows the application to listen for a connection from the client socket which also needs to be created. 

The server then accepts the client socket and obtains the IP address and port number of the client and then the video frames and audio chunks are transmitted. 
