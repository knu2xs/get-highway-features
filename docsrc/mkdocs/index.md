---
title: Home
---
# Get Highway Features 0.0.0 Documentation

{% include "../../README.md" %}

## Commands

Here are a few commonly used commands for efficient project configuration and use.

* `make env` - creates a Conda environment in the project directory in `./env` with resources needed for project development
* `make jupyter` - run Jupyter notebook with options enabling connecting from another computer on the same network if desired
* `make data` - build data using the file `./scripts/make_data.py` using the Conda environment `./env` created with the command    
  `make env`
* `make docs` - builds documentation in `./docs` from resources in `./docsrc`.
* `make docserve` - runs live server on http://127.0.0.1:8000/ to see updates to docs in real
  time. This is extremely useful when building the documentation to see how it will look.

!!! note

    These commands are defined in `./make.cmd` if you want to examine, modify or extend this capability.
