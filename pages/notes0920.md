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
`-E` to use Extended (not basic) regular expressions

exercise: find the option to get the matched pattern to be colorized.

Some options for `find`:  
`-type` with `d` or `f` for directory / file  
`-name` with a regular expression (say `'*.pdf'`)  
`-d` for depth (e.g. `-d 1` or `-d +1` or `-d -1`)  
`-mtime` for modified time  

## regular expressions

We need a whole class period on this!
<!-- http://v4.software-carpentry.org -->
Just a few things here:

|    |    |
|:---|:---|
|`.` | any one character |
|`^` | beginning of line |
|`$` | end of line |
|`[aBc]` | anything in: a or B or c |
|`[^aBc]`| anything but: a, B, c |
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
anything other than A, C, G or T.

<!--
```shell
grep -v "^>" tb1.fasta | grep --color -i "[^ATCG]"
```
Y is for pYrimidine bases: C or T.
-->


---
[previous](notes0915.html) & [next](notes0922.html)
