# Alexandria Documentation

[![Build Status](https://travis-ci.org/srtab/alexandria-docs.svg?branch=master)](https://travis-ci.org/srtab/alexandria-docs)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f3ff11fbcbdd4ef1ade40d8033e7642f)](https://www.codacy.com/app/srtabs/alexandria-docs?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=srtab/alexandria-docs&amp;utm_campaign=Badge_Grade)

## Purpose
Alexandria is a documentation centralizer statically generated. Receive, store, index and serve documentation generated using tools like sphinx, mkdocs, etc...

## Starting development
Steps to start developing and contributing:

```
// clone the project
$ git clone https://github.com/srtab/alexandria-docs.git
$ cd alexandria-docs

// build the image
$ docker build -t alexandria .

// run the container
$ docker run -d -p 8000:8000 -v $(pwd):/app --name alexandria alexandria

// stop container
$ docker stop alexandria

// start container
$ docker start alexandria
```

## Running tests
To run unit tests we use tox. You need to access the container bash and run tox:

```
// access to container bash
$ docker exec -it alexandria bash

// run unit tests inside the container
$ tox -e py27
```
