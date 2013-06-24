# -*- coding: utf-8 -*-

# datastructures.py - Various helpful datastructures or converters
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

import time

class MapDict(dict):
    """
    Dictionary that allows for multiple keys to the same value
    """

    def __init__(self, mapping={}):
        """
        Initialise the MapDict by creating a key map and interate through a
        provided mapping (or an empty dict if not present)
        """
        self.map = {}
        for k,v in mapping.iteritems():
            self.__setitem__(k,v)
        super(MapDict,self).__init__()

    def __getitem__(self, key):
        """
        Get a value for a key (can be in the key map or the key itself)
        """
        return super(MapDict,self).__getitem__(self.map.get(key, key))
        
    def __setitem__(self, keys, value):
        """
        Set a value for keys. In case keys have an iterator first value is set
        as the main key, the rest are mapped. If the main key is already in the
        key map it is removed from it before proceeding.
        """
        if hasattr(keys, '__iter__'):
            if keys[0] in self.map:
                del self.map[keys[0]]
            for key in keys[1:]:
                self.map[key] = keys[0]
            super(MapDict,self).__setitem__(keys[0],value)
        else:
            super(MapDict,self).__setitem__(keys,value)
        
    def __delitem__(self, key):
        """
        Remove a key and value (along with all mapped keys)
        """
        mappedkey = self.map.get(key, key)
        for k,v in self.map.items():
            if v == mappedkey:
                del self.map[k]
        super(MapDict,self).__delitem__(mappedkey)

    def update(self, mapdict):
        """
        Update the MapDict with another MapDict (update the key map as well)
        """
        self.map.update(mapdict.map)
        return super(MapDict,self).update(mapdict)

