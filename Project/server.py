import requests
from bs4 import BeautifulSoup
import threading
import time
import socket
import warnings

warnings.filterwarnings('ignore')

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
key = '3gAlzH3Qu4kUSbXDJPvqC0/wfHZWpQDYqEib/p/GbuBG5rZfDyNoZRO4AGkWUnB6bdb1moMINYwiZlI9OH9baw=='
#본인 IP 작성해주세요.F
host = "192.168.35.148"
port = 4000

def request_pm(input):
    data = str(input)
    city = {'1' : '구월동', '2' : '주안', '3' : '논현', '4' : '부평', '5' : '송도'}
    station = city[data]
    params ={'serviceKey' : key, 'returnType' : 'xml', 'numOfRows' : '1', 'pageNo' : '1', 'stationName' : station, 'dataTerm' : 'DAILY', 'ver' : '1.0' }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    ItemList = soup.findAll('item')

    for item in ItemList:
        g = item.find('pm10value').text
        i = item.find('pm25value').text
        s = item.find('pm10grade').text
        t = item.find('pm25grade').text
        result_str = '측정소:' + station + '\n' \
                     + '미세먼지 농도:' + g + '㎍/㎥ ( ' + s + ' )' + '\n' \
                     + '초미세먼지 농도:' + i + '㎍/㎥ ( ' + s + ' )' + '\n' \
                     + '( 좋음: 1 ),( 보통: 2 ),( 나쁨: 3 ),( 매우나쁨: 4)'
        #print('측정소:' + station)
        #print('미세먼지 농도:' + g + '㎍/㎥ ( ' + s + ' )')
        #print('초미세먼지 농도:' + i + '㎍/㎥ ( ' + s + ' )')
        #print('( 좋음: 1 ),( 보통: 2 ),( 나쁨: 3 ),( 매우나쁨: 4)')

        return result_str

def handle_client(client_socket, addr):
    user = client_socket.recv(1024)
    client_socket.sendall(request_pm(user.decode()).encode())
    print("요청받은 데이터 " + user.decode())
    time.sleep(1)
    client_socket.close()

def accept_func():
    global server_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while 1:
        try:
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            server_socket.close()
            print("Keyboard interrupt")

        print("클라이언트 핸들러 스레드로 이동 됩니다.")
        t = threading.Thread(target=handle_client, args=(client_socket, addr))
        t.daemon = True
        t.start()


if __name__ == '__main__':
    accept_func()