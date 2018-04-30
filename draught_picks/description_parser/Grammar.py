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


# Set a higher recursion limit or we will get RecursionErrors in large descriptions due to many epsilon
sys.setrecursionlimit(2000)


class TreeNode(object):
    """
    This class instantiates a tree node for the grammar
    """
    children = []
    name = ''

    def __init__(self, name, children=[]):
        """
        This method instantiates a tree node object
        :param name:
        :param children:
        """
        self.name = name
        self.children = children

    def has_children(self):
        """
        This returns true of the tree node has children
        :return:
        """
        return len(self.children) > 0


class Grammar(object):
    """
    Holds the grammar for parsing the description.
    """

    # Order of these will matter to the semantics.
    # Colors will be listed from lighter -> darker
    dark_colors = ['red', 'amber', 'copper', 'brown', 'dark', 'ebony', 'black']
    light_colors = ['light', 'yellow', 'pale', 'gold', 'golden', 'tan']
    america = ['america', 'american']
    india = ['indian', 'india']
    german = ['german', 'germany']
    europe = ['european', 'europe']
    belgium = ['belgium', 'belgian']
    ireland = ['irish', 'ireland']
    other_origin = ['bohemian', "baltic"]
    flavors = ['coffee', 'chocolate', 'wheat', 'vanilla', 'strawberry', 'almond',
               'coconut', 'pineapple', 'plum', 'mango', 'orange', 'peach', 'caramel', 'toffee',
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
        '<type>': ['<ales>', '<lager>', '<adj_list> <type>', '<adj_list>'],
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
        '<origin>': ['<america>', '<india>', '<ireland>', '<german>', '<belgium>', '<europe>', '<other_origin>'],
        '<ireland>': ireland,
        '<belgium>': belgium,
        '<europe>': europe,
        '<german>': german,
        '<america>': america,
        '<india>': india,
        '<other_origin>': other_origin,
        '<epsilon>': [''],
    })

    terminal_symbols = light_colors + dark_colors + other_origin + ireland + belgium + german + america + india + hops + malt + flavors + bitter + oats + dry + sweet + tart + sour +\
                       ['', 'lager', 'lagers', 'ale', 'ales', 'stout', 'stouts', 'oatmeal', 'oats', 'porter', 'porters', 'lambic']

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
    def adj_list_adj(cls, node, store):
        """
        This method adjusts the list adj
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def adj_malt(cls, node, store):
        """
        This method adjusts the malt
        :param node:
        :param store:
        :return:
        """
        store['malt'] = 1
        return store

    @classmethod
    def adj_hops(cls, node, store):
        """
        This method adjusts the hops
        :param node:
        :param store:
        :return:
        """
        store['hops'] = 1
        return store

    @classmethod
    def type_list_type(cls, node, store):
        """
        This method returns the type_list type
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def type_list_type_list(cls, node, store):
        """
        This method returns the type_list type_list
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def type_adj_list(cls, node, store):
        """
        This method adjusts the type list
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def type_ales(cls, node, store):
        """
        This method returns the ale children
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def type_lager(cls, node, store):
        """
        This method returns the lager children
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def type_adj_list_type(cls, node, store):
        """
        This method returns the type adjusts list type
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def adj_origin(cls, node, store):
        """
        This emthod adjusts the origin for the beer
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def origin_america(cls, node, store):
        """
        This sets the origin to america
        :param node:
        :param store:
        :return:
        """
        store['america'] = 1
        return store

    @classmethod
    def origin_india(cls, node, store):
        """
        This sets the origin to india
        :param node:
        :param store:
        :return:
        """
        store['india'] = 1
        return store

    @classmethod
    def origin_german(cls, node, store):
        """
        This sets the origin to germany
        :param node:
        :param store:
        :return:
        """
        store['german'] = 1
        return store

    @classmethod
    def origin_europe(cls, node, store):
        """
        This sets the origin to europe
        :param node:
        :param store:
        :return:
        """
        store['europe'] = 1
        return store

    @classmethod
    def origin_belgium(cls, node, store):
        """
        This sets the origin to belgium
        :param node:
        :param store:
        :return:
        """
        store['belgium'] = 1
        return store

    @classmethod
    def origin_ireland(cls, node, store):
        """
        This sets the origin to ireland
        :param node:
        :param store:
        :return:
        """
        store['ireland'] = 1
        return store

    @classmethod
    def origin_other_origin(cls, node, store):
        """
        This sets an origin to other
        :param node:
        :param store:
        :return:
        """
        term = node.children[0]
        store[term.name] = 1
        return store

    @classmethod
    def adj_flavor(cls, node, store):
        """
        This method adjusts the flavor
        :param node:
        :param store:
        :return:
        """
        term = node.children[0]
        store[term.name] = 1
        return store

    @classmethod
    def adj_tart(cls, node, store):
        """
        This method adjusts the flavor to tart
        :param node:
        :param store:
        :return:
        """
        store['tart'] = 1
        return store

    @classmethod
    def adj_sour(cls, node, store):
        """
        This method adjusts the flavor to sour
        :param node:
        :param store:
        :return:
        """
        store['sour'] = 1
        return store

    @classmethod
    def adj_sweet(cls, node, store):
        """
        This method adjusts the sweetness of the beer
        :param node:
        :param store:
        :return:
        """
        store['sweet'] = 1
        return store

    @classmethod
    def adj_dry(cls, node, store):
        """
        This method adjusts the dryness of the beer
        :param node:
        :param store:
        :return:
        """
        store['dry'] = 1
        return store

    @classmethod
    def type_adj(cls, node, store):
        """
        This method adjusts the type
        :param node:
        :param store:
        :return:
        """
        return cls.call_children(node, store)

    @classmethod
    def adj_epsilon(cls, node, store):
        """
        This method adjusts the epsilon
        :param node:
        :param store:
        :return:
        """
        return store

    @classmethod
    def ales_oats(cls, node, store):
        """
        This method sets the ales' oats
        :param node:
        :param store:
        :return:
        """
        store['oats'] = 1
        return store

    @classmethod
    def color_light_colors(cls, node, store):
        """
        This sets the beer to light color
        :param node:
        :param store:
        :return:
        """
        store['light_colors'] = 1
        return store

    @classmethod
    def color_dark_colors(cls, node, store):
        """
        This sets the beer to a dark color
        :param node:
        :param store:
        :return:
        """
        store['dark_colors'] = 1
        return store

    @classmethod
    def adj_color(cls, node, store):
        """
        This adjusts the beer color
        :param node:
        :param store:
        :return:
        """
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
        """
        This sets it to a lager
        :param node:
        :param store:
        :return:
        """
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
        store['stouts'] = 1
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
        """
        this method calls the children
        :param node:
        :param store:
        :return:
        """
        for c in node.children:
            store = getattr(cls, "_".join([node.name.strip("<>"), c.name.strip("<>")]))(c, store)
        return store

    @classmethod
    def rules(cls):
        """
        This sets the rules for the grammar
        :return:
        """
        return cls._grammar

    @classmethod
    def items(cls):
        """
        This gets the grammar items
        :return:
        """
        return cls._grammar.items()


class DescriptionParseException(Exception):
    """
    This class raises a DescriptionParseException
    """
    def __init__(self, stack):
        """
        Initializes the DescriptionParaseException
        :param stack:
        """
        super().__init__("Stack has %d elements. Should only have one" % len(stack))


class DescriptionParser(object):
    """
    Builds the parse tree for a description.
    """
    description = ''

    def __init__(self, description, initial_store):
        """
        Initializes the Description Parser
        :param description:
        :param initial_store:
        """
        self.initial_store = initial_store

        # Map punctuation to spaces and upper to lower case
        table = str.maketrans(string.ascii_uppercase + string.punctuation, string.ascii_lowercase + " " * len(string.punctuation))

        self.description = description.translate(table)
        self.tokens = self.description.split()

    def parse(self):
        """
        This method parses the grammar
        :return:
        """
        stack = []
        remaining = self.tokens

        while len(remaining) > 0:
            self.shift(stack, remaining)
            while self.reduce(stack, len(remaining)):
                pass
        if len(stack) is 1:
            root = stack[0]
            store = getattr(Grammar, "beer_type_list")(root, self.initial_store)
        elif len(stack) is 0:
            store = {}
        else:
            raise DescriptionParseException(stack)

        return store

    def shift(self, stack, remaining):
        """
        This method shifts the grammar
        :param stack:
        :param remaining:
        :return:
        """
        if len(remaining) > 0 and not is_terminal(remaining[0]):
            # Remove any string not in our terminal symbols for now. We may do something with them later.
            remaining.remove(remaining[0])
            remaining.insert(0, '')  # add an epsilon

        stack.append(remaining[0])
        remaining.remove(remaining[0])

    def case_matches_stack(self, case, stack):
        """
        This method case_matches the stack
        :param case:
        :param stack:
        :return:
        """
        for m in stack:
            if isinstance(m, str) and m in case:
                # If we have a string it is a terminal and if it is in the rule we have a match
                return case, 1
        # We make it here, a tree is present in the stack. Map the strings to a list of strings to match a rule.
        # This could be a combo of terminals and non terminals
        combo = list(map(lambda n: n.name if isinstance(n, TreeNode) else n, stack))
        return (case, len(combo)) if combo == case else (None, None)

    def reduce(self, stack, len_rem):
        """
        This reduces an element in the grammar if requirements are not met
        :param stack:
        :param len_rem:
        :return:
        """
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
    """
    Recursie function to print the tree.
    :param node: TreeNode to process
    :param margin: Left handed margin
    :return: None
    """
    print('%s%s' % (margin, node.name))
    margin += '|--'
    for child in node.children:
        print_tree(child, margin)


def is_terminal(node_name):
    """
    Determines if the string is in our language.
    :param node_name:
    :return: Boolean
    """
    return node_name in Grammar.terminal_symbols


def render_tree(node, dot, parent_uid):
    """
    Recursive function to build the graph for graphviz.
    :param node: TreeNode being processed
    :param dot: Dipraph object from graphviz
    :param parent_uid: UUID of parent
    :return: None
    """
    for i, c in enumerate(node.children):
        new_uid = str(uuid.uuid4())
        dot.node(new_uid, c.name if not is_terminal(c.name) else '"%s"' % c.name)
        dot.edge(parent_uid, new_uid)
        render_tree(c, dot, new_uid)


def render_tree_to_pdf(root):
    """
    Use graphviz to render a tree to a file.
    :param root: root TreeNode
    :return: None
    """
    try:
        from graphviz import Digraph
    except ImportError:
        raise DescriptionParseException("You must have graphviz installed to render a tree.")
    dot = Digraph()
    root_uid = str(uuid.uuid4())
    dot.node(root_uid, root.name)
    render_tree(root, dot, root_uid)
    dot.render('tree.gv')

