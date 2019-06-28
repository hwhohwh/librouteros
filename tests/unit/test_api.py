# -*- coding: UTF-8 -*-

import pytest
from mock import MagicMock, patch

from librouteros.api import Api, Composer, Parser
from librouteros.connections import ApiProtocol


class Test_Parser:

    def test_apiCast_bidirectional(self, bidirectional_type_cast):
        assert Parser.apiCast(bidirectional_type_cast.api) == bidirectional_type_cast.python

    def test_apiCast(self, from_api_type_cast):
        assert Parser.apiCast(from_api_type_cast.api) == from_api_type_cast.python

    def test_parseWord(self, attribute_word):
        assert Parser.parseWord(attribute_word.raw) == (attribute_word.key, attribute_word.value)


class Test_Composer:

    def test_pythonCast_bidirectional(self, bidirectional_type_cast):
        assert Composer.pythonCast(bidirectional_type_cast.python) == bidirectional_type_cast.api

    def test_pythonCast(self):
        """
        Do not cast None to string. MikroTik API sometime returns "none" as value.
        Casting to "none" requires more reasearch.
        "none" may not always be None
        """
        assert Composer.pythonCast(None) == 'None'

    def test_composeWord(self, attribute_word):
        result = Composer.composeWord(key=attribute_word.key, value=attribute_word.value)
        assert result == attribute_word.raw


class Test_Api:

    def setup(self):
        self.api = Api(protocol=MagicMock())

    @pytest.mark.parametrize("path, expected", (
        ("/ip/address/", "/ip/address"),
        ("ip/address", "/ip/address"),
        ("/ip/address", "/ip/address"),
        ))
    def test_joinPath_single_param(self, path, expected):
        assert self.api.joinPath(path) == expected

    @pytest.mark.parametrize("path, expected", (
        (("/ip/address/", "print"), "/ip/address/print"),
        (("ip/address", "print"), "/ip/address/print"),
        (("/ip/address", "set"), "/ip/address/set"),
        (("/", "/ip/address", "set"), "/ip/address/set"),
        ))
    def test_joinPath_multi_param(self, path, expected):
        assert self.api.joinPath(*path) == expected

    @patch.object(Api, '_readResponse')
    @patch.object(ApiProtocol, 'writeSentence')
    def test_rawCmd_calls_writeSentence(self, writeSentence_mock, read_mock):
        args = ('/command', '=arg1=1', '=arg2=2')
        self.api.rawCmd(*args)
        assert writeSentence_mock.called_once_with(*args)

    @patch.object(Api, '_readResponse')
    @patch.object(ApiProtocol, 'writeSentence')
    def test_rawCmd_returns_from_readResponse(self, writeSentence_mock, read_mock):
        assert self.api.rawCmd('/command', '=arg1=1', '=arg2=2') == read_mock.return_value
