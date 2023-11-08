from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from unittest.mock import patch

from ansible_collections.sshnaidm.ocptest.plugins.module_utils.common.utils import (
    get_url,
)


@pytest.mark.parametrize('test_input, expected', [
    ("http://example.com", "http://example.com"),
])
@patch('requests.get')
def test_get_url(self, mock_get):
    mock_get.return_value.text = "testme"
    result = get_url('http://example.com')
    self.assertEqual(result, 'testme')
