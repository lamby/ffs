"""
*nix style python functions
"""
import contextlib
import errno
import filecmp
import os
import shutil

class cd(object):
    """
    Change directory to PATH. Mimics the *nix cd command

    When used as a contextmanager, will change directory
    within the nested block, returning you to your previous
    location on exit. Yields a Path object representing the
    new current directory.

    Arguments:
    - `path`: str

    Return: None or Path when contextmanager
    Exceptions: None
    """
    def __init__(self, path):
        """
        Change directories on initialization.
        This is a "Bad idea" but it allows us to be both
        function-like and contextmanager-like
        """
        self.startdir = getwd()
        self.path = path
        os.chdir(str(path)) # Coerce Path objects

    def __enter__(self):
        """
        Contextmanager protocol initialization.

        Returns a Path representing the current working directory
        """
        from ffs import Path
        return Path(self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Contextmanager handling.return to the original directory
        """
        os.chdir(self.startdir)
        return

def chmod(path, mode):
    """
    Change the access permissions of a file.
    Also accepts Path objects

    Arguments:
    - `path`: str or Path
    - `mode`: int

    Return: None
    Exceptions: None
    """
    return os.chmod(str(path), mode)

# ::chmod_R (FileUtils)

chown = os.chown

# ::chown_R (FileUtils)

cmp = filecmp.cmp
cp = shutil.copy2
cp_r = shutil.copytree

getwd = os.getcwd

def head(filename, lines=10):
    """
    Python port of the *nix head command.

    Return the frist LINES lines of the file at FILENAME
    Defaults to 10 lines.

    Arguments:
    - `filename`: str
    - `lines`: int

    Return: str
    Exceptions: None
    """
    with open(filename) as fh:
        return "".join(fh.readlines()[:lines])


# ::install (FileUtils)

ln = os.link

ln_s = os.symlink

# ::ln_sf (FileUtils)

mkdir = os.mkdir

def mkdir_p(path):
    """
    Python translation of *nix mkdir -p

    Will create all components in `path` which do not exist.

    Arguments:
    - `path`: str

    Return: None
    Exceptions: Exception
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

mv = shutil.move

def pwd():
    """
    Python port of the *nix pwd command.

    Prints the current working directory
    """
    print(getcwd())
    return

def rm(*targets):
    """
    API wrapper to get closer to the *nix
    rm utility.

    Arguments:
    - `*targets`: all target paths

    Return: None
    Exceptions: None
    """
    for target in targets:
        os.remove(target)
    return

# ::rm_f (FileUtils)

rm_r = shutil.rmtree

# ::rm_rf (FileUtils)

rmdir = os.rmdir
stat = os.stat

def touch(fname):
    """
    Python port of the Unix touch command

    Create a file at FNAME if one does not exist
    """
    with open(fname, 'a'):
        pass
    return

unlink = os.unlink

def which(program):
    """
    Python port of the Unix which command.

    Examine PATH to see if `program' is on it.
    Return either the fully qualified filename or None

    Arguments:
    - `program`: str

    Return: str or None
    Exceptions: None
    """
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

def is_exe(fpath):
    """
    Is `fpath' executable?

    Arguments:
    - `fpath`: str

    Return: bool
    Exceptions: None
    """
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)