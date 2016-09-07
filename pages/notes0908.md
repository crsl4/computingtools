---
layout: page
title: 9/8 notes
description: notes, links, example code, exercises
---

## the Unix shell

quick count: shell versus terminal? absolute versus relative path? `grep`?

We will follow the
[software carpentry introduction](http://swcarpentry.github.io/shell-novice/).
Click on 'setup' to download the data.

summary:

- directory structure, root is `/`
- relative versus absolute paths
- shortcuts: `.`, `..`, `~`, `-`
- tab completion to get program and file names
- up/down arrows and `!` to repeat commands

|          |      |
|:---------|:-----------|
| `whoami` | who am I? to get your username |
| `pwd`    | print working directory. where am I? |
| `ls`     | list. many options, e.g. `-a` (all) `-l` (long) `-lrt` (reverse-sorted by time) |
| `cd`     | change directory |
| `mkdir`  | make directory   |
| `rm`     | remove (forever). `-f` to force, `-i` to ask interactively, `-r` recursively
| `rmdir`  | remove (delete) directory, if empty |
| `mv`     | move (and rename). can overwrite existing files, unless `-i` to ask|
| `cp`     | copy. would also overwrite existing files |
| `diff`   | difference |
| `wc`     | word count: lines, words, characters. `-l`, `-w`, `-c` |
| `cat`    | concatenate |
| `less`   | because "less is more". `q` to quit. |
| `sort`   | `-n` for numerical sorting |
| `head`   | first 10 lines. `-n 3` for first 3 lines (etc.) |
| `tail`   | last 10 lines. `-n 3` for last 3 lines, `-n +30` for line 30 and up |
| `uniq`   | filters out repeated lines (consecutive). `-c` to get counts |
| `cut`    | cut and return column(s). `-d,` to set the comma as field delimiter (tab otherwise), `-f2` to get 2nd field (column) |
| `echo`   | print |
| `history`| shows the history of all previous commands, numbered |
| `!`      | `!76` to re-execute command number 76 in the history, `!$` for last word or last command |
|----------|------------|
|         |   |
{: rules="groups"}

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

```
ls -d * unknownfile
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
| d     | show next half-page |
| b     | back one page |
| y     | back one line |
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

---
[previous](notes0906.html) & [next](notes0913.html)
