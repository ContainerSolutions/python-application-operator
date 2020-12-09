# Copyright 2020 kirek007@gmail.com <Marek Ruszczyk>
# See LICENSE file for licensing details.

import unittest

from ops.testing import Harness
from charm import PythonApplicationOperatorCharm


class TestCharm(unittest.TestCase):
    def test_config_changed(self):
        harness = Harness(PythonApplicationOperatorCharm)
        self.addCleanup(harness.cleanup)
        harness.begin()
        harness.update_config({"thing": "foo"})
