"""
models.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J.Harding

Models pertaining to beers.
"""
import uuid

from django.db import models as m
from django.conf import settings

from description_parser.Grammar import DescriptionParser, DescriptionParseException


class Beer(m.Model):
    """
    Stores information about beer.
    """

    uuid = m.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    calories = m.IntegerField(blank=True, null=True)
    name = m.CharField(max_length=255)
    description = m.TextField(blank=True, null=True)
    abv = m.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    ibu = m.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    api_id = m.CharField(max_length=255, help_text="Unique id of the api the beer was pulled from")
    name_of_api = m.CharField(max_length=255, help_text="Name of the api used to get data.")
    created_at = m.DateTimeField(auto_now_add=True, help_text="Date and time the beer was added to this database")
    beer_learning = m.OneToOneField('beers.BeerLearning', blank=True, null=True, related_name='beer',
                                    on_delete=m.PROTECT)

    def save(self, *args, **kwargs):
        """
        Override the save method to parse a beer's description on save.
        :param args:
        :param kwargs:
        :return:
        """

        if not self.description:
            self.description = ""
        n = DescriptionParser(self.name, {})
        p = DescriptionParser(self.description, n.parse())
        parsed = p.parse()

        if not self.beer_learning:
            self.beer_learning = BeerLearning.objects.create(**parsed)
        else:
            # fields to update are in parsed.keys() and only set to 1
            # The difference between beer_learning.fields and parsed.keys() is set to zero
            zeros = self.beer_learning.learning_fields - parsed.keys()
            for attr in zeros:
                setattr(self.beer_learning, attr, 0)
            for k, v in parsed.items():
                setattr(self.beer_learning, k, v)
            self.beer_learning.save()
        super(Beer, self).save(*args, **kwargs)

    def __str__(self):
        """
        Description: str representation
        :return: self.name
        """
        return self.name


class BeerRating(m.Model):
    """
    Class handles the beer rating
    """
    uuid = m.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.PROTECT)
    beer = m.ForeignKey(Beer, on_delete=m.PROTECT)
    rating = m.PositiveSmallIntegerField()
    description = m.TextField(blank=True, null=True)
    created_at = m.DateTimeField(auto_now_add=True)


class RecentBeer(m.Model):
    """
    Class hnadles the recent beers
    """
    uuid = m.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.PROTECT)
    beer = m.ForeignKey(Beer, on_delete=m.PROTECT)
    created_at = m.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s drank %s" % (self.user.username, self.beer.name)


class RecommendedBeer(m.Model):
    """
    Class that handles recommended beers by assigning recommended beer
    """
    uuid = m.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.PROTECT)
    beer = m.ForeignKey(Beer, on_delete=m.PROTECT)
    created_at = m.DateTimeField(auto_now_add=True)
    agreed = m.BooleanField(default=False)
    percent_match = m.IntegerField(blank=True, null=True)

    def __str__(self):
        """
        __str__ string representation method override
        :return:
        """
        return "%s is recommended for %s" % (self.beer.name, self.user.username)


class BeerLearningManager(m.Manager):
    """
    Beer Learning Manager: Manages the machine learning for the recommended beers
    """
    def beer_descriptions(self):
        """
        Handles the beer descriptions to be used in the beer recommendation algorithm
        :param self:
        :return:
        """
        from django.db import connection
        with connection.cursor() as c:
            try:
                c.execute("""SELECT 
                    bb.id as id,
                    bl.malt,
                    bl.hops,
                    bl.india,
                    bl.america,
                    bl.german,
                    bl.belgium,
                    bl.ireland,
                    bl.europe,
                    bl.bohemian,
                    bl.baltic,
                    bl.coffee,
                    bl.chocolate,
                    bl.caramel,
                    bl.wheat,
                    bl.vanilla,
                    bl.strawberry,
                    bl.almond,
                    bl.coconut,
                    bl.pineapple,
                    bl.plum,
                    bl.mango,
                    bl.orange,
                    bl.peach,
                    bl.toffee,
                    bl.honey,
                    bl.hazelnut,
                    bl.blueberry,
                    bl.banana,
                    bl.pumpkin,
                    bl.tart,
                    bl.sour,
                    bl.sweet,
                    bl.dry,
                    bl.oats,
                    bl.light_colors,
                    bl.dark_colors,
                    bl.bitter,
                    bl.lambic,
                    bl.lager,
                    bl.porter,
                    bl.stouts,
                    bl.ales,
                    bl.melon
                    from beers_beerlearning bl
                    join beers_beer bb ON bl.id = bb.beer_learning_id
                    where bb.beer_learning_id is not NULL and (
                       bl.malt     >= 1 or bl.hops      >= 1 or bl.india        >= 1 or bl.america     >= 1
                    or bl.german   >= 1 or bl.belgium   >= 1 or bl.ireland      >= 1 or bl.europe      >= 1
                    or bl.bohemian >= 1 or bl.baltic    >= 1 or bl.coffee       >= 1 or bl.chocolate   >= 1
                    or bl.caramel  >= 1 or bl. wheat    >= 1 or bl.vanilla      >= 1 or bl.strawberry  >= 1
                    or bl.almond   >= 1 or bl.coconut   >= 1 or bl.pineapple    >= 1 or bl.plum        >= 1
                    or bl.mango    >= 1 or bl.orange    >= 1 or bl.peach        >= 1 or bl.toffee      >= 1
                    or bl.honey    >= 1 or bl.hazelnut  >= 1 or bl.blueberry    >= 1 or bl.banana      >= 1
                    or bl.pumpkin  >= 1 or bl.tart      >= 1 or bl.sour         >= 1 or bl.sweet       >= 1
                    or bl.dry      >= 1 or bl.oats      >= 1 or bl.light_colors >= 1 or bl.dark_colors >= 1
                    or bl.bitter   >= 1 or bl.lambic    >= 1 or bl.lager        >= 1 or bl.porter      >= 1
                    or bl.stouts   >= 1 or bl.ales      >= 1 or bl.melon        >= 1
                    );""")
                col_names = [x.name for x in c.description]
                rows = c.fetchall()
                return rows, col_names
            except Exception:
                pass


class BeerLearning(m.Model):
    """
    !!IMPORTANT
    Any changes to this table need to be reflected in the UserLearningProfile.
    """
    objects = BeerLearningManager()

    uuid = m.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    # Scaled ibu/abv
    scaled_ibu = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    scaled_abv = m.DecimalField(max_digits=4, decimal_places=3, default=0)

    # Malt/Hops
    malt = m.IntegerField(default=0)
    hops = m.IntegerField(default=0)

    # Origin
    india = m.IntegerField(default=0)
    america = m.IntegerField(default=0)
    german = m.IntegerField(default=0)
    belgium = m.IntegerField(default=0)
    ireland = m.IntegerField(default=0)
    europe = m.IntegerField(default=0)
    bohemian = m.IntegerField(default=0)
    baltic = m.IntegerField(default=0)

    # Flavor
    coffee = m.IntegerField(default=0)
    chocolate = m.IntegerField(default=0)
    caramel = m.IntegerField(default=0)
    wheat = m.IntegerField(default=0)
    vanilla = m.IntegerField(default=0)
    strawberry = m.IntegerField(default=0)
    almond = m.IntegerField(default=0)
    coconut = m.IntegerField(default=0)
    pineapple = m.IntegerField(default=0)
    plum = m.IntegerField(default=0)
    mango = m.IntegerField(default=0)
    orange = m.IntegerField(default=0)
    peach = m.IntegerField(default=0)
    toffee = m.IntegerField(default=0)
    melon = m.IntegerField(default=0)
    honey = m.IntegerField(default=0)
    hazelnut = m.IntegerField(default=0)
    blueberry = m.IntegerField(default=0)
    banana = m.IntegerField(default=0)
    pumpkin = m.IntegerField(default=0)
    tart = m.IntegerField(default=0)
    sour = m.IntegerField(default=0)
    sweet = m.IntegerField(default=0)
    dry = m.IntegerField(default=0)
    oats = m.IntegerField(default=0)
    light_colors = m.IntegerField(default=0)
    dark_colors = m.IntegerField(default=0)
    bitter = m.IntegerField(default=0)
    lambic = m.IntegerField(default=0)
    lager = m.IntegerField(default=0)
    porter = m.IntegerField(default=0)
    stouts = m.IntegerField(default=0)
    ales = m.IntegerField(default=0)

    @property
    def learning_fields(self):
        """
        Learning fields used for the model
        :return:
        """
        fields = list(map(lambda f: f.name, self._meta.fields))
        fields.remove('uuid')
        fields.remove('id')
        fields.remove('scaled_abv')
        fields.remove('scaled_ibu')
        return fields


class UserLearningProfile(m.Model):
    """
    This table mirrors BeerLearning but uses Decimals.
    !!IMPORTANT
    Any changes to either table should be reflected in the other.
    """

    uuid = m.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = m.OneToOneField('users.DraughtPicksUser', related_name='learning_profile', on_delete=m.PROTECT)

    # Scaled ibu/abv
    scaled_ibu = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    scaled_abv = m.DecimalField(max_digits=4, decimal_places=3, default=0)

    # Malt/Hops
    malt = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    hops = m.DecimalField(max_digits=4, decimal_places=3, default=0)

    # Origin
    india = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    america = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    german = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    belgium = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    ireland = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    europe = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    bohemian = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    baltic = m.DecimalField(max_digits=4, decimal_places=3, default=0)

    # Flavor
    coffee = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    chocolate = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    caramel = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    wheat = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    vanilla = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    strawberry = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    almond = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    coconut = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    pineapple = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    plum = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    mango = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    orange = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    peach = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    toffee = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    melon = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    honey = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    hazelnut = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    blueberry = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    banana = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    pumpkin = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    tart = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    sour = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    sweet = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    dry = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    oats = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    light_colors = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    dark_colors = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    bitter = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    lambic = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    lager = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    porter = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    stouts = m.DecimalField(max_digits=4, decimal_places=3, default=0)
    ales = m.DecimalField(max_digits=4, decimal_places=3, default=0)

    @property
    def learning_fields(self):
        """
        Learning fields used for the model
        :return:
        """
        fields = list(map(lambda f: f.name, self._meta.fields))
        fields.remove('uuid')
        fields.remove('id')
        return fields

