---
layout: page
title: 9/20 notes
description: notes, links, example code, exercises
---

## homework

- for Thursday: edit your readme files for exercise 1,
  to add metadata and documentation
- for Tuesday next week: do exercise 2 of [homework 1](https://github.com/UWMadison-computingtools/coursedata/tree/master/hw1-snaqTimeTests)  
  document your new work in your readme file, save your work

## the shell: more on redirection

We will do "Loops" from the
[software carpentry introduction](http://swcarpentry.github.io/shell-novice/).  
Summary of [command](notes0908.html) and of [wild cards](notes0915.html).

```shell
ls -d * unknownfile
```
What is this command doing?  
It gives both: some output and some error.
Let's try to capture the output and the error separately.

```shell
ls -d * unknownfile > outfile
cat outfile
rm outfile
ls -d * unknownfile 2> errfile
cat errfile
rm errfile
ls -d * unknownfile > outfile 2> errfile
cat outfile
cat errfile
rm outfile errfile
ls -d * unknownfile &> outerrfile
cat outerrfile
rm outerrfile
```

What would `2>>` do?

each open file has a "file descriptor"

- standard input: 0, standard output: 1, standard error: 2
- `>` does the same as `1>`

How could `tail -f` (f=follow) be useful to check status
of a program that takes very long to finish? example:

```shell
cd ~/Documents/private/st679/coursedata/ex-mrbayes
mb mrBayes-run.nex
```

What if a program generates a whole lot of "standard output"
to the screen, which we are not interested in?
(interesting output might go to a file)? We can redirect the
screen output (STDOUT) to a "fake" disk `/dev/null` (black hole):

```shell
myprogram > /dev/null
```

## less and man

- `man ls` to get help on `ls`
- other very standard option: `--help`
- the result of `man` is actually passed on to the "viewer" `less`
- try `more` on a long file: shows more and more, one page at a time
- `less` is similar, but much better. Name from "less is more".
  Power of text streams: can read very long files without having
  to load the whole thing in memory.

some commands for `less` (there are many more!):

|       |    |
|:------|:---|
| q     | quit             |
| enter | show next line   |
| space | show next "page" |
| d     | down next half-page |
| b     | back one page |
| y     | back (yp?) one line |
| g or < | go to first line. 4g or 4G: go to 4th line |
| G or > | Go to last line   |
| /pattern | search forward  |
| ?pattern | search backward |
| n        | next: repeat previous search |
|----------|------------|
|         |   |
{: rules="groups"}

- use these commands for `less` to search a manual page and
  navigate fast between the top, bottom, marked positions,
  and searched keywords: `man less`
- how to search for anything that does *not* match a pattern?

## finding things

- `find` to find files: whose names match simple patterns
- `grep` to find things in (text) files:
   select lines that match simple patterns
- do a **command substitution** with `$()` to pass the list of files found
  to another command, like `grep` or `wc`: `grep xxx $(find yyy)`

examples:

```shell
grep "and" filename
echo "orchestra and band" | grep "and" # to search a string, not a file
grep -w "and" *
find . -type d
```

Some options for `grep`:  
`-n` for line numbers  
`-i` for case-insensitive search  
`-w` for whole words  
`-v` to in**v**ert the search  
`-o` to get the match only  
`-E` to use Extended (not basic) regular expressions,
`-P` for Perl-like regular expressions (GNU only)

exercise: find the option to get the matched pattern to be colorized.

Some options for `find`:  
`-type` with `d` or `f` for directory / file  
`-name` with a regular expression (say `'*.pdf'`)  
`-d` for depth (e.g. `-d 1` or `-d +1` or `-d -1`)  
`-mtime` for modified time

## GNU vs BSD command-line tools

Mac users: you have BSD tools (do `man grep` for instance, or `grep --version`).
They differ slightly from the GNU tools, which are generally better.
Install the GNU tools with [homebrew](http://brew.sh):

```shell
brew install coreutils # basic tools like ls, cat etc.
brew tap homebrew/dupes
brew install grep      # to get GNU grep, not included in basic tools
brew install gnu-sed   # to get GNU sed, also not included in basic
```

then use `gcat` instead of `cat`, `ggrep` instead of `grep` etc.

<!--
`brew --prefix coreutils` showed me `/usr/local/opt/coreutils`
in which there was `bin/` with all the "g" tools. I then checked to see if
this directory was in my PATH variable: `echo $PATH`. It wasn't. but gcat and gecho worked.
ggrep and gsed were not there.
-->

## regular expressions: "regexp"

We need lots of practice on this!
For help: `man re_format`,
get an explanation of your expression (and debug it)
on [regexp101](https://regex101.com) or [debuggex](https://www.debuggex.com)

<!-- http://v4.software-carpentry.org -->

|    |    |
|:---|:---|
|`.` | any one character |
|`^` | beginning of line (only if placed first)|
|`$` | end of line (only if placed last)|
|`\` | turns off special meaning of next symbol |
|`[aBc]` | anything in: a or B or c |
|`[^aBc]`| anything but: a, B, c |
|`\w` | any word character: letter, number, or "_". also `[[:alnum:]_]`. opposite: `\W`|
|`\d` | any single digit. also `[[:digit:]]`. opposite: `\D` |
|`\s` | any white space character: single space, `\t` (tab), `\n` (life feed) or `\r` (carriage return). also `[[:space:]]`. opposite: `\S` |
|`\b` | word boundary (null string). also `\<` and `\>` for start/end boundaries. opposite: `\B` |
|`+` | one or more of the previous |
|`?` | zero or one of the previous |
|`*` | zero or more of the previous |
|`{4}`| 4 of the previous |
|`{4,6}`| 4 or 6 of the previous |
|`{4,}`| 4 or more of the previous |
|--------|------------|
|        |            |
{: rules="groups"}


<!-- from Bioinformatics Data Skills, Chapter 2 (ideas) and
     Chapter 6 (example) -->

## more practice with grep

Use `grep` to find whether and where the file below has
non-nucleotide characters.

```shell
$ cd bds-files/chapter-03-remedial-unix/
$ cat tb1.fasta
>gi|385663969|gb|JQ900508.1| Zea mays subsp. mexicana isolate IS9 teosinte branched 1 (tb1) gene, complete cds
GCCAGGACCTAGAGAGGGGAGCGTGGAGAGGGCATCAGGGGGCCTTGGAGTCCCATCAGTAAAGCACATG
TTTCCTTTCTGTGATTCCTCAAGCCCCATGGACTTACCGCTTTACCAACAACTGCAGCTAAGCCCGTCTT
CCCCAAAGACGGACCAATCCAGCAGCTTCTACTGCTAYCCATGCTCCCCTCCCTTCGCCGCCGCCGACGC
CAGCTTTCCCCTCAGCTACCAGATCGGTAGTGCCGCGGCCGCCGACGCCACCCCTCCACAAGCCGTGATC
AACTCGCCGGACCTGCCGGTGCAGGCGCTGATGGACCACGCGCCGGCGCCGGCTACGGCTACAGAGCTGG
GCGCCTGCGCCAGTGGTGCAGAAGGATCCGGCGCCAGCCTCGACAGGGCGGCTGCCGCGGCGAGGAAAGA
CCGGCACAGCAAGATATGCACCGCCGGCGGGATGAGGGACCGCCGGATGCGGCTCTCCCTTGACGTCGCG
CGCAAATTCTTCGCGCTGCAGGACATGCTTGGCTTCGACAAGGCAAGCAAGACGGTACAGTGGCTCCTCA
ACACGTCCAAGTCCGCCATCCAGGAGATCATGGCCGACGACGCGTCTTCGGAGTGCGTGGAGGACGGCTC
CAGCAGCCTCTCCGTCGACGGCAAGCACAACCCGGCAGAGCAGCTGGGAGGAGGAGGAGATCAGAAGCCC
AAGGGTAATTGCCGCGGCGAGGGGAAGAAGCCGGCCAAGGCAAGTAAGGCGGCGGCCACCCCGAAGCCGC
CAAGAAAATCGGCCAATAACGCACACCAGGTCCCCGACAAGGAGACGAGGGCGAAAGCGAGGGAGAGGGC
GAGGGAGCGGACCAAGGAGAAGCACCGGATGCGCTGGGTAAAGCTTGCTTCAGCAATTGACGTGGAGGCG
GCGGCTGCCTCGGGGCCGAGCGACAGGCCGAGCTCGAACAATTTGAGCCACCACTCATCGTTGTCCATGA
ACATGCCGTGTGCTGCCGCTGAATTGGAGGAGAGGGAGAGGTGTTCATCAGCTCTCAGCAATAGATCAGC
AGGTAGGATGCAAGAAATCACAGGGGCGAGCGACGTGGTCCTGGGCTTTGGCAACGGAGGAGGAGGATAC
GGCGACGGCGGCGGCAACTACTACTGCCAAGAGCAATGGGAACTCGGTGGAGTCGTCTTTCAGCAGAACT
CACGCTTCTACTGAACACTACGGGCGCACTAGGTACTAGAACTACTCTTTCGACTTACATCTATCTCCTT
TCCCTCAACGTGAGCTTCTCAATAATTTGCTGTCTTAATCTATGCGTGTGTTTCTCTTTCTAGACTTCGT
AATTGGCTGTGTGACGATGAACTAAGTTTGGTCATCGCATGATGATGTATTATAGCTAGCTAGCATGCAC
TGTGGCGTTGATTCAATAATGGAATTAATCGGTGTCGTCGATTTGGTGATTTCCGAACTGAATCTCTGTG
ATGAACGAGATCAAACAGTATCCGCCGGTGACGGACGTTCATTACTATTGGCAAGCAAAGCAAGTACTAA
TGTAATTCAGCTGTTTGATGACAGAATGAAAAAAATGTTGAAGGCTGAAGCTATAACATGCTGAAAGAGA
GGCTTTTGCTAGGTAAAAGTCTAGCTCACAAGGTCAATTCCATGATGCCGTTTGTATGCATGTTAAAATC
TGCACCTAATGGCGCGGCTTTATATAGTCTTATAATTCATGGATCAAACATGCCGATC
```
Hint: first exclude non-nucleotide lines, then (pipe) find lines with
anything other than A, C, G or T (and other than a, c, g, t).

<!--
```shell
grep -v "^>" tb1.fasta | grep --color -i "[^ATCG]"
```
Y is for pYrimidine bases: C or T.
-->

beginning/end of lines, and escaping special characters:

```shell
echo abc a g ef$ g
echo abc a g ef$ g | grep "a" -o    # 2 matches
echo abc a g ef$ g | grep "^a" -o   # 1 match only: last one
echo abc a g ef$ g | grep "g" -o    # 2 matches
echo abc a g ef$ g | grep "g$" -o   # 1 match
echo abc a g ef$ g | grep "f$" -o   # no match
echo abc a g ef$ g | grep "f\$" -o  # match
echo ^abc a g ef$ g | grep "$ " -o  # match
echo ^abc a g ef$ g | grep "^a" -o  # no match
echo ^abc a g ef$ g | grep "\^a" -o # match
echo ^abc a g ef$ g | grep "^^a" -o # match
```

What would `grep "^$" filename` do? How about

dot, words, digits:

```shell
cd ../../coursedata/hw1-snaqTimeTests
cat out/timetest9_snaq.out
grep "Elapsed time" out/timetest9_snaq.out #  Elapsed time: 34831.465925074 seconds in 10 successful runs
grep "Elapsed time." -o out/timetest9_snaq.out # . matches any one character
grep "Elapsed time. \d+" -o out/timetest9_snaq.out # no match: need Extended regexp
grep -E "Elapsed time. \d+" -o out/timetest9_snaq.out # \d = digit, +: one or more
grep -E "Elapsed time. \d+\.\d" -o out/timetest9_snaq.out # need to escape the dot to match "."
```


---
[previous](notes0915.html) & [next](notes0922.html)
