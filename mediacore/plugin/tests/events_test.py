# This file is a part of MediaCore CE, Copyright 2009-2012 MediaCore Inc.
# The source code contained in this file is licensed under the GPL.
# See LICENSE.txt in the main project directory, for more information.
#
# Copyright (c) 2012 Felix Schwarz (www.schwarz.eu)

from mediacore.lib.test.pythonic_testcase import *

from mediacore.plugin.events import Event, FetchFirstResultEvent, GeneratorEvent


class EventTest(PythonicTestCase):
    def setUp(self):
        self.observer_was_called = False
    
    def probe(self):
        self.observer_was_called = True
    
    def test_can_notify_all_observers(self):
        event = Event([])
        event.observers.append(self.probe)
        
        assert_false(self.observer_was_called)
        event()
        assert_true(self.observer_was_called)


class FetchFirstResultEventTest(PythonicTestCase):
    def test_returns_first_non_null_result(self):
        event = FetchFirstResultEvent([])
        event.observers.append(lambda: None)
        event.observers.append(lambda: 1)
        event.observers.append(lambda: 2)
        
        assert_equals(1, event())
    
    def test_passes_all_event_parameters_to_observers(self):
        event = FetchFirstResultEvent([])
        event.observers.append(lambda foo, bar=None: foo)
        event.observers.append(lambda foo, bar=None: bar or foo)
        
        assert_equals(4, event(4))
        assert_equals(6, event(None, bar=6))


class GeneratorEventTest(PythonicTestCase):
    def test_can_unroll_lists(self):
        event = GeneratorEvent([])
        event.observers.append(lambda: [1, 2, 3])
        event.observers.append(lambda: ('a', 'b'))
        
        assert_equals([1, 2, 3, 'a', 'b'], list(event()))
    
    def test_can_return_non_iterable_items(self):
        event = GeneratorEvent([])
        event.observers.append(lambda: [1, ])
        event.observers.append(lambda: None)
        event.observers.append(lambda: 5)
        event.observers.append(lambda: 'some value')
        
        assert_equals([1, None, 5, 'some value'], list(event()))



import unittest
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EventTest))
    suite.addTest(unittest.makeSuite(FetchFirstResultEventTest))
    suite.addTest(unittest.makeSuite(GeneratorEventTest))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')