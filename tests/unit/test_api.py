# -*- coding: UTF-8 -*-

import pytest
from mock import MagicMock, patch

from librouteros.api import (
        Api,
        )
from librouteros.protocol import (
        parseWord,
        composeWord,
        ApiProtocol,
        )


@pytest.mark.parametrize('word,pair', (
            ('=dynamic=true', ('dynamic', True)),
            ('=dynamic=false', ('dynamic', False)),
        ))
def test_bool_parseWord(word, pair):
    """
    Test for parsing legacy bool values.

    Older routeros versions accept yes/true/no/false as values,
    but only return true/false.
    """
    assert parseWord(word) == pair


def test_parseWord(word_pair):
    assert parseWord(word_pair.word) == word_pair.pair


def test_composeWord(word_pair):
    assert composeWord(*word_pair.pair) == word_pair.word


class Test_Api:

    def setup(self):
        self.api = Api(protocol=MagicMock())

    @patch.object(Api, 'readResponse')
    @patch.object(ApiProtocol, 'writeSentence')
    def test_rawCmd_calls_writeSentence(self, writeSentence_mock, read_mock):
        args = ('/command', '=arg1=1', '=arg2=2')
        self.api.rawCmd(*args)
        assert writeSentence_mock.called_once_with(*args)

    @patch.object(Api, 'readResponse', return_value=(1,2))
    @patch.object(ApiProtocol, 'writeSentence')
    def test_rawCmd_returns_from_readResponse(self, writeSentence_mock, read_mock):
        assert tuple(self.api.rawCmd('/command', '=arg1=1', '=arg2=2')) == (1,2)
