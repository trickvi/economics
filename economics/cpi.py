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
import pickle
import os

CPIResult = collections.namedtuple('CPI', 'date value')


class CPI:
    """
    Provides a Pythonic interface to Consumer Price Index data packages
    """

    def __init__(self, country="all", data_source=None):
        """
        Initialise a CPI instance.
        
        Parameters:
        - country (str): the country to retrieve data for. Defaults to "all".
        - data_source (str): the data source to use. Currently supported sources are
        "world_bank" (default) and "local_cache".
        """

        # Initialise empty data structures
        self.data = collections.ChainMap()

        # Set data source
        if data_source:
            self.data_source = data_source
        else:
            self.data_source = "world_bank"

        # Load the data into the data structures
        self.load(country)
        self.country = country

    def load(self, country="all"):
        """
        Load data
        
        Parameters:
        - country (str): the country to retrieve data for. Defaults to "all".
        """
        if self.data_source == "world_bank":
            u = ("https://api.worldbank.org/v2/countries/{}/indicators/CPTOTSAXN"
                 "?format=json&per_page=10000").format(country)
            r = requests.get(u)
            try:
                j = r.json()
            except ValueError:
                print("Error parsing data from World Bank API")
                return
            try:
                cpi_data = j[1]
            except IndexError:
                print("Error: No data returned from World Bank API")
                return
            self._store_data(cpi_data)
        elif self.data_source == "local_cache":
            try:
                with open("cpi_data.pkl", "rb") as f:
                    cpi_data = pickle.load(f)
            except FileNotFoundError:
                print("Error: CPI data cache not found")
                return
            self._store_data(cpi_data)
        else:
            raise ValueError("Unrecognized data source: {}".format(self.data_source))

    def _store_data(self, cpi_data):
        """
        Store CPI data in the data attribute
        
        Parameters:
        - cpi_data (list): a list of dictionaries containing the CPI data
        """
        # Loop through the rows of the datapackage with the help of data
        for row in cpi_data:
            # Get the code and the name and transform to uppercase
            # so that it'll match no matter the case
            iso_3 = row["countryiso3code"].upper()
            iso_2 = row["country"]["id"].upper()
            name = row["country"]['value'].upper()
            # Get the date (which is in the field Year) and the CPI value
            date = row['date '] # Note the trailing space in the field name
            cpi = row['value']
            for key in [iso_3, iso_2, name]:
                existing = self.data.get(key, {})
                existing[str(date)] = cpi
                if key:
                    self.data[key] = existing

    def get(self, date=datetime.date.today(), country=None):
        """
        Get the CPI value for a specific time. Defaults to today.
        
        Parameters:
        - date (datetime.date or int or str): the date to retrieve the CPI value for.
        If not provided, defaults to today.
        - country (str): the country to retrieve data for. Defaults to the country
        specified when the CPI instance was created.
        
        Returns:
        - CPIResult: a named tuple with the date and value.
        
        Raises:
        - ValueError: if the data is not available for the specified date and country.
        """
        if not country:
            country = self.country
        if country == "all":
            raise ValueError("You need to specify a country")
        if not isinstance(date, str) and not isinstance(date, int):
            date = date.year

        cpi = self.data.get(country.upper(), {}).get(str(date))
        if not cpi:
            raise ValueError("Missing CPI data for {} for {}".format(
                country, date))

        return CPIResult(date=date, value=cpi)

    def save_cache(self):
        """
        Save the current data to a local cache file
        """
        with open("cpi_data.pkl", "wb") as f:
            pickle.dump(self.data.values(), f)
    
        def clear_cache(self):
        """
        Delete the local cache file
        """
        try:
            os.remove("cpi_data.pkl")
        except FileNotFoundError:
            pass


