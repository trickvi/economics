# -*- coding: utf-8 -*-

# cpi.py - Consumer Price Index data manipulation, computation and Class
# Copyright (C) 2013 Tryggvi Björgvinsson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import collections
import requests

CPIResult = collections.namedtuple('CPI', 'date value')


class CPI:
    """
    Provides a Pythonic interface to Consumer Price Index data packages
    """

    def __init__(self, country="all"):
        """
        Initialise a CPI instance.
        """

        # Initialise empty data structures
        self.data = collections.ChainMap()

        # Load the data into the data structures
        self.load(country)
        self.country = country

    def load(self, country="all"):
        """
        Load data
        """
        u = ("https://api.worldbank.org/v2/countries/{}/indicators/CPTOTSAXN"
             "?format=json&per_page=10000").format(country)
        r = requests.get(u)
        j = r.json()
        cpi_data = j[1]

        # Loop through the rows of the datapackage with the help of data
        for row in cpi_data:
            # Get the code and the name and transform to uppercase
            # so that it'll match no matter the case
            iso_3 = row["countryiso3code"].upper()
            iso_2 = row["country"]["id"].upper()
            name = row["country"]['value'].upper()
            # Get the date (which is in the field Year) and the CPI value
            date = row['date']
            cpi = row['value']
            for key in [iso_3, iso_2, name]:
                existing = self.data.get(key, {})
                existing[str(date)] = cpi
                if key:
                    self.data[key] = existing

    def get(self, date=datetime.date.today(), country=None):
        """
        Get the CPI value for a specific time. Defaults to today. This uses
        the closest method internally but sets limit to one day.
        """
        if not country:
            country = self.country
        if country == "all":
            raise ValueError("You need to specify a country")
        if not isinstance(date, str) and not isinstance(date, int):
            date = date.year

        cpi = self.data.get(country.upper(), {}).get(str(date))
        if not cpi:
            raise ValueError("Missing CPI data for {} for {}".format(country, date))

        return CPIResult(date=date, value=cpi)
