import json
from kafka.consumer.fetcher import ConsumerRecord
from kafka import KafkaConsumer
from influxdb import InfluxDBClient


consumer = KafkaConsumer('kline', bootstrap_servers='94.130.92.47:9092')
client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='example')
client.create_database('example')


def to_influx_format(message: ConsumerRecord):
    temp_value = json.loads(message.value.decode('utf-8'))

    json_body = dict()
    json_body['measurement'] = message.key.decode('utf-8')
    json_body['tags'] = {
        'type': temp_value['e'],
        'pair': temp_value['s'],
        'interval': temp_value['k']['i'] if temp_value['e'] == 'kline' else None
    }
    json_body['time'] = temp_value['k']['t']
    json_body['fields'] = temp_value['k']

    return [json_body]


for message_received in consumer:
    parsed_message = to_influx_format(message_received)
    client.write_points(parsed_message, time_precision='ms')
    print(parsed_message)
    print()