[![Build Status](https://travis-ci.org/pylipp/financeager.svg?branch=master)](https://travis-ci.org/pylipp/financeager)
[![Coverage Status](https://coveralls.io/repos/github/pylipp/financeager/badge.svg?branch=master)](https://coveralls.io/github/pylipp/financeager?branch=master)

FINANCEAGER
===========

A command line application (possibly interacting with a Flask webservice) that helps you administering your daily expenses and earnings.

The `financeager` backend holds a database containing 'periods'. A period consists of entries of a certain year.

Who is this for?
----------------
You might be someone who wants to organize finances with a simple software because you're tired of Excel and the like. And you like the command line. And Python.

NOTE
----
You're currently on the `master` branch which is under active development.

GENERAL USAGE
-------------
## Installation

### From PyPI package

    pip install financeager

### From source

Create a virtual environment

    mkvirtualenv --python=$(which python3) financeager

Clone the repo

    git clone https://github.com/pylipp/financeager

Install

    cd financeager
    make install

Alternatively, you can omit the first step and install `financeager` to `~/.local` with (requires `pip3`)

    pip3 install -r requirements.txt . --user

## Testing

You're invited to run the tests from the root directory:

    git clone https://github.com/pylipp/financeager
    cd financeager
    make test

### Client-server or serverless mode?

You can run `financeager` as a client-server or a serverless application (default). This can be controlled by the configuration file at `~/.config/financeager/config`.

In either mode, you can configure frontend options, that is the name of the default category (assigned when omitting the category option when e.g. adding an entry) and the date format (string that `datetime.strptime` understands; note the double percent).

Default config:

    [FRONTEND]
    default_category = unspecified
    date_format = %%m-%%d

To run `financeager` as client-server application, specify a the server-sided configuration like this

    [SERVICE]
    name = flask

    [SERVICE:FLASK]
    host = 0.0.0.0

You can launch the server via `financeager start` or by wrapping the `app = fflask.create_app()` in a WSGI.

On the client side, you want to put something along the lines of

    [SERVICE]
    name = flask

    [SERVICE:FLASK]
    host = foo.pythonanywhere.com
    timeout = 10
    username = foouser
    password = S3cr3t

This specifies the timeout for HTTP requests and username/password for basic auth, if required by the server.

### Command line usage

```
usage: financeager [-h] {add,get,rm,update,copy,print,list} ...

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {add,start,get,rm,update,copy,print,list}
                        list of available subcommands
    add                 add an entry to the database
    get                 show information about single entry
    rm                  remove an entry from the database
    update              update one or more fields of an database entry
    copy                copy an entry from one period to another
    print               show the period database
    list                list all databases
```

On the client side, `financeager` provides the following commands to interact with the database: `add`, `update`, `rm`, `get`, `print`, `list`, `copy`.

*Add* earnings (no/positive sign) and expenses (negative sign) to the database:

    > financeager add burgers -19.99 --category Restaurants
    > financeager add lottery 123.45 --date 03-14

Category and date can be optionally specified. They default to None and the current day's date, resp. `financeager` will try to derive the entry category from the database if not specified. If several matches are found, the default category is used.

*Add recurrent* entries using the `-t recurrent` flag (`t` for table name) and specify the frequency (yearly, half-yearly, quarterly, bi-monthly, monthly, weekly, daily) with the `-f` flag and optionally start and end date with the `-s` and `-e` flags, resp.

    > financeager add rent -500 -t recurrent -f monthly -s 01-01 -c rent

If not specified, the start date defaults to the current date and the end date to the last day of the database's year.

Did you make a mistake when adding a new entry? *Update* one or more fields by calling the 'update' command with the entry's ID and the respective corrected fields:

    > financeager update 1 --name "McKing Burgers" --value -18.59

*Remove* an entry by specifying its ID (visible in the output of the `print` command). This removes the `burgers` entry:

    > financeager rm 1

This would remove the recurrent rent entries (ID is also 1 because standard and recurrent entries are stored in separate tables):

    > financeager rm 1 --table-name recurrent

Show a side-by-side *overview* of earnings and expenses (filter date and/or category by providing the `-d` and `-c` flag and/or filter the name by providing a positional argument)

    > financeager print

                   Earnings               |                Expenses
	Name               Value    Date  ID  | Name               Value    Date  ID
	Unspecified          123.45           | Rent                1500.00
	  Lottery            123.45 03-14   2 |   Rent January       500.00 01-01   1
	                                      |   Rent February      500.00 02-01   1
                                          |   Rent March         500.00 03-01   1
	=============================================================================
	Total                123.45           | Total               1500.00

The aforementioned `financeager` commands operate on the default database (named by the current year, e.g. 2017) unless another period is specified by the `--period` flag.

	> financeager add xmas-gifts -42 --date 12-23 --period 2016

*Copy* an entry from one database to another by specifying entry ID and source/destination period:

    > financeager copy 1 --source 2017 --destination 2018

Detailed information is available from

	> financeager --help
	> financeager <subcommand> --help

### More Goodies

- `financeager` will store requests if the server is not reachable (the timeout is configurable). The offline backup is restored the next time a connection is established. This feature is online available when running financeager with flask.

### Expansion

Want to use a different database? Should be straightforward by deriving from `Period` and implementing the `_entry()` methods. Modify the `Server` class accordingly to use the new period type.

KNOWN BUGS
----------
- Please. Report. Them.

FUTURE FEATURES
---------------
- [ ] experiment with urwid for building TUI or remi for HTML-based GUI
- [ ] support querying of standard/recurrent table with `print`

IMPLEMENTED FEATURES
---------------
- [x] recurrent entries
- [x] stacked layout for `print`
- [x] detect category from entry name (category cache)
- [x] allow filtering of specific date, name, etc. for `print`
- [x] use flask for REST API
- [x] always show entry ID when `print`ing
- [x] specify date format as `MM-DD`
- [x] validate user input prior to inserting to database
- [x] support `get` command
- [x] support 'updating' of entries
- [x] sort `print` output acc. to entry name/value/date/category
- [x] refactor config module (custom method to intuitively retrieve config parameters)
- [x] `copy` command to transfer recurrent entries between period databases
- [ ] return element ID as response to add/copy/update request
- [ ] support passing multiple elements IDs to update/rm/copy/get

DISCARDED FEATURE IDEAS
-----------------------
- select from multiple options if possible (e.g. when searching or deleting an entry): breaks the concept of having a single request-response action. Instead, the user is expected to know which element he wants to delete (by using the element ID) and can give a precise command

DEVELOPER'S TODOs
-----------------
- [x] refactor TinyDbPeriod (return Model strings)
- [x] improve documentation (period module)
- [x] create Python package
- [x] set up Travis CI
- [ ] use logging module instead of print
- [x] drop PyQt dependency for schematics package
- [x] allow remove elements by ID only
- [x] specify CL option to differ between removing standard and recurrent element
- [x] refactor `entries` module (no dependency on schematics package)
- [x] consistent naming (recurrent instead of repetitive)
- [x] increase code coverage
- [ ] refactor period module (separate database member of TinyDbPeriod instead of subclassing, no use of CONFIG_DIR)
- [ ] use marshmallow package for keyword validation in period and webservice
- [ ] refactor some modules (e.g. split fflask and server)

PERSONAL NOTE
-------------
This is a 'sandbox' project of mine. I'm exploring and experimenting with databases, data models, server applications (`Pyro4` and `flask`), frontends (command line, Qt-based GUI), software architecture and general Python development.

Feel free to browse the project and give feedback (comments, issues, pull requests).
