# -*- coding: utf-8 -*-

# inflation.py - Inflation computations and class
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
import economics

InflationResult = collections.namedtuple('Inflation', 'factor value')


class Inflation(object):
    """
    Object to provide simple inflation computational functions
    """

    def __init__(self, reference=None, country="all", data_source=None):
        """
        Create a new Inflation instance using the CPI class. Optional
        parameters are source which defaults to economics.CPI class, 
        reference date (datetime.date), country (name or code), and data_source
        (str).
        
        Parameters:
        - reference (datetime.date or int or str): the reference date to use.
        If not provided, the current year will be used.
        - country (str): the country to retrieve data for. Defaults to "all".
        - data_source (str): the data source to use. Currently supported sources are
        "world_bank" (default) and "local_cache".
        """
        
        # Create a new data source from the source
        self.data = economics.CPI(country=country, data_source=data_source)

        # Set reference and country based on parameters
        if not reference:
            self.reference = datetime.date.today().year
        elif isinstance(reference, datetime.date):
            self.reference = reference.year
        else:
            self.reference = reference
        self.country = country if country != "all" and country else None

    @staticmethod
    def _compute_inflation(value, reference_value):
        """
        Helper function to compute the inflation/deflation based on a value and
        a reference value
        
        Parameters:
        - value (float): the value to compute inflation/deflation for.
        - reference_value ( float): the reference value to use.
        def get(self, target=datetime.date.today(), reference=None, country=None):
        """
        Get the inflation/deflation value change for the target date based 
        on the reference date.
        
        Parameters:
        - target (datetime.date or int or str): the date to compute the inflation/deflation for.
        If not provided, defaults to today.
        - reference (datetime.date or int or str): the reference date to use.
        If not provided, the reference date specified when the Inflation instance
        was created will be used.
        - country (str): the country to retrieve data for. Defaults to the country
        specified when the Inflation instance was created.
        
        Returns:
        - InflationResult: a named tuple with the factor and value.
        
        Raises:
        - ValueError: if the data is not available for the specified dates and country.
        """

        # Set country & reference to object's country & reference respectively
        reference = self.reference if reference is None else reference
        country = self.country if country is None else country

        # Get the reference and target indices (values) from the source
        reference_value = self.data.get(reference, country).value
        target_value = self.data.get(target, country).value

        # Compute the inflation value and return it
        return self._compute_inflation(target_value, reference_value)

    def inflate(self, amount, target=datetime.date.today(), reference=None,
                country=None):
        """
        Inflate a given amount to the target date from a reference date (or
        the object's reference year if no reference date is provided) in a
        given country (or objects country if no country is provided). The
        amount has to be provided as it was valued in the reference year.
        
        Parameters:
        - amount (float): the amount to
         def get_rate(self, target=datetime.date.today(), reference=None, country=None):
        """
        Get the inflation rate for the target date based on the reference date.
        
        Parameters:
        - target (datetime.date or int or str): the date to compute the inflation rate for.
        If not provided, defaults to today.
        - reference (datetime.date or int or str): the reference date to use.
        If not provided, the reference date specified when the Inflation instance
        was created will be used.
        - country (str): the country to retrieve data for. Defaults to the country
        specified when the Inflation instance was created.
        
        Returns:
        - float: the inflation rate as a percentage.
        
        Raises:
        - ValueError: if the data is not available for the specified dates and country.
        """
        inflation = self.get(target, reference, country)
        return inflation.value * 100

    def compare_countries(self, country_1, country_2, target=datetime.date.today(),
                          reference=None):
        """
        Compare the inflation rates of two countries for a given target date and reference date.
        
        Parameters:
        - country_1 (str): the name or code of the first country to compare.
        - country_2 (str): the name or code of the second country to compare.
        - target (datetime.date or int or str): the date to compute the inflation rate for.
        If not provided, defaults to today.
        - reference (datetime.date or int or str): the reference date to use.
        If not provided, the reference date specified when the Inflation instance
        was created will be used.
        
        Returns:
        - tuple: a tuple with two elements, the first is the inflation rate for country_1 and
        the second is the inflation rate for country_2.
        
        Raises:
        - ValueError: if the data is not available for the specified dates and countries.
        """
        rate_1 = self.get_rate(target, reference, country_1)
        rate_2 = self.get_rate(target, reference, country_2)
        return (rate_1, rate_2)

