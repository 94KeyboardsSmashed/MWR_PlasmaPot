sudo nice -20 python read_pot.py > log.txt & websocketd --port=8080 --staticdir=./static tail -f log.txt
