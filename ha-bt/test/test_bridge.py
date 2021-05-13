from unittest import TestCase
from unittest.mock import Mock, patch
from bridge import Bridge, MqttConnectError


class TestConnection(TestCase):
    def setUp(self):
        self.config = TestConfig()

    def test_throw_on_connection_error(self):
        with self.assertRaises(MqttConnectError):
            Bridge(self.config)

    @patch('bridge.mqtt')
    def test_throw_on_non_zero_connect_response_code(self, mqtt_mock):
        mqtt_client = Mock()
        mqtt_mock.Client.return_value = mqtt_client

        Bridge(self.config)

        with self.assertRaises(MqttConnectError):
            response_code = 1
            mqtt_client.on_connect(None, None, None, None, response_code)

    @patch('bridge.mqtt')
    def test_log_message_on_connect(self, mqtt_mock):
        mqtt_client = Mock()
        mqtt_mock.Client.return_value = mqtt_client

        Bridge(self.config)

        with self.assertLogs('bridge', level='INFO') as cm:
            response_code = 0
            mqtt_client.on_connect(None, None, None, None, response_code)

        self.assertEqual(
            ['INFO:bridge:Connected to MQTT Broker!'],
            cm.output
        )

    @patch('bridge.mqtt')
    def test_call_loop_forever_on_start(self, mqtt_mock):
        mqtt_client = Mock()
        mqtt_mock.Client.return_value = mqtt_client

        bridge = Bridge(self.config)

        bridge.start()

        mqtt_client.loop_forever.assert_called_once()

    @patch('bridge.mqtt')
    def test_subscribe_on_add_listener(self, mqtt_mock):
        mqtt_client = Mock()
        mqtt_mock.Client.return_value = mqtt_client

        def dummy_method():
            pass

        bridge = Bridge(self.config)

        bridge.add_listener('some/topic', dummy_method)

        mqtt_client.subscribe.assert_called_with('some/topic')

    @patch('bridge.mqtt')
    def test_send_json_message(self, mqtt_mock):
        mqtt_client = Mock()
        mqtt_mock.Client.return_value = mqtt_client

        bridge = Bridge(self.config)

        bridge.send('target_topic', {"foo": "bar", "bar": "baz"})

        mqtt_client.publish.assert_called_with(
            'target_topic',
            '{"foo": "bar", "bar": "baz"}',
            qos=1
        )

    @patch('bridge.mqtt')
    def test_route_message_to_listener(self, mqtt_mock):
        mqtt_client = Mock()
        mqtt_mock.Client.return_value = mqtt_client

        bridge = Bridge(self.config)

        bridge.add_listener('some_topic', self._listener_method)

        message = Mock()
        message.topic = 'some_topic'
        message.payload.decode.return_value = '{"foo": "bar"}'

        mqtt_client.on_message(None, None, message)

        self.assertEqual({'foo': 'bar'}, self.payload)

    def _listener_method(self, payload):
        self.payload = payload


class TestConfig:
    broker = '8.8.8.8'
    port = 1883
    username = 'test'
    password = 'test'
    keepalive = 0.1
