Vidgen
======

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

Vidgen is a python video generator.


Installation
------------

To install vidgen, run this command:

.. code-block:: console

   $ pip install vidgen


Usage
-----

To download a reddit post, use the `redditdl` commmand.

To run this command,
you need to register a reddit API app first.
You can do this at `the Reddit Apps Page
<https://reddit.com/prefs/apps>`_.
Once you register an app,
you need the Client ID,
Client Secret,
and a user agent
like

.. code-block::

   <platform>:<app ID>:<version string> (by u/<Reddit username>)

You can pass these variables
on the commandline or in
environment variables.
For more information about which
environment variables to set, run

.. code-block:: console

   $ vidgen redditdl --help

You can download a post
using its URL or its ID
(which can be found in the url)
and an output filename.

.. code-block:: console

   $ vidgen redditdl https://www.reddit.com/r/programming/comments/dhwtvt/python_38_released/ python.json

Or you can use a post ID
(this has the same effect as the command above):

.. code-block:: console

   $ vidgen redditdl dhwtvt python.json

.. note::
   These examples don't include
   the client ID or
   client secret command line options.

   You have to add these on after the command
   unless you're using environment variables.

   These client ID can be passed
   with the `-cid` or `--client-id`
   option, the client secret in the
   `-csec` or `--client-secret` option,
   and the user-agent in the
   `-ua` or `--user-agent` option.

   For example:

   .. code-block::

      -cid xxxxxxxx -csec xxxxxxxxx -ua "python:someproject:v0.0.1 (Made with love by /u/Scoder12)"
