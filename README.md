# auditor-crawl-cli
Python script to display search results from [Mahoning County Auditor property search](http://oh-mahoning-auditor.publicaccessnow.com/) website.

```
$ python crawl.py "Youngstown state university" --no-vacant-land

Results for "Youngstown state university": 10 Structures 5 Lots

Owner               Address                  Parcel                                                             Url
-------------------------------------------------------------------------------------------------------------------
YOUNGSTOWN STAT     264 CARLTON ST           53-018-0-323.00-0      Property.aspx?mpropertynumber=53-018-0-323.00-0
YOUNGSTOWN STAT     223 COURT ST             53-017-0-175.00-0      Property.aspx?mpropertynumber=53-017-0-175.00-0
YOUNGSTOWN STAT     315 ELM ST               53-003-0-162.00-0      Property.aspx?mpropertynumber=53-003-0-162.00-0
YOUNGSTOWN STAT     315 ELM ST               53-003-0-162.00-T      Property.aspx?mpropertynumber=53-003-0-162.00-T
YOUNGSTOWN STAT     360 GRANT ST             53-076-0-024.00-0      Property.aspx?mpropertynumber=53-076-0-024.00-0
YOUNGSTOWN STAT     369 GRANT ST             53-005-0-420.00-0      Property.aspx?mpropertynumber=53-005-0-420.00-0
YOUNGSTOWN STAT     334 N WATT ST            53-017-0-157.00-0      Property.aspx?mpropertynumber=53-017-0-157.00-0
YOUNGSTOWN STAT     158 W RAYEN AVE          53-003-0-121.00-0      Property.aspx?mpropertynumber=53-003-0-121.00-0
YOUNGSTOWN STAT     525 WICK AVE             53-018-0-147.01-0      Property.aspx?mpropertynumber=53-018-0-147.01-0
YOUNGSTOWN STAT     429 WICK AVE             53-018-0-151.02-0      Property.aspx?mpropertynumber=53-018-0-151.02-0
```

# Installation

1. Clone this repo
2. Install requirements via `pip install -r requirements.txt`

# Usage
Provide a search query and optionally flag for no vacant land.

```
python crawl.py "Youngstown state university" --no-vacant-land
```

# Issues
Currently the auditor site will truncate results over 20 pages in length and randomize the order. 
