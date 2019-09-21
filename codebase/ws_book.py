from kafka import KafkaProducer
from binance.client import Client
from binance.websockets import BinanceSocketManager
import json

api_key = 'FQbSRS2sixuRGn8rXoHBXEBYY6xpFJvMGoAgvzcr1ryECZRfrBAqodQQr7oLskNk'
api_secret = 'jHajrkReMUiC7ozVpdZ6zpTpHjbRStANRHvMupBWtSkou02U7QPf5zrrjsjr5NIP'

client = Client(api_key, api_secret)
bm = BinanceSocketManager(client, user_timeout=60)

producer = KafkaProducer(bootstrap_servers='94.130.92.47:9092')


def process_m_message(msg):
    # if 'kline' in str(msg['stream']):
    producer.send('kline', key=msg['stream'].encode('utf-8') , value=json.dumps(msg['data']).encode('utf-8'))
    print("topic: {} key: {} data: {}".format('kline', msg['stream'], msg['data']))


# pass a list of stream names
conn_key = bm.start_multiplex_socket(['btcusdt@depth20@100ms'], process_m_message)

bm.start()

