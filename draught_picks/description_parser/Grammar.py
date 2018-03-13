"""
Grammar.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Define how a grammar and it's productions rules behave.
"""

import string, uuid, sys
from collections import OrderedDict

from graphviz import Digraph

# Set a higher recursion limit or we will get RecursionErrors in large descriptions due to many epsilon
sys.setrecursionlimit(2000)


class TreeNode(object):
    children = []
    name = ''

    def __init__(self, name, children=[]):
        self.name = name
        self.children = children

    def has_children(self):
        return len(self.children) > 0


class Grammar(object):
    """
    Holds the grammar for parsing the description.
    """

    # Order of these will matter to the semantics.
    # Colors will be listed from lighter -> darker
    dark_colors = ['red', 'amber', 'copper', 'brown', 'dark', 'ebony', 'black']
    light_colors = ['light', 'yellow', 'pale', 'gold', 'golden', 'tan']
    origin = ['india', 'american', 'european', 'german', 'bohemian', 'belgian', "irish", "baltic"]
    flavors = ['coffee', 'chocolate', 'caramel', 'wheat', 'vanilla', 'strawberry', 'almond',
               'coconut', 'pineapple', 'plum','mango', 'orange', 'peach', 'caramel', 'toffee',
               'melon', 'honey', 'hazelnut', 'blueberry', 'banana', 'pumpkin']
    dry = ['dry', 'dryness']
    sour = ['sour', 'sourness']
    sweet = ['sweet', 'sweetness']
    tart = ['tart', 'tartness']
    # malt hopp bitter range, no range just numerical
    hops = ['hop', 'hops', 'hopped', 'hoppy', 'hoppiness', 'hoppyness']
    malt = ['malty', 'malt', 'maltyness', 'maltiness']

    # bitterness- group, coffee individual key with terminal name and increment.
    bitter = ['bitter', 'bitterness']
    oats = ['oats', 'oatmeal']

    # Avoid right hand production or case containing more than one terminal such as '<term1> nonterm1 nonterm2'
    # Create another production rule instead.
    _grammar = OrderedDict({
        '<beer>': ['<type_list>'],
        '<type_list>': ['<type> <type_list>', '<type>'],
        '<type>': ['<ales>', '<lager>', '<adj_list> <type>', '<adj>'],
        '<ales>': ['<stouts>', '<oats>', '<porter>', '<ale_terms>', '<lambic>'],
        '<ale_terms>': ['ale', 'ales'],
        '<lambic>': ['lambic'],
        '<stouts>': ['stout', 'stouts'],
        '<oats>': ['oats', 'oatmeal', 'oat'],
        '<lager>': ['<pilsner>', '<lager_terms>'],
        '<lager_terms>': ['lager', 'lagers'],
        '<porter>': ['porter', 'porters'],
        '<adj_list>': ['<adj> <adj_list>', '<adj>'],
        '<adj>': ['<color>', '<origin>', '<malt>', '<hops>', '<flavor>', '<dry>', '<sweet>', '<sour>', '<tart>', '<bitter>', '<epsilon>'],
        '<flavor>': flavors,
        '<bitter>': bitter,
        '<hops>': hops,
        '<malt>': malt,
        '<dry>': dry,
        '<sweet>': sweet,
        '<sour>': sour,
        '<tart>': tart,
        '<color>': ['<light_colors>', '<dark_colors>'],
        '<light_colors>': light_colors,
        '<dark_colors>': dark_colors,
        '<origin>': origin,
        '<epsilon>': [''],
    })

    terminal_symbols = light_colors + dark_colors + origin + hops + malt + flavors + bitter + oats + dry + sweet + tart + sour +\
                       ['', 'lager', 'lagers', 'ale', 'ales', 'stout', 'stouts', 'oatmeal', 'oats', 'porter', 'porters']

    @classmethod
    def beer_type_list(cls, node, store):
        """
        An example of method to handle semantics. Name of method is significant so we can use getattr.
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def adj_malt(cls, node, store):
        store['malt'] = 1
        return store

    @classmethod
    def adj_hops(cls, node, store):
        store['hops'] = 1
        return store

    @classmethod
    def type_list_type(cls, node, store):
        return cls.call_children(node, store)

    @classmethod
    def type_list_type_list(cls, node, store):
        return cls.call_children(node, store)

    @classmethod
    def type_adj(cls, node, store):
        return cls.call_children(node, store)

    @classmethod
    def type_ales(cls, node, store):
        return cls.call_children(node, store)

    @classmethod
    def type_lager(cls, node, store):
        return cls.call_children(node, store)

    @classmethod
    def type_adj_list_type(cls, node, store):
        return cls.call_children(node, store)

    @classmethod
    def adj_origin(cls, node, store):
        term = node.children[0]
        store[term.name] = 1
        return store

    @classmethod
    def adj_flavor(cls, node, store):
        term = node.children[0]
        store[term.name] = 1
        return store

    @classmethod
    def adj_tart(cls, node, store):
        store['tart'] = 1
        return store

    @classmethod
    def adj_sour(cls, node, store):
        store['sour'] = 1
        return store

    @classmethod
    def adj_sweet(cls, node, store):
        store['sweet'] = 1
        return store

    @classmethod
    def adj_dry(cls, node, store):
        store['dry'] = 1
        return store

    @classmethod
    def type_adj(cls, node, store):
        return cls.call_children(node, store)

    @classmethod
    def adj_epsilon(cls, node, store):
        return store

    @classmethod
    def ales_oats(cls, node, store):
        store['oats'] = 1
        return store

    @classmethod
    def color_light_colors(cls, node, store):
        store['light_colors'] = 1
        return store

    @classmethod
    def color_dark_colors(cls, node, store):
        store['dark_colors'] = 1
        return store

    @classmethod
    def adj_color(cls, node, store):
        return cls.call_children(node, store)


    @classmethod
    def adj_bitter(cls, node, store):
        """
        A rule that only goes to terminals applies the semantics.
        :param node:
        :param store:
        :return:
        """
        store['bitter'] = 1
        return store

    @classmethod
    def ales_lambic(cls, node, store):
        """
        A rule that only goes to terminals applies the semantics.
        :param node:
        :param store:
        :return:
        """
        store['lambic'] = 1
        return store

    @classmethod
    def lager_lager_terms(cls, node, store):
        store['lager'] = 1
        return store

    @classmethod
    def ales_porter(cls, node, store):
        """
        A rule that only goes to terminals applies the semantics.
        :param node:
        :param store:
        :return:
        """
        store['porter'] = 1
        return store

    @classmethod
    def ales_stouts(cls, node, store):
        """
        A rule that only goes to terminals applies the semantics.
        :param node:
        :param store:
        :return:
        """
        store['stouts'] =  1
        return store

    @classmethod
    def ales_ale_terms(cls, node, store):
        """
        A rule that only goes to terminals applies the semantics.
        :param node:
        :param store:
        :return:
        """
        store['ales'] = 1
        return store

    @classmethod
    def call_children(cls, node, store):
        for c in node.children:
            store = getattr(cls, "_".join([node.name.strip("<>"), c.name.strip("<>")]))(c, store)
        return store

    @classmethod
    def rules(cls):
        return cls._grammar

    @classmethod
    def items(cls):
        return cls._grammar.items()


class DescriptionParseException(Exception):

    def __init__(self, stack):
        super().__init__("Stack has %d elements. Should only have one" % len(stack))


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
        # for e in stack:
        #     if isinstance(e, TreeNode):
        #         print_tree(e, '')
        #         print('\n')

        if len(stack) is 1:
            root = stack[0]
            # store = {}
            # for c in root.children:
            store = getattr(Grammar, "beer_type_list")(root, {})
            print("FINISH", store)
        else:
            raise DescriptionParseException(stack)

        # Example of rendering the tree to a pdf
        # root = stack[0]
        # dot = Digraph()
        # root_uid = str(uuid.uuid4())
        # dot.node(root_uid, root.name)
        # render_tree(root, dot, root_uid)
        # print(dot.source)
        # dot.render('tree.gv')
        return store

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
