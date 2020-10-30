# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.locate_result import LocateResult  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLocateController(BaseTestCase):
    """LocateController integration test stubs"""

    def test_locate_token(self):
        """Test case for locate_token

        Find tokens
        """
        body = '\"The brown fox jumped over the brown log\"'
        query_string = [('save', true),
                        ('compute', true)]
        response = self.client.open(
            '/mscs721/concordance/1.0.0/locate',
            method='POST',
            data=json.dumps(body),
            content_type='text/plain',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
