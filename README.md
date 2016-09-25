# Engine

### Setup.

1. git clone the code.
2. create a virtualenv
  1. `mkdir venv`
  2. `cd venv`
  3. `virtualenv -p python3 .`
  4. `cd .. && source venv/bin/activate`
  5. `pip install -r requirements.txt`
3. run unit tests
  1. `python -m unittest discover`