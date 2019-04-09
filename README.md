#   hangman
Hangman API (work in progress)

##  Installation instructions

1.  Ensure you have Python >=3.5 installed.  (This has only been
    testing on a GNU/Linux system)
1.  `python3 -m venv $HOME/hangman/venv`
1.  `. $HOME/hangman/venv/activate`
1.  `pip install Flask`

##  Running the API server

1.  `cd $HOME/hangman`
1.  `export FLASK_APP=hangman; export FLASK_ENV=development`
1.  `flask run` (or `flask run --host 0.0.0.0` if you want to access
    it from the outside world, not just 127.0.0.1)
