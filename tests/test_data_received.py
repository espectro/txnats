from mock import patch

import json

from twisted.trial import unittest
from twisted.internet import task
from twisted.internet import defer

import txnats


class BaseTest(unittest.TestCase):
    maxDiff = None

    @defer.inlineCallbacks
    def setUp(self):
        """
        Create protocol.

        Add any fixtures.

        :return:
        """
        self.reactor = task.Clock()
        self.nats_protocol = txnats.io.NatsProtocol(
            own_reactor=self.reactor)
        yield

    def tearDown(self):
        """
        Any tear down.

        :return:
        """


class TestDataReceived(BaseTest):
    @defer.inlineCallbacks
    def test_info(self):
        """
        Ensure upon receiving an INFO operation, the server info is
        parsed and saved and a CONNECT operation is sent.

        """
        with patch("txnats.io.NatsProtocol.transport") as mock_transport:
            self.nats_protocol.dataReceived(
                "INFO {}".format(
                    json.dumps(
                        {u'auth_required': False,
                         u'go': u'go1.5.2',
                         u'host': u'0.0.0.0',
                         u'max_payload': 1048576,
                         u'port': 4222,
                         u'server_id': u'16dd1049f122d8d3d148894074423d48',
                         u'ssl_required': False,
                         u'tls_required': False,
                         u'tls_verify': False,
                         u'version': u'0.7.2'}
                    )
                )
            )

            mock_transport.write.assert_called_once_with(
                'CONNECT {"lang":"py.twisted","pedantic":false,'
                '"version":"0.2.0","verbose":true,"name":"xnats",'
                '"pass":"","auth_token":null,'
                '"ssl_required":false,"user":""}\r\n'
            )

            self.assertEqual(
                self.nats_protocol.server_settings,
                txnats.io.ServerInfo(
                    auth_required=False,
                    go=u'go1.5.2',
                    host=u'0.0.0.0',
                    max_payload=1048576,
                    port=4222,
                    server_id=u'16dd1049f122d8d3d148894074423d48',
                    ssl_required=False,
                    tls_required=False,
                    tls_verify=False,
                    version=u'0.7.2'
                ))
            yield
