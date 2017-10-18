"""Resolvers based on Twitter user profile data."""


import re
import warnings

from ..names import *
from ..resolver import AbstractResolver, register


STATE_RE = re.compile(r'.+,\s*(\w+)')
NORMALIZATION_RE = re.compile(r'\s+|\W')


def normalize(location_name, preserve_commas=False):
    """Normalize *location_name* by stripping punctuation and collapsing
    runs of whitespace, and return the normalized name."""
    try:
        location_name.encode('ascii')
    except UnicodeEncodeError:
        return location_name
    except UnicodeDecodeError:
        return location_name
    else:
        def replace(match):
            if preserve_commas and ',' in match.group(0):
                return ','
            return ' '
        return NORMALIZATION_RE.sub(replace, location_name).strip().lower()


@register('profile')
class ProfileResolver(AbstractResolver):
    """A resolver that locates a tweet by matching the tweet author's
    profile location against known locations."""

    name = 'profile'

    def __init__(self):
        self.location_name_to_location = {}

    def add_location(self, location):
        aliases = list(location.aliases)
        aliases_already_added = set()
        for alias in aliases:
            if alias in aliases_already_added:
                continue
            #if alias in self.location_name_to_location:
                #warnings.warn('Duplicate location name "%s"' % str(alias))
            else:
                self.location_name_to_location[alias.encode('utf-8')] = location
            # Additionally add a normalized version of the alias
            # stripped of punctuation, and with runs of whitespace
            # reduced to single spaces.
            
            normalized = normalize(alias)
            if normalized != alias:
                aliases.append(normalized)
            aliases_already_added.add(alias)

    def give_location_data(self):
        return(self.location_name_to_location)

    def resolve_tweet(self, tweet):
        import sys
        location_string = tweet.get('user', {}).get('location', '')
        
        if not location_string:
            return None

        normalized = normalize(location_string)

        if normalized in self.location_name_to_location:
            return (False, self.location_name_to_location[normalized])
        
        #Try again splitting commas
        normalized = normalize(location_string, preserve_commas=True)

        splits = normalized.split(', ')

        for s in splits:
            if s in self.location_name_to_location:
                return (False, self.location_name_to_location[s])

        return None
