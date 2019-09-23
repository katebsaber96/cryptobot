import json
from kafka.consumer.fetcher import ConsumerRecord
from kafka import KafkaConsumer
from influxdb import InfluxDBClient

consumer = KafkaConsumer('book', bootstrap_servers='127.0.0.1:9092')
client = InfluxDBClient(host='localhost', port=8086, username='admin', password='@Mystrongpassword1', database='cryptobot')
client.create_database('cryptobot')

def to_influx_format(message: ConsumerRecord):
    temp_value = json.loads(message.value.decode('utf-8'))

    json_body = dict()
    json_body['measurement'] = message.key.decode('utf-8')
    json_body['tags'] = {
        'type': 'depth',
        'pair': message.key.decode('utf-8').split('@')[0],
        'depth': message.key.decode('utf-8').split('@')[1]
    }
    json_body['time'] = message_received.timestamp
    json_body['fields'] = {
        'asks': json.dumps(temp_value['asks']),
        'bids': json.dumps(temp_value['bids'])
    }

    return [json_body]


for message_received in consumer:
    parsed_message = to_influx_format(message_received)
    client.write_points(parsed_message, time_precision='ms')
    print(parsed_message)
    print()
