"""
Grammar.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Define how a grammar and it's productions rules behave.
"""

import string, uuid
from collections import OrderedDict

from graphviz import Digraph


class TreeNode(object):
    children = []
    name = ''

    def __init__(self, name, children=[]):
        self.name = name
        self.children = children


class Grammar(object):
    """
    Holds the grammar for parsing the description.
    """

    # Order of these will matter to the semantics.
    # Colors will be listed from lighter -> darker
    dark_colors = ['red', 'amber', 'copper', 'brown', 'dark', 'ebony', 'black']
    light_colors = ['light', 'yellow', 'pale', 'gold', 'golden', 'tan']
    origin = ['india', 'american', 'european', 'german', 'bohemian', 'belgian', "irish", "baltic"]
    flavors = ['bitter', 'bitterness', 'coffee', 'dry', 'sour', 'chocolate', 'caramel', 'wheat', 'sweet']
    hops = ['hop', 'hops', 'hopped', 'hoppy', 'hoppiness', 'hoppyness']
    malt = ['malty', 'malt', 'maltyness', 'maltiness']

    # Avoid right hand production or case containing more than one terminal such as '<term1> nonterm1 nonterm2'
    # Create another production rule instead.
    _grammar = OrderedDict({
        '<beer>': ['<type_list>'],
        '<type_list>': ['<type> <type_list>', '<type>'],
        '<type>': ['<ales>', '<lager>', '<adj_list> <type>', '<adj>'],
        '<ales>': ['<stouts>', 'ale', 'ales', 'lambic', '<porter>'],
        '<stouts>': ['stout', 'stouts', 'oatmeal', 'oats'],
        '<lager>': ['<pilsner>', 'lager', 'lagers'],
        '<porter>': ['porter', 'porters'],
        '<adj_list>': ['<adj> <adj_list>', '<adj>'],
        '<adj>': ['<color>', '<origin>', '<malt>', '<hops>', '<flavor>', '<epsilon>'],
        '<flavor>': flavors,
        '<hops>': hops,
        '<malt>': malt,
        '<color>': ['<light_colors>', '<dark_colors>'],
        '<light_colors>': light_colors,
        '<dark_colors>': dark_colors,
        '<origin>': origin,
        '<epsilon>': [''],
    })

    terminal_symbols = light_colors + dark_colors + origin + hops + malt + flavors +\
                       ['', 'lager', 'lagers', 'ale', 'ales', 'stout', 'stouts', 'oatmeal', 'oats', 'porter', 'porters']

    @classmethod
    def beer_type_list(cls, value):
        """
        An example of method to handle semantics. Name of method is significant so we can use getattr.
        :param value: Value to define a meaning to.
        :return:
        """
        print("semantics go here", value)

    @classmethod
    def items(cls):
        return cls._grammar.items()


class DescriptionParser(object):
    """
    Builds the parse tree for a description.
    """
    description = ''

    def __init__(self, description):

        # Map punctuation to spaces and upper to lower case
        table = str.maketrans(string.ascii_uppercase + string.punctuation, string.ascii_lowercase + " " * len(string.punctuation))

        self.description = description.translate(table)
        self.tokens = self.description.split()

    def parse(self):

        stack = []
        remaining = self.tokens

        while len(remaining) > 0:
            self.shift(stack, remaining)
            while self.reduce(stack, len(remaining)):
                pass

        # Example of printing the tree
        for e in stack:
            if isinstance(e, TreeNode):
                print_tree(e, '')
                print('\n')

        # Example of rendering the tree to a pdf
        # root = stack[0]
        # dot = Digraph()
        # root_uid = str(uuid.uuid4())
        # dot.node(root_uid, root.name)
        # render_tree(root, dot, root_uid)
        # print(dot.source)
        # dot.render('tree.gv')

    def shift(self, stack, remaining):
        if len(remaining) > 0 and not is_terminal(remaining[0]):
            # Remove any string not in our terminal symbols for now. We may do something with them later.
            remaining.remove(remaining[0])
            remaining.insert(0, '')  # add an epsilon

        stack.append(remaining[0])
        remaining.remove(remaining[0])

    def case_matches_stack(self, case, stack):

        for m in stack:
            if isinstance(m, str) and m in case:
                # If we have a string it is a terminal and if it is in the rule we have a match
                return case, 1
        # We make it here, a tree is present in the stack. Map the strings to a list of strings to match a rule.
        # This could be a combo of terminals and non terminals
        combo = list(map(lambda n: n.name if isinstance(n, TreeNode) else n, stack))
        return (case, len(combo)) if combo == case else (None, None)

    def reduce(self, stack, len_rem):
        for lh, rh in Grammar.items():
            for case in rh:
                case_as_list = [case]
                if lh != '<epsilon>':
                    case_as_list = case.split()
                is_match, match_length = self.case_matches_stack(case_as_list, stack[-len(case_as_list):])
                if is_match:
                    if (lh == '<type_list>' and len_rem is not 0) or (lh == '<beer>' and len(stack) is not 1):
                        continue
                    trees = list(map(lambda c: TreeNode(c) if isinstance(c, str) else c, stack[-match_length:]))
                    stack[-match_length:] = [TreeNode(lh, trees)]
                    return stack
        return None


def print_tree(node, margin='--'):
    print('%s%s' % (margin, node.name))
    margin += '|--'
    for child in node.children:
        print_tree(child, margin)


def is_terminal(node_name):
    return node_name in Grammar.terminal_symbols


def render_tree(node, dot, parent_uid):
    for i, c in enumerate(node.children):
        new_uid = str(uuid.uuid4())
        dot.node(new_uid, c.name if not is_terminal(c.name) else '"%s"' % c.name)
        dot.edge("%s" % parent_uid, new_uid)
        render_tree(c, dot, new_uid)
