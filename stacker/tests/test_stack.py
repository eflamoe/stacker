import unittest

from mock import MagicMock

from stacker.stack import _gather_parameters, Stack
from .factories import generate_definition


class TestStack(unittest.TestCase):

    def setUp(self):
        self.sd = {"name": "test"}
        self.stack = Stack(
            definition=generate_definition('vpc', 1),
            context=MagicMock(),
        )

    def test_stack_requires(self):
        self.assertIn('fakeStack', self.stack.requires)
        self.assertIn('fakeStack2', self.stack.requires)

    def test_empty_parameters(self):
        build_action_parameters = {}
        self.assertEqual({}, _gather_parameters(self.sd, build_action_parameters))

    def test_generic_build_action_override(self):
        sdef = self.sd
        sdef["parameters"] = {"Address": "10.0.0.1", "Foo": "BAR"}
        build_action_parameters = {"Address": "192.168.1.1"}
        result = _gather_parameters(sdef, build_action_parameters)
        self.assertEqual(result["Address"], "192.168.1.1")
        self.assertEqual(result["Foo"], "BAR")

    def test_stack_specific_override(self):
        sdef = self.sd
        sdef["parameters"] = {"Address": "10.0.0.1", "Foo": "BAR"}
        build_action_parameters = {"test::Address": "192.168.1.1"}
        result = _gather_parameters(sdef, build_action_parameters)
        self.assertEqual(result["Address"], "192.168.1.1")
        self.assertEqual(result["Foo"], "BAR")

    def test_invalid_stack_specific_override(self):
        sdef = self.sd
        sdef["parameters"] = {"Address": "10.0.0.1", "Foo": "BAR"}
        build_action_parameters = {"FAKE::Address": "192.168.1.1"}
        result = _gather_parameters(sdef, build_action_parameters)
        self.assertEqual(result["Address"], "10.0.0.1")
        self.assertEqual(result["Foo"], "BAR")

    def test_specific_vs_generic_build_action_override(self):
        sdef = self.sd
        sdef["parameters"] = {"Address": "10.0.0.1", "Foo": "BAR"}
        build_action_parameters = {
            "test::Address": "192.168.1.1",
            "Address": "10.0.0.1"}
        result = _gather_parameters(sdef, build_action_parameters)
        self.assertEqual(result["Address"], "192.168.1.1")
        self.assertEqual(result["Foo"], "BAR")
