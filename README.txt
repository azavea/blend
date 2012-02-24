=====
Blend
=====

A cross-platform tool for merging and processing client-side assets for web sites and web applications.

Introduction
============

Blend is designed to mimic the asset pipeline introduced in Ruby on Rails 3.1 (http://guides.rubyonrails.org/asset_pipeline.html) with two key differences:

    - Written as a Python module
    - Works with any web framework, or no framework at all

Installation
============

- Download and extract the package
- Run python setup.py install

Usage
=====

The ``blend`` command line tool is designed to process a directory full of files or individually specified files.

Command Line Options
====================

-o OUTPUT, --output=OUTPUT
Where the file output will be written

-e ENV, --environment=ENV
A directory to be searched for required files (multiple directories can specified by repeating the flag)

-s, --skipcwd
Exclude the current working directory from the environment