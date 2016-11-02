---
layout: page
title: 11/3 notes
description: course notes
---
[previous](notes1101.html) & [next](notes1108.html)

---

## homework

[homework 2](https://github.com/UWMadison-computingtools/coursedata/tree/master/hw2-datamerge), due R 11/10. learning goals:
experience with Python, more experience with git,
think about algorithm strategy,
set good computing habits (project organization, documentation,
[etc](http://cecileane.github.io/computingtools/pages/notes0906.html#best-practices)).

## binomial coefficients script: con't

improve on `binomial.py`:

- expand the *docstring* to state assumptions
- *checks* that the input `n` is non-negative
- add an *optional argument* `k` to calculate `log(n!/k!)=log((k+1)*...*n)`,
  with default `k=0`. return log(1)=0 if k>n, with no error.
- check that `k` is a non-negative integer
- add associated *tests* as examples inside the docstring:
  with n=5 and some k<5, also n=k=5 (boundary), and n=5, k=6.
- Write a function "choose" to calculate `log(choose(n,k))` for any integers
  `n>=0` and `0 <= k <= n`. Start with the docstring and with a test.
- add an optional argument to this `choose` function, to return the
  binomial coefficient itself (default) or its log otherwise.
- add a docstring for the module


## python script arguments

`sys` module: function `sys.arg` to get the script name and arguments  
module [argparse](https://docs.python.org/dev/howto/argparse.html):
to do things well, more easily, and with documentation.  
let's revise our binomial script to give it arguments:

- `-n` and `-k` values, no defaults: to get the binomial coefficient "n choose k"
- `--log` option: to get the log of the binomial coefficient
- `--test` option: to test the package instead of calculating one particular
  coefficient value. should be incompatible with n, k, log options.

```python
import argparse
# use an Argument Parser object to handle script arguments
parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, help="total number of items to choose from")
parser.add_argument("-k", type=int, help="number of items to choose")
parser.add_argument("-l", "--log", action="store_true", help="returns the log binomial coefficient")
parser.add_argument("--test", action="store_true", help="tests the module and quits")
args = parser.parse_args()
# test argument problems early:
if args.test and (args.n or args.k or args.log):
    print("ignoring n, k or log arguments")
if not (args.test or (args.n and args.k)):
    raise Exception("needs 2 integer arguments: -n and -k")
```

next add this at the end of the script:

```python
def runTests():
    print("testing the module...")
    import doctest
    doctest.testmod()
    print("done with tests")

if __name__ == '__main__':
    if args.test:
        runTests()
    else:
        res = choose(args.n, args.k, args.log)
        print(res)
```

then run the script like this:

```
$ ./binomial_v2.py -h
usage: binomial_v2.py [-h] [-n N] [-k K] [-l] [--test]

optional arguments:
  -h, --help  show this help message and exit
  -n N        total number of items to choose from
  -k K        number of items to choose
  -l, --log   returns the log binomial coefficient
  --test      tests the module and quits

$ ./binomial.py -n 150 -k 40
4408904561911885789946649584764715008
$ ./binomial.py -n 1500 -k 400 --log
866.1129352492226
$ ./binomial.py --test
testing the module...
done with tests
```

## working with files

- disk file vs. file object (file handle)
- 3 modes to open a file: `r`, `w`, `a` (append)

```python
fh = open("newfile", 'w') # creates file handle
try:
    fh.write("hello world\n") # problem if disk quota full, etc.
finally:
    fh.close() # need to close to clean up, even if problems earlier
```

equivalent to:

```python
with open("newfile", 'w') as fh:
    fh.write("hello world\n")

# fh is closed now
```

methods for file handles: `.write()`, `.writelines()`,
`read()`, `.readline()`, `.readlines()`

example: read fasta protein files from bds data (chapter 3)

- treat sequence names differently (lines starting with ">")
- concatenate lines that are for the same sequence
- output file with protein from all fasta files, with new format:
1 sequence = 1 line, with species name preceding the sequence itself

```python
with open("tb1-protein.fasta","r") as fh:
  for line in fh:
    print("line=", line, sep="", end="")
```

equivalent to:

```python
with open("tb1-protein.fasta","r") as fh:
  linelist = fh.readlines()
  for line in linelist:
    print("line=", line, sep="", end="")

with open("tb1-protein.fasta","r") as fh:
  line = fh.readline() # header line only
  print("line=", line, sep="", end="")
  dna = ""
  while line: # will be false at the end of file: ''
    line = fh.readline()
    print("line=", line, sep="", end="")
    dna += line.strip()

print("dna=", dna, sep="", end="")
```

let's do what we need now:

```python
def reformat_onefile(fin, fout):
  """assumes fin not open, fout already open for writing."""
  with open(fin,"r") as fh:
    for line in fh:
      line = line.strip()
      if not line:
        continue # skip the rest if empty line
      if line.startswith(">"): # header line
        fout.write(line)
        fout.write("\n") # after header
      else:              # dna sequence line
        fout.write(line)
  fout.write("\n") # after end of full sequence

import sys
reformat_onefile("tb1-protein.fasta", sys.stdout) # check function

import glob
filenames = glob.glob("*-protein.fasta")
with open("all1linesequences.fasta", "w") as outfile:
  for fname in filenames:
    print("next: will reformat",fname)
    reformat_onefile(fname, outfile)
```

note: `sys.stdout` is a file handle open for writing :)

## break and continue

extremely useful!
`break` to break out of a loop:

```python
i=0
while True:
  i += 1
  print("code for i =",i,"here")
  if i >= 4:
    break
i # 4
```

`continue` to *directly* continue to the next iteration of the loop,
*bypassing* all remaining code for the current iteration:

```python
for i in range(0,10000):
  if i==3 or i >= 5:
    continue
  print("code here not bypassed, i =", i)
i # 9999
```

also: `pass` to do nothing, useful for new not-ready code: a function
must have at least 1 line.

## file manipulations

- in module `os`: `listdir`, `mkdir`, `makedirs`, `rename`, `remove`, `rmdir`,
  `chdir`, `path.exists`, `path.isdir`, `path.isfile`
- in module `shutil`: `copy`, `copytree`, `rmtree`

```python
import os
os.listdir()
os.remove(".DS_Store")
os.mkdir("try1")
os.rmdir("try1")
os.makedirs("try/data/dna")
os.listdir("try")
os.chdir("try")
os.path.isdir("data/dna")
os.path.realpath("data/dna") # absolute path
os.path.isfile("data/dna/gene1.fa")
shutil.copy("../lizard/cten_16s.fasta?sequence=1", "data/dna/cten_16s.fa")
shutil.copy("../lizard/cten_16s.fasta?sequence=1", "data/dna")
os.system("touch readme.md")
```

---
[previous](notes1101.html) & [next](notes1108.html)
