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
    if 'kline' in str(msg['stream']):
        producer.send('kline', key=msg['stream'].encode('utf-8') , value=json.dumps(msg['data']).encode('utf-8'))
        print("topic: {} key: {} data: {}".format('kline', msg['stream'], msg['data']))


# pass a list of stream names
conn_key = bm.start_multiplex_socket(['btcusdt@kline_1m', 'btcusdt@kline_5m', 'fetbtc@kline_1m', 'fetbtc@kline_5m', 
				      'ethusdt@kline_1m', 'ethusdt@kline_5m', 'ethbtc@kline_1m', 'ethbtc@kline_5m', 
				      'xrpbtc@kline_1m', 'xrpbtc@kline_5m', 'bnbbtc@kline_1m', 'bnbbtc@kline_5m',
				      'bnbusdt@kline_1m', 'bnbusdt@kline_5m', 'bnbeth@kline_1m', 'bnbeth@kline_5m',
				      'adabtc@kline_1m', 'adabtc@kline_5m', 'adaeth@kline_1m', 'adaeth@kline_5m'], process_m_message)

bm.start()

