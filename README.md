Hearts is a python program to play the card game Hearts.  It is planned to 
include the following features:

    * Console based hearts game player for humans to play.
    * Various AI players to play against.
    * A framework to write new Hearts AI players in python.
    * A batch mode to have AI players play against each and report 
      back the results.

Features in 0.1.0
-----------------

    * The program includes a program to have AI programs play against 
      each other. 
    * Three AI players are included: Random, Highest, Hybrid.  The 
      source can be found in hearts/players.py.


Dependencies
------------
    * Python 2.7.3

Usage
-----

To run the program from source, type:

    python hearts/hearts.py <config file>

Sample config files can be found in <hearts>/conf.

You can also install the program with:

    pip install dist/pyhearts-0.1.0.tar.gz

Known Issues
------------
