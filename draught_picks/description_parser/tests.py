"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J.Harding

Tests for the parser.
"""

from django.test import TestCase

from .Grammar import DescriptionParser, TreeNode

class TestParser(TestCase):

    def setUp(self):
        self.parser = DescriptionParser("I like indian lagers stouts and light/dark american ales baltic")
        # self.parser = DescriptionParser("In April 2013 we inked a deal with ArtPrize that made us the official brewery of the competition for the next five years. The premier leadership sponsorship deal included offering our beer at all official ArtPrize events, signage, promotion, merchandise, specialized glassware and other items. It also included permission for us to use the ArtPrize identity marks (logo and graphics) on any co-packaged items, including beer. We plan to release a new beer for each year of our five-year partnership with ArtPrize under the name “Artist Series”. This is year two. Last year’s release was Inspired Artist Black IPA._x000D_\n_x000D_\n“Making a unique beer in honor of ArtPrize has become a fun challenge for our brewers,” said Dave Engbers, our co-founder and vice president of brand and education. “This year’s release just fell into place. Ninkasi—a stained glass ArtPrize submission that showed in our taproom last year—became a permanent part of our taproom when we purchased it last year. We knew right away that it would make a perfect label for Mosaic Promise, a beautifully simple beer that we had been experimenting with for some time.”_x000D_\n_x000D_\nMosaic Promise showcases a single malt—Golden Promise—and a single hop—Mosaic. The traditional barley’s depth of flavor and the versatility of the hops’ bittering, flavor and aroma characteristics are the strong pillars that comprise the structure of this clean, rich, golden beer. We can brew complex beers with the best of them, but we recognize that there’s also beauty in simplicity. The beer clocks in at 5.5% ABV and 50 IBUs._x000D_\n_x000D_\nProceeds from the sale of Mosaic Promise will support the future programming of the ArtPrize organization. ArtPrize is an international art competition, open to any artist and decided by public vote. Its mission is to promote critical dialogue and collaboration through new, creative ideas among a large and diverse population of people. As an innovator in redefining what beer can be, we believe that experimentation is central to the human experience—whether one experiments with grains and hops or colored glass and light—and that sharing one’s creation with the public is a brave act worth celebrating._x000D_\n_x000D_\n“Founders is an iconic brand producing a sublime range of exquisite beers in our own Grand Rapids,” said Christian Gaines, executive director of ArtPrize. “We’re honored and elated to count Founders as the ArtPrize Official Brewery and to include Mosaic Promise as the latest special release beer—one that’s emblematic of our strong partnership and shared commitment to art, artists and community.”_x000D_\n_x000D_\nMore than 400,000 people are expected to attend ArtPrize 2014._x000D_\n_x000D_\nWe also partnered with ArtPrize to launch ArtPrize on Tap, the newest ArtClub membership perk. From the patios of the Centennial Room, our private second-floor entertainment space, ArtPrize on Tap offers ArtClub members the opportunity to connect year-round and stay on the ArtPrize insider track, while enjoying Founders food and beer. We will premiere Mosaic Promise at the August installment of ArtPrize on Tap. Held on the third Wednesday of every month, ArtPrize on Tap is free for ArtClub members, and friends of ArtPrize and Founders can join for $10. To learn more, go to artprize.org/artclub._x000D_\n_x000D_\nMosaic Promise will be available for a limited time starting on Sunday, September 14, across our Michigan, Wisconsin, metro NYC and Chicagoland distribution footprint. It will be released in our taproom on draft and in bottles starting on Tuesday, September 16. There will be an event in our taproom featuring the artists and introducing the beer from 4:30-6:30pm that day. One-of-a-kind Mosaic Promise posters will be given away, while supplies last. Mosaic Promise will also be featured at official ArtPrize events._x000D_\n_x000D_\nThis year marks the sixth edition of ArtPrize, which will take place Sept. 24–Oct. 12, 2014. Our taproom will be a venue for the sixth year running.")
        # self.parser = DescriptionParser("""Our first beer has been aptly named ""633"" after the Regions telephone exchange for starters.  ""If I could call a beer home, this would be the one."" ~ Win

# It is a mildly hoppy pale ale using a 2 row, vienna, and munich malts for body,color, and head retention. It is hopped with American west coast hops later in the boil giving it a nice citrus hop flavor and very mild aroma. Slight addition of a roasted caramel malt gives ""633"" it's signature 'sunset over the harbor glow'.""")

    def test_shift(self):

        stack = []
        self.parser.shift(stack, self.parser.tokens)
        self.assertEqual(stack, [''])
#        self.assertEqual(self.parser.tokens, ['like', 'lagers', 'stouts','stouts'])
        # self.assertEqual(self.parser.tokens, ['like', 'india', 'pale', 'ales', 'brown', 'lagers', 'and', 'dark', 'stouts'])

    def test_init(self):
        a_parser = DescriptionParser("American-style lagers and ales")

        self.assertEqual(a_parser.description, "american style lagers and ales")
        self.assertEqual(a_parser.tokens, ["american", "style", "lagers", "and", "ales"])

    def test_case_matches_stack_with_strings_only(self):
        # Arrange
        stack = ['lager']
        case = ['<adj_list>', 'lager']

        # Act
        result, match = self.parser.case_matches_stack(case, stack)

        # Assert
        self.assertTrue(result is case)
        self.assertEqual(match, 1)

    def test_case_matches_stack_with_non_terms_and_strings(self):
        # Arrange
        stack = [TreeNode('<adj_list>'), 'lager']
        case = ['<adj_list>', 'lager']

        # Act
        (result, match) = self.parser.case_matches_stack(case, stack)

        # Assert
        self.assertTrue(result is case, result)
        self.assertEqual(match, 1)

        # Arrange
        stack = [TreeNode('<type>'), TreeNode('<type_list>')]
        case = ['<type>', '<type_list>']

        # Act
        result, match = self.parser.case_matches_stack(case, stack)

        # Assert
        self.assertTrue(result is case, "%s %s" % (result, case))
        self.assertEqual(match, 2)

    def test_reduce(self):
        # Arrange
        stack = ["lagers"]

        # Act
        self.parser.reduce(stack, 1)

        # Assert it should parse the right most symbol to a tree
        self.assertTrue(isinstance(stack[0], TreeNode) and stack[0].name == "<lager_terms>", stack[0].name)
        stack.append("stouts")
        self.parser.reduce(stack, 0)
        self.assertTrue(isinstance(stack[1], TreeNode) and stack[1].name == "<stouts>", stack[1].name)

    def test_parse(self):
        store = self.parser.parse()
        print(store)
