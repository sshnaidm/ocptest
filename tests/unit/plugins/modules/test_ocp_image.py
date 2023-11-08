from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.sshnaidm.ocptest.plugins.module_utils.ocp_image_lib import (
   OCPImage
)


@pytest.mark.parametrize('test_input, expected', [
    ('4.13', '....'),
    ()
])
def test_image(test_input, expected):
    result = OCPImage(test_input)
    assert result == expected
