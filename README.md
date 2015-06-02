========
recommdr
========

A movie recommendation tool

* BSD license

Documentation
=============

[MkDocs](http://www.mkdocs.org/) is used to write docs. Once requirements are installed, run:

`mkdocs serve`

Documentation will be available at 127.0.0.1:800 with nice ReadTheDocs theme :)

## Overview

`recommdr` is a command line movie recommendation tool. It utilizes json data dump
 of large numbers of users and their movie preference which is included in project dir at `data/movies.json`.

 This tool takes number of movie IDs, and recommends movies based on input. Collaborative filtering formula
 [Cosine Similarity](http://en.wikipedia.org/wiki/Cosine_similarity) is used to calculate users who have similar preference.
 With that similarity, movies are recommended.


## Install

1. `cd recommdr`
2. `virtualenv env && source env/bin/activate` - crate virtualenv and activate it
3. `pip install -r requirements.txt` - install requirements
4. `python setup.py install` - install recommdr

## Usage

* `recommdr --movies 5 27 60 --json path/to/movies.json

More details below:

* `recommdr -h, --help ` - Show help
* `recommdr --version` - Show current version of this tool
* `recommdr --movies` - Given list of movie IDs, it will recommend movies.
* `recommdr --movies --number` - Optional: number of movies to be recommended.

## Run tests

Tests are written in `tests/` directory.
Tests can be run with:

`python tests/test_recommdr.py`
