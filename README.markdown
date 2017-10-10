# Carmen

A Python version of [Carmen](https://github.com/mdredze/carmen),
a library for geolocating tweets.

Given a tweet, Carmen will return `Location` objects that represent a
physical location.
Carmen uses both coordinates and other information in a tweet to make
geolocation decisions.
It's not perfect, but this greatly increases the number of geolocated
tweets over what Twitter provides.

To install, simply run:

    $ python setup.py install

To run the Carmen frontend, see:

    $ python -m carmen.cli --help

This version has been modified my Conservation International to include the following changes:
* Only matches from the users profile (other resolvers will likely not work)
* Only returns the country for a toponym (not the lat/long)
* Includes a vastly expanded database with all cities over 20k people, all countries, admin 1 and admin 2 names, as well as extensive alternate spellings and names for a given toponym.
* Works with unicode, allowing geocoding user locations that are not ascii.
