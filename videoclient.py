# lets make the client code
import socket,cv2, pickle,struct,time
import numpy as np


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
		packet = client_socket.recv(4*1024) # 4K
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

	# FPS calc
	next_frame = time.time()
	diff = next_frame - first_frame
	fps = int(1/(diff))
	first_frame = next_frame

	fps_text = "FPS: {:.2f}".format(fps)
	cv2.putText(frame, fps_text, (5, 30), cv2.FONT_HERSHEY_PLAIN, 3, (66,135,245), 1)

	cv2.imshow("RECEIVING VIDEO",frame)
	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break
client_socket.close()