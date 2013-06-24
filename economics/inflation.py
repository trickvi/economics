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

class Inflation(object):
    """
    Object to provide simple inflation computational functions
    """

    def __init__(self, source=economics.CPI, reference=None, country=None):
        """
        Create a new Inflation instance using the CPI class. Optional
        parameters are source which defaults to economics.CPI class, 
        reference date (datetime.date), country (name or code).
        """
        
        # Create a new data source from the source
        self.data = source(country=country)

        # Set reference and country based on parameters
        self.reference = reference

    def _compute_inflation(self, value, reference_value):
        """
        Helper function to compute the inflation/deflation based on a value and
        a reference value
        """
        return collections.namedtuple('Inflation', 'factor value')\
            ._make((value / float(reference_value),
                    (value - reference_value) / float(reference_value)))

    def get(self, target=datetime.date.today(), reference=None, country=None):
        """
        Get the inflation/deflation value change for the target date based 
        on the reference date. Target defaults to today and the instance's
        reference and country will be used if they are not provided as
        parameters
        """

        # Set country & reference to object's country & reference respectively
        reference = self.reference if reference is None else reference

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
        """

        # Get the inflation for the two dates and country
        inflation = self.get(target, reference, country)
        # Return the inflated/deflated amount
        return amount * inflation.factor
