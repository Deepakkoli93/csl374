
HOST="127.0.0.1"
PORT=4400
PLEN=1000
TTL=2
FILENAME=report.txt

server: 2011cs50278_server.py
	python 2011cs50278_server.py $(HOST) $(PORT)

client: 2011cs50278_client.py
	python 2011cs50278_client.py $(HOST) $(PORT) $(PLEN) $(TTL) $(FILENAME)
