import hashlib
import bisect


class HashRing(object):

    def __init__(self, node_dict):
        self.ring = dict()
        self.keys = []
        self.key_node = {}
        self.nodes = []
        self.node_index = 0
        self.weight = {}

        self.add_nodes(node_dict)

    def del_nodes(self, nodes, hook_func=None):
        for node in nodes:
            if node not in self.nodes:
                continue

            for key in self._node_keys(node):
                self.keys.remove(key)
                del self.key_node[key]

        self.node_index -= 1
        self.nodes.remove(node)

    def add_nodes(self, node_dict, hook_func=None):
        self.nodes.extend(node_dict.keys())
        self.weight.update(node_dict.copy())
        self._update_ring(start=self.node_index)
        self.node_index = self.get_nodes_cnt()
        self.keys.sort()

    def get_node(self, string_key):
        """ return the corresponding node in the hash ring of the given
        string_key
        """
        pos = self.get_node_pos(string_key)
        if pos is None:
            return None
        return self.key_node[self.keys[pos]]

    def get_node_pos(self, string_key):
        if not self.key_node:
            return None
        key = self.gen_key(string_key)
        pos = bisect.bisect(self.keys, key)
        if pos == len(self.keys):
            return 0
        return pos

    def _update_ring(self, start=0):
        for node in self.nodes[start:]:
            for key in self._node_keys(node):
                self.keys.append(key)
                self.key_node[key] = node

    def _node_keys(self, node):
        virtual_cnts = self.VIRTUAL_CNT * self.weight[node]
        for i in range(0, virtual_cnts):
            b_key = self._hash_digest('%s-%s' % (node, i))
            for i in range(4):
                yield self._hash_val(b_key, lambda x: x + i * 4)

    def _hash_val(self, b_key, entry_fn):
        return ((b_key[entry_fn(3)] << 24) |
                (b_key[entry_fn(2)] << 16) |
                (b_key[entry_fn(1)] << 8) |
                b_key[entry_fn(0)])

    def _hash_digest(self, key):
        m = hashlib.md5()
        m.update(bytes(key, 'utf-8'))
        return list(map(int, m.digest()))
