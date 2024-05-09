from input_tree_node import Node
from helper_functions import _parse_url, random_choose_with_weights
import random
from collections import deque
import re

class InputTree:

    def __init__(self, grammar, seed, url, verbose):
        """ Constructs a request object.
            
        Args:
          grammar: input grammar for describing the structure
          seed: a value based on which random number is
            generated. It is used for reproducability.

          url: address of the target endpoint
          verbose: a parameter to decide whether messages
            should be displayed.

        Returns:
          the constructed object
        """
        self.nonterminal_node_list = {}
        Node.symbol_counts = {}
        self.root = Node('<start>')
        self.grammar = grammar
        self.seed = seed
        random.seed(seed)
        self.url = url
        self.verbose = verbose
        self.host_header = None

    def build_tree(self, start_node):
        self.nonterminal_node_list[start_node.id] = start_node

        node_queue = deque([start_node])
        while node_queue:
            current_node = node_queue.pop()

            possible_expansions = self.grammar[current_node.symbol]
            chosen_expansion = random_choose_with_weights(possible_expansions)

            for symbol in re.split(Node.RE_NONTERMINAL, chosen_expansion):
                if len(symbol) > 0:
                    new_node = Node(symbol)

                    current_node.children.append(new_node)

                    if not new_node.is_terminal:
                        node_queue.appendleft(new_node)
                        self.nonterminal_node_list[new_node.id] = new_node

        return start_node

    def remove_subtree_from_nodelist(self, start_node):
        """ This function updates the node_list dictionary
            when a node (and as a result its children) are removed.
        """
        if not start_node.is_terminal:
            self.nonterminal_node_list.pop(start_node.id)
            for child in start_node.children:
                self.remove_subtree_from_nodelist(child)

    def tree_to_request(self, partial=False):
        """ This function converts the request 
            object into bytes. 
        """
        self.request = b""
        self.expand_node(self.root)
        if partial:#request in its most basic form -- with placeholder values.
            return self.request

        self.host, self.port, self.authority, self.uri = _parse_url(self.url)
        if self.host_header is None:
            self.host_header = self.authority

        body_length = len(self.request) - self.request.find(b'\r\n\r\n') - 4

        return self.request.replace(b'_URI_', self.uri.encode('utf-8')).replace(b'_HOST_', self.host_header.encode('utf-8')).replace(b'_REQUEST_ID_', str(self.seed).encode('utf-8')).replace(b'_CONTENT_LENGTH_', str(body_length).encode('utf-8'))

    def expand_node(self, node):
        if node.is_terminal:
            self.request += node.symbol.encode('utf-8')
        else:
            for child in node.children:
                self.expand_node(child)

