economics
=========

**economics** provides a toolkit with economical computations based on
data from `data.okfn.org <http://data.okfn.org/data>`__.

Features
--------

-  CPI
-  Inflation (based on CPI by default)

Requirements
------------

-  `datapackage <https://pypi.python.org/pypi/datapackage/>`__

CPI
---

::

    >> from economics import CPI
    >> import datetime
    >>
    >> # Create a new CPI instance
    >> cpi = CPI()
    >>
    >> # Get CPI for Iceland in 2007
    >> cpi.get(datetime.date(2007,1,1), 'Iceland')
    CPI(date=datetime.date(2007, 1, 1), value=112.07753358)
    >> 
    >> # We're going to work with Iceland so set default country
    >> # (we're creating a new instance but the country variable can be set)
    >> iceland = CPI(country='Iceland')
    >>
    >> # Get CPI in 2012 (not in the data)
    >> iceland.get(datetime.date(2012,1,1))
    ...
    KeyError: 'Date 2012-01-01 not found in data'
    >>
    >> # Get the closest CPI value sintead
    >> iceland.closest(datetime.date(2012,1,1))
    CPI(date=datetime.date(2011, 1, 1), value=155.03663004)

Inflation
---------

::

    >> from economics import Inflation
    >> import datetime
    >>
    >> # Create a new Inflation instance
    >> inflation = Inflation()
    >>
    >> # How many US $ would I need in 2011 to pay for what cost $5 in 2007
    >> inflation.inflate(5, datetime.date(2011,1,1), datetime.date(2007,1,1), 'United States')
    5.424340332378624
    >> 
    >> # We can also set the reference year and the country
    >> usa_2007 = Inflation(reference=datetime.date(2007,1,1), country='United States')
    >>
    >> # Get the inflation for 2007 in the United States
    >> usa_2007.get(datetime.date(2011,1,1))
    Inflation(factor=1.0848680664757249, value=0.08486806647572484)

License
-------

economics is available under the GNU General Public License, version 3.
See LIENCE for more details.
