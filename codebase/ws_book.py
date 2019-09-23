from kafka import KafkaProducer
from binance.client import Client
from binance.websockets import BinanceSocketManager
import json

api_key = 'FQbSRS2sixuRGn8rXoHBXEBYY6xpFJvMGoAgvzcr1ryECZRfrBAqodQQr7oLskNk'
api_secret = 'jHajrkReMUiC7ozVpdZ6zpTpHjbRStANRHvMupBWtSkou02U7QPf5zrrjsjr5NIP'

client = Client(api_key, api_secret)
bm = BinanceSocketManager(client, user_timeout=60)

producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')


def process_m_message(msg):
    producer.send('book', key=msg['stream'].encode('utf-8') , value=json.dumps(msg['data']).encode('utf-8'))
    print("topic: {} key: {} data: {}".format('book', msg['stream'], msg['data']))


# pass a list of stream names
conn_key = bm.start_multiplex_socket(['btcusdt@depth20@100ms', 'fetbtc@depth20@100ms', 'ethusdt@depth20@100ms',
				      'ethbtc@depth20@100ms', 'xrpbtc@depth20@100ms', 'bnbbtc@depth20@100ms',
				      'bnbusdt@depth20@100ms', 'bnbeth@depth20@100ms', 'adabtc@depth20@100ms',
			       	      'adaeth@depth20@100ms'], process_m_message)

bm.start()

