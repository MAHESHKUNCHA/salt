# -*- coding: utf-8 -*-

# Import Python Libs
from __future__ import absolute_import, unicode_literals, print_function

# Import Salt Testing Libs
from tests.support.mock import NO_MOCK, NO_MOCK_REASON, patch
from tests.support.unit import TestCase, skipIf

# Import Salt Libs
import salt.utils.platform
import salt.utils.win_pdh as win_pdh


@skipIf(NO_MOCK, NO_MOCK_REASON)
@skipIf(not salt.utils.platform.is_windows(), 'System is not Windows')
class WinPdhTestCase(TestCase):
    def test_list_objects(self):
        known_objects = ['Cache', 'Memory', 'Process', 'Processor', 'System']
        objects = win_pdh.list_objects()
        for item in known_objects:
            self.assertTrue(item in objects)

    def test_list_counters(self):
        counters = win_pdh.list_counters('Processor')
        known_counters = ['% Processor Time', '% User Time', '% DPC Time']
        for item in known_counters:
            self.assertTrue(item in counters)

    def test_list_instances(self):
        instances = win_pdh.list_instances('Processor')
        known_instances = ['0', '_Total']
        for item in known_instances:
            self.assertTrue(item in instances)

    def test_build_counter_list(self):
        counter_list = [
            ('Memory', None, 'Available Bytes'),
            ('Paging File', '*', '% Usage'),
            ('Processor', '*', '% Processor Time'),
            ('Server', None, 'Work Item Shortages'),
            ('Server Work Queues', '*', 'Queue Length'),
            ('System', None, 'Context Switches/sec'),
        ]
        resulting_list = win_pdh.build_counter_list(counter_list)
        for counter in resulting_list:
            self.assertTrue(isinstance(counter, win_pdh.Counter))

        resulting_paths = []
        for counter in resulting_list:
            resulting_paths.append(counter.path)

        expected_paths = [
            '\\Memory\\Available Bytes',
            '\\Paging File(*)\\% Usage',
            '\\Processor(*)\\% Processor Time',
            '\\Server\\Work Item Shortages',
            '\\Server Work Queues(*)\\Queue Length',
            '\\System\\Context Switches/sec']
        self.assertEqual(resulting_paths, expected_paths)

    def test_get_all_counters(self):
        results = win_pdh.get_all_counters('Processor')
        known_counters = [
            '\\Processor(*)\\% Processor Time',
            '\\Processor(*)\\% Idle Time',
            '\\Processor(*)\\DPC Rate',
            '\\Processor(*)\\% Privileged Time',
            '\\Processor(*)\\DPCs Queued/sec',
            '\\Processor(*)\\% Interrupt Time',
            '\\Processor(*)\\Interrupts/sec',
        ]
        for item in known_counters:
            self.assertTrue(item in results)

    def test_get_counters(self):
        counter_list = [
            ('Memory', None, 'Available Bytes'),
            ('Paging File', '*', '% Usage'),
            ('Processor', '*', '% Processor Time'),
            ('Server', None, 'Work Item Shortages'),
            ('Server Work Queues', '*', 'Queue Length'),
            ('System', None, 'Context Switches/sec'),
        ]
        results = win_pdh.get_counters(counter_list)
        expected_counters = [
            '\\Memory\\Available Bytes',
            '\\Paging File(*)\\% Usage',
            '\\Processor(*)\\% Processor Time',
            '\\Server\\Work Item Shortages',
            '\\Server Work Queues(*)\\Queue Length',
            '\\System\\Context Switches/sec'
        ]
        for item in expected_counters:
            self.assertTrue(item in results)

    def test_get_counter(self):
        results = win_pdh.get_counter('Processor', '*', '% Processor Time')
        self.assertTrue('\Processor(*)\\% Processor Time' in results)
