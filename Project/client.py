import socket


port = 4000

def client_request(input):
    # 본인 IP 작성해주세요.
    host = "192.168.35.148"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(input.encode())
    receive_data = client_socket.recv(1024)
    print("받은 데이터는 \"", receive_data.decode(), "\" 입니다.", sep="")
    client_socket.close()

if __name__ == '__main__':
    print("'1' : '구월동', '2' : '주안', '3' : '논현', '4' : '부평', '5' : '송도'")
    input = input("측정소를 입력하세요: ")
    client_request(input)
