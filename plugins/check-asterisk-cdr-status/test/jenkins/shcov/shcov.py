#!/usr/bin/env python
######################################################################
##
## Copyright (C) 2008,  Simon Kagstrom
##
## Filename:      shcov
## Author:        Simon Kagstrom <simon.kagstrom@gmail.com>
## Description:   Test shell script coverage
##
## $Id:$
##
######################################################################

# export PS4='SHCOV:::${BASH_SOURCE}:::${LINENO}::: SHCOV:'

import os, sys, subprocess, pickle, signal, select

base_dir = os.path.abspath(sys.path[0] + "/../")
sys.path =  [base_dir] + sys.path

import shcov

from shcov.file import File

class ShcovCollector:
    def __init__(self, args, outpath = "/tmp/shcov", shell = ["bash", "-x"]):
        self.files = {}
        self.args = args
        self.outpath = outpath
        self.shell = shell

        # Where we execute this script
        os.environ["PS4"] = "SHCOV:::${BASH_SOURCE}:::${LINENO}::: SHCOV:"

        self.process = None
        # Counts the number of ' characters. This is to detect (some) multi-line output
        self.tick_count = 0
        self.pid = os.getpid()

    def handle_line(self, line):
        """Handle one line of stderr input"""
        if line.find("SHCOV:::") == -1:
            # Three cases: No tick means that the last SHCOV tag was single-line,
            # one tick means that we're waiting for the end (don't output),
            # more than one means that we have stderr output with ticks
            if self.tick_count > 1 or self.tick_count == 0:
                sys.stderr.write(line)
            return
        # Reset tick count
        self.tick_count = line.count("'")
        parts = line.split(":::")

        file_name = parts[1]
        line_nr = parts[2]

        # Get the file for this path
        path = os.path.abspath(file_name)
        path = os.path.realpath(path)
        try:
            file = self.files[path]
        except KeyError, e:
            # Not found, create a new one
            try:
                file = File(path)
            except IOError, e:
                # Cannot create the object (file not found most likely),
                # just ignore it
                return

            # And create the dir to save it in
            try:
                os.makedirs( os.path.dirname(self.outpath + file.path) )
            except OSError, e:
                pass
            self.files[path] = file
        file.add_to_line(line_nr)
        try:
            file.save(self.outpath + file.path + ".%d.pkl" % (self.pid))
        except Exception, e:
            # No big deal - just means that we cannot write
            # to the destination just yet
            pass

    def parse_output(self):
        """Process the bash stderr output"""
        self.process = subprocess.Popen( self.shell + self.args,  stdin = sys.stdin,
                                         stdout = sys.stdout, stderr = subprocess.PIPE)

        fd_poll = select.poll()
        fd_poll.register( self.process.stderr.fileno() )

        while True:
            # Did the process exit?
            ret = self.process.poll()
            if ret != None:
                try:
                    pid = os.fork()
                except OSError, e:
                    raise Exception, "%s [%d]" % (e.strerror, e.errno)
                if pid == 0:
                    # Read the last stuff
                    for line in self.process.stderr.readlines():
                        self.handle_line(line)
                    # Save everything
                    self.save()
                return ret

            # Write out everything on stderr
            self.process.stderr.flush()

            # If stderr is not ready, just continue
            status = fd_poll.poll(10)
            if status == []:
                continue

            line = self.process.stderr.readline()
            self.handle_line(line)

    def save(self):
        for file in self.files.values():
            # Merge into the (locked) global file and remove the pid-specific
            # one
            file.merge_with_path(self.outpath + file.path + ".pkl")

            # If it hasn't been saved, no need to unlink it
            if not file.has_been_saved():
                continue
            os.unlink( self.outpath + file.path + ".%d.pkl" % (self.pid) )

def usage():
    print "Usage: shcov [-h] [--output=where] [--shell=what] script...\n"
    print "Produce coverage data for 'script'. Options are\n"
    print "  --output=where  write data to 'where' instead of /tmp/shcov"
    print "  --shell=what    ues 'what' (including arguments) as shell instead of 'bash -x'"

    sys.exit(1)

glob_sc = None

def sighandler(signum, frame):
    glob_sc.save()
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    outpath = "/tmp/shcov"
    shell = ["bash", "-x"]

    # Really, really, ugly, but it's done this way to avoid parsing the
    # options passed to the shell script
    last = 1
    for arg in sys.argv[1:min(len(sys.argv), 3)]:
        if arg == "-h" or arg == "--help":
            usage()
        elif arg.startswith("--output="):
            last = last + 1
            outpath = arg.strip("--output=")
        elif arg.startswith("--shell="):
            last = last + 1
            shell = arg.strip("--shell=").split()
        else:
            # First non-option
            break
    args = sys.argv[last:]

    if len(args) < 1:
        usage()

    sc = ShcovCollector(args, outpath = outpath, shell = shell)
    glob_sc = sc
    signal.signal(signal.SIGTERM, sighandler)
    out = 1
    try:
        out = sc.parse_output()
    except KeyboardInterrupt, e:
        # Just save
        sc.save()
    sys.exit(out)
