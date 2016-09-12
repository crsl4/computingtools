---
layout: page
title: 9/13 notes
description: notes, links, example code, exercises
---

## logistics

- email me if you want to be added to the course mailing list
  (auditors)
- starting next Thursday (9/15), we will meet in
  133 [SMI](http://map.wisc.edu/s/dc3243ls), in which it's easier to move
  chairs & tables arounds, and tables are larger.
- do things on your own laptop: watching the screen is insufficient
  to get good at this

## intro to the shell (con't)

We will continue with "Working with Files and Directories" from the
[software carpentry introduction](http://swcarpentry.github.io/shell-novice/).
Summary of commands [here](notes0908.html).

- wild cards:
  - `*` matches zero or more characters (anything).
  - `?` matches exactly 1 characters

  the shell expands the wild cards *before* running the command.
- pipes and redirection:  
 `>` to redirect the output of one command to a file  
 `|` pipes the output of one command to the input of another command: pipeline!
  very fast: uses streams only.  
 `>>` redirects output and appends to a file  
 `2>` redirects standard error  
 `&>` redirects both output and error (bash shell)

```shell
ls -d * unknownfile
```
What is this command doing?  
It gives both some output, and some error.
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

### more on redirection

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

## file names

so important: **no spaces!** example:

- create a directory 'raw sequences' in `data`, using a GUI (e.g. Finder)
- try to remove it from the command line:

```
cd data
ls
rm -rf raw sequences
```
lucky for us: `raw` or `sequences` didn't exist (chainsaw...)  
how can we remove this directory?

- prefer lower-case letters, especially for the first letter of a file name:
  time saver, along with tab completion

- some common usage: capitalize between words, or underscore, like
  `wheatSequenceAlignments` or `wheat_sequence_alignments`.

- use ASCII characters only, no space (did I mention this already?),
  no `/`, no `\` (for Windows), no `-` for the first character.

- R users: avoid dots. conventionally used for the file extension.

- file extensions:
   * not needed by the computer. for humans only.
     your computer uses `.txt` to open the file with whichever app is supposed
     to open text files. That's it.
   * explicit is better than implicit for humans.
     ex: `rice_genes.fasta` versus `rice_genes`

- choose file names to ease automation, using shell expansion

- use leading zeros: `file-0021.txt` rather than `file-21.txt`.
  lexicographic sorting files (like with `ls`) would otherwise place
  `file-1390.txt` before `file-21.txt`.

## text editor

- see [here](notes0906.html#text-editor)

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

## typing skills

- quick count: who had keyboarding classes in elementary school?
- it's like talking or walking: it's assumed.
- take a [test](http://www.typingtest.com/test.html)
- invest in your typing skills! it will save you time and stress.  
  allow yourself one week to be slow.

## homework

- create a [github](https://github.com) account: done?
- request a "student developer pack" [here](https://education.github.com/pack),
  which includes unlimited free repositories on github.  
  Click on "get your pack", then follow instructions.
  To the question "How do you plan to use "GitHub", you can say
  "for research" (my hope is that you will continue to use github for
  analyses in your dissertation), or "for learning computational tools",
  or some other appropriate description.
- email me your github username, so that I can add you to the
  github organization for the course:
  [UWMadison-computingtools](https://github.com/UWMadison-computingtools)



---
[previous](notes0908.html) & [next](notes0915.html)
