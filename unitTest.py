import unittest
from SystemMonitor import get_cpu_usage, get_memory_utilization


class MonitoringTests(unittest.TestCase):

    def test_get_cpu_usage(self):
        cpu_usage = get_cpu_usage()
        self.assertIsInstance(cpu_usage, float)
        self.assertGreaterEqual(cpu_usage, 0)
        self.assertLessEqual(cpu_usage, 100)

    def test_get_memory_utilization(self):
        memory_utilization = get_memory_utilization()
        self.assertIsInstance(memory_utilization, float)
        self.assertGreaterEqual(memory_utilization, 0)
        self.assertLessEqual(memory_utilization, 100)


if __name__ == '__main__':
    unittest.main()
