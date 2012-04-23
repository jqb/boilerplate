boilerplate
-----------

Very simple (and stupid) templating engine for directories & files structures.
You can use it to generate short, file-based snippets of code as well.


Installation
------------

  $ pip install boilerplate


Simple usage
------------

1) create simple file-based template ::

   $ echo "print 'This is generated file for name \"{{ template_name }}\"'" > _\$template_name\$_.py


2) use "boil" commandline utility to generate your file ::

   $ boil simple_template -t _\$template_name\$_.py
   $ ls
   $ simple_template.py
   $ python simple_template.py
   $ This is generated file for name "simple_template"
