
HOST="127.0.0.1"
PORT=4400
PLEN=100
TTL=2
FILENAME=report.txt

server: server.py
	python server.py $(HOST) $(PORT)

client: client.py
	python client.py $(HOST) $(PORT) $(PLEN) $(TTL) $(FILENAME)
