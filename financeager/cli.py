# -*- coding: utf-8 -*-
"""
Module containing command line interface to financeager backend.
"""
from __future__ import unicode_literals, print_function

import argparse
import traceback

from financeager import offline, communication


def main(**kwargs):
    """Main entry point of the application. If used from the command line, all
    arguments and options are parsed and passed.
    On the other hand this method can be used in scripts. Kwargs have to be
    passed analogously to what the command line interface would accept (consult
    the help via `financeager [command] --help`), e.g. `{"command": "add",
    "name": "champagne", "value": "99"}.
    """

    cl_kwargs = kwargs or vars(_parse_command())

    command = cl_kwargs.pop("command")
    communication_module = communication.module()

    if command == "start":
        communication_module.launch_server()
        return

    proxy = communication_module.proxy()
    try:
        communication.run(proxy, command, **cl_kwargs)
        offline.recover(proxy)
    except (communication_module.CommunicationError) as e:
        print("Error running command '{}':\n{}".format(
            command, traceback.format_exc()))
        offline.add(command, **cl_kwargs)


def _parse_command():
    parser = argparse.ArgumentParser()

    period_args = ("-p", "--period")
    period_kwargs = dict(default=None, help="name of period to modify or query")

    subparsers = parser.add_subparsers(title="subcommands", dest="command",
            help="list of available subcommands")

    add_parser = subparsers.add_parser("add",
            help="add an entry to the database")

    add_parser.add_argument("name", help="entry name")
    add_parser.add_argument("value", type=float, help="entry value")
    add_parser.add_argument("-c", "--category", default=None,
            help="entry category")
    add_parser.add_argument("-d", "--date", default=None, help="entry date")

    add_parser.add_argument("-r", "--repetitive", default=[],
            nargs=argparse.REMAINDER, help="entry is repeated with given frequency,\
                    from start date to end date (optional)")

    add_parser.add_argument(*period_args, **period_kwargs)

    start_parser = subparsers.add_parser("start", help="start period server")

    rm_parser = subparsers.add_parser("rm",
            help="remove an entry from the database")
    rm_parser.add_argument("name", help="entry name")
    rm_parser.add_argument(*period_args, **period_kwargs)

    print_parser = subparsers.add_parser("print",
            help="show the period database")
    print_parser.add_argument("name", nargs="?", default=None,
            help="only entries containing 'name' (omitting prints all)")
    print_parser.add_argument("-c", "--category", default=None,
            help="only entries containing 'category'")
    print_parser.add_argument("-d", "--date", default=None,
            help="only entries containing 'date'")
    print_parser.add_argument("-s", "--stacked-layout", action="store_true",
            help="if true, display earnings and expenses in stacked layout, otherwise side-by-side")
    print_parser.add_argument(*period_args, **period_kwargs)

    list_parser = subparsers.add_parser("list",
            help="list all databases")
    list_parser.add_argument("-r", "--running", action='store_true',
            help="list only databases that are currently running")

    return parser.parse_args()


if __name__ == "__main__":
    main()
