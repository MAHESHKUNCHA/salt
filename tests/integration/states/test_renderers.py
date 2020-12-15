"""
Integration tests for renderer functions
"""


import pytest
from tests.support.case import ModuleCase
from tests.support.helpers import flaky, slowTest


@pytest.mark.windows_whitelisted
class TestJinjaRenderer(ModuleCase):
    """
    Validate that ordering works correctly
    """

    @slowTest
    def test_dot_notation(self):
        """
        Test the Jinja dot-notation syntax for calling execution modules
        """
        ret = self.run_function("state.sls", ["jinja_dot_notation"])
        for state_ret in ret.values():
            self.assertTrue(state_ret["result"])

    @flaky
    @slowTest
    def test_salt_contains_function(self):
        """
        Test if we are able to check if a function exists inside the "salt"
        wrapper (AliasLoader) which is available on Jinja templates.
        """
        ret = self.run_function("state.sls", ["jinja_salt_contains_function"])
        for state_ret in ret.values():
            self.assertTrue(state_ret["result"])
