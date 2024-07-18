import socket,cv2, pickle, struct, time, select, sys
import pyaudio
import threading


def trans_video():
	# Socket Create
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_name  = socket.gethostname()
	host_ip = socket.gethostbyname(host_name)
	print('HOST IP:',host_ip)
	port = 9999
	socket_address = (host_ip,port)

	# Socket Bind
	server_socket.bind(socket_address)

	# Socket Listen
	server_socket.listen(5)
	print("LISTENING AT:",socket_address)

	# Socket Accept
	while True:
		client_socket,addr = server_socket.accept()
		print('GOT CONNECTION FROM:',addr)
		if client_socket:
			vid = cv2.VideoCapture(0)
			
			while(vid.isOpened()):
				img,frame = vid.read()
				a = pickle.dumps(frame)
				message = struct.pack("Q",len(a))+a
				client_socket.sendall(message)
				
				cv2.imshow('TRANSMITTING VIDEO',frame)
				key = cv2.waitKey(1) & 0xFF
				if key ==ord('q'):
					client_socket.close()

def trans_audio():
	
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    #Socket Create
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name  = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    port = 4444
    socket_address = (host_ip,port)  

    # Socket Bind
    serversocket.bind(socket_address)

    # Socket Listen
    serversocket.listen(5)


    def callback(in_data, frame_count, time_info, status):
        for s in read_list[1:]:
            s.send(in_data)
        return (None, pyaudio.paContinue)

    # Start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)

    read_list = [serversocket]
    print ("recording...")

    try:
        while True:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is serversocket:
                    (clientsocket, address) = serversocket.accept()
                    read_list.append(clientsocket)
                    print ("CONNECTION FROM:", address)
                else:
                    data = s.recv(1024)
                    if not data:
                        read_list.remove(s)
                         
    except KeyboardInterrupt:
        pass


    print ("finished recording")

    serversocket.close()
    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

def rec_video():
	# Socket Create
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_ip = '192.168.0.7' # paste server IP address here
	port = 9999
	client_socket.connect((host_ip,port)) 
	data = b""
	payload_size = struct.calcsize("Q")
	first_frame = 0
	next_frame = 0

	while True:
		while len(data) < payload_size:
			packet = client_socket.recv(4*1024) 
			if not packet: break
			data+=packet
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack("Q",packed_msg_size)[0]
		
		while len(data) < msg_size:
			data += client_socket.recv(4*1024)
		frame_data = data[:msg_size]
		data  = data[msg_size:]
		frame = pickle.loads(frame_data)

		next_frame = time.time()
		fps = int(1/(next_frame - first_frame))
		first_frame = next_frame

		fps_text = "FPS: {:.2f}".format(fps)
		cv2.putText(frame, fps_text, (5, 30), cv2.FONT_HERSHEY_PLAIN, 2, (66,135,245), 1)

		cv2.imshow("RECEIVING VIDEO",frame)
		key = cv2.waitKey(1) & 0xFF
		if key  == ord('q'):
			break
	client_socket.close()

def rec_audio():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    # Socket Create
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.0.7' #paste server IP address here
    port = 4444
    socket_address = (host_ip,port)
    client_socket.connect(socket_address)
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    try:
        while True:
            data = client_socket.recv(CHUNK)
            stream.write(data)

    except KeyboardInterrupt:
        pass

    print('Shutting down')
    client_socket.close()
    stream.close()
    audio.terminate()

x1 = threading.Thread(target = trans_video)
x2 = threading.Thread(target = trans_audio)
x3 = threading.Thread(target = rec_video)
x4 = threading.Thread(target = rec_audio)

x1.start()

x2.start()

x3.start()

x4.start()
