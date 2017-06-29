from unittest import TestCase

from consistent_hash.ring import HashRing


class TestRing(TestCase):

    def create_simple_servers(self):
        servers = {'192.168.0.246:11212': 1,
                   '192.168.0.247:11212': 1,
                   '192.168.0.249:11212': 1,
                   '192.168.0.250:11212': 1,
                   '192.168.0.251:11212': 1,
                   '192.168.0.252:11212': 2}
        self.simple_servers = servers.keys()
        ring = HashRing(servers)
        return ring

    def test_get_node(self):
        ring = self.create_simple_servers()
        server = ring.get_node('wade')
        self.assertIn(server, self.simple_servers)
        self.assertEqual(server, ring.get_node('wade'))

    def get_test_string_keys(self):
        text = open('tests/string_keys.txt').read()
        text = text.replace('\n', '').replace('a ', '').replace('an ', '')
        return text.split(',')

    def test_distribution(self):
        counts = {}
        ring = self.create_simple_servers()
        for s in self.simple_servers:
            counts[s] = 0

        def count_word(w):
            counts[ring.get_node(w)] += 1

        test_string_keys = self.get_test_string_keys()

        for string_key in test_string_keys:
            count_word(string_key)

        for s in self.simple_servers:
            self.assertTrue(counts[s] > 0)

    def test_add_nodes(self):
        nodes = {'192.168.0.240:11212': 1,
                 '192.168.0.241:11212': 1
                 }
        ring = self.create_simple_servers()
        ring.add_nodes(nodes)
        self.assertEqual(len(ring.nodes), 8)

    def test_del_nodes(self):
        nodes = ['192.168.0.249:11212',
                 '192.168.0.250:11212']

        ring = self.create_simple_servers()
        self.assertEqual(len(ring.nodes), 6)
        ring.del_nodes(nodes)
        self.assertEqual(len(ring.nodes), 4)

    def test_print(self):
	    print(123)
