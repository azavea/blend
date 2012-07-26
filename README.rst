=====
Blend
=====

Merge, analyze, and optimize client-side assets for web applications and static web sites.

Example
=======

Given the following directory structure::

    project
      lib
        jquery-1.7.2.min.js
      src
        app.js
        components
          menu.js
        common
          helpers.js

And the following ``app.js``::

    /* app.js */

    //= require jquery
    //= require menu
    var app = {};

And the following ``menu.js``::

    /* menu.js */

    //= require jquery
    //= require helpers
    var menu = {};

And the following ``helpers.js``::

    /* helpers.js */

    var helpers = {};

Running ``blend`` with no arguments from the ``project`` directory will produce this directory structure::

    project
      lib
        jquery-1.7.2.min.js
      output
        app.js
        app.min.js
        menu.js
        menu.min.js
      src
        app.js
        components
          menu.js
        common
          helpers.js

Where ``app.js`` has the following content::

    /* app.js */

    /* ... the minified JQuery code, included only once */
    var helpers = {};
    var menu = {}
    var app = {};

Usage
=====

blend [options] [file1 [file2 [fileN]]]

Command Line Options
--------------------

Output
~~~~~~
``-o OUTPUT, --output=OUTPUT``

Where the file output will be written. The default is a directory at the root of the
project directory named ``output``

Path
~~~~~
``-p PATH, --path=PATH``

A directory to be searched for required files. Multiple directories can specified by
repeating the flag. If you do not
specify any directory with the PATH flag then only the working directory will be searched for required files.

Skip Working Directory
~~~~~~~~~~~~~~~~~~~~~~
``-s, --skipcwd``

Exclude the current working directory from the requirement search paths.

Specify A Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~
``-c, --config``

Specify a JSON confguration file that describes the analyzers and minifiers to be used.

Installation
============

From the Python Package Index
-----------------------------
::

    pip install blend

From Source
-----------
::

    git clone git://github.com/azavea/blend.git
    cd blend
    python setup.py install

Documentation
=============
http://azavea-blend.readthedocs.org

License
============

MIT
