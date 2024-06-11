# FIT3077

## Video

https://youtu.be/dC35bf3lzcc

### Repository Structure

Inside this repository are the source files, raw files and documentation used
to create our submission for Sprint 03. The structure is as follows:

**game**
<br>
_Inside this folder is all the source code for the program,
it also includes the executable build file_ **_main.exec_** _in the_ **_dist_**
folder, which you can use to run the game locally in a **_MacOS environment_**.

**Raw Files**
<br>
_This folder contains each of the .pdf files that compose the combined documentation
for this assignment. It also has a link to the_ **_LucidChart_** project where our
UML diagram can be found.

**FIT3077 Team009 Fiery Dragons Sprint 03 Documentation.pdf**
<br>
_This file, found in the root directory where_ **_README.md_** _can be found, is the
combined documentation for the assignment, from each of the individual .pdf files
found in the_ **_Raw Files_** _folder._

# Running the executable

The game has already been packaged into a single executable found in dist/main.exec

The app is self-contained and does not require any additional software to run. However, one limitation of pyinstaller
is that it can only create an executable for the device it is run on, in my case an arm (M-series) MacBook. The
application has not been tested on Intel based MacBooks.

When the executable is run, it should open a terminal which will display debug messages for movement. Please be patient
as the game can take some time (up to 30 seconds on my machine) to start after the terminal is opened.

# Development Setup

### Getting setup

I used pyenv ([tutorial for mac here](https://medium.com/marvelous-mlops/the-rightway-to-install-python-on-a-mac-f3146d9d9a32))
to get my python environment setup.

Installing required libraries
`pip install pygame`

### Building Game

To compile the game into a single executable for the platform you are developing on, you'll
first need to install [pyinstaller](https://www.google.com/search?client=safari&rls=en&q=pyinstaller&ie=UTF-8&oe=UTF-8)

`pip install pyinstaller`

Once pyinstaller is installed, to build the executable run:

`pyinstaller --add-data "imgs/animals/*.png:./imgs/animals" --add-data "imgs/caves/*.png:./imgs/caves" --add-data "imgs/chits/*.png:./imgs/chits" --add-data "imgs/tokens/*.png:./imgs/tokens" --add-data "imgs/*.png:./imgs" main.py -F`

If we break this down, the first flag `--add-data "[relative-path-to-images]:[executable-path-to-images]"`
will specify what images pyinstaller will copy to the executable. We copy this to the same path in the executable preceded
by a "." (signifies relative directory of game.py) to ensure that our code will be able to find our images in the same
directory when run by the executable.

The `*` in "/\*.png" tells pyinstaller to copy all .png files in the directory.

Finally, the -F flag tells pyinstaller to build the app into a single executable. Without this flag, by default
pyinstaller will produce a one folder bundle, instead of a single file bundle executable.

#### Specific versions

- Python: 3.11..8
- pygame: 2.5.2
- however pretty sure any python >= 3.8 is fine (min version for pyinstaller), and whatever latest pygame you get should be fine too
