economics
=========

**economics** provides a toolkit with economical computations based on
data from `https://api.worldbank.org/v2/countries/all/indicators/CPTOTSAXN`.

Features
--------

-  CPI
-  Inflation (based on CPI by default)

Requirements
------------

-  `requests <https://pypi.org/project/requests/>`

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
    CPI(date=2007, value=76.01874988441)
    >> 
    >> # We're going to work with Iceland so set default country
    >> # (we're creating a new instance but the country variable can be set)
    >> iceland = CPI(country='ISL')
    >>
    >> # Get CPI in 1800 (not in the data)
    >> iceland.get(datetime.date(1800,1,1))
    ...
    ValueError: Missing CPI data for ISL for 1800

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
    5.423904699513575
    >> 
    >> # We can also set the reference year and the country
    >> usa_2007 = Inflation(reference=datetime.date(2007,1,1), country='USA')
    >>
    >> # Get the inflation for 2007 in the United States
    >> usa_2007.get(datetime.date(2011,1,1))
    Inflation(factor=1.1104902566655777, value=0.11049025666557766)

License
-------

economics is available under the GNU General Public License, version 3.
See LICENCE for more details.
