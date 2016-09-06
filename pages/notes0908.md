---
layout: page
title: 9/8 notes
description: notes, links, example code, exercises
---

## the Unix shell

[software carpentry introduction](http://swcarpentry.github.io/shell-novice/).

summary:

- directory structure, root is `/`
- relative versus absolute paths
- shortcuts: `.`, `..`, `~`, `-`
- tab completion

|          |      |
|:---------|:-----------|
| `whoami` | who am I? to get your username |
| `pwd`    | print working directory. where am I? |
| `ls`     | list. many options, e.g. `-a` (all) `-l` (long) `-lrt` (reverse-sorted by time) |
| `man ls` | manual for `ls`. very standard option: `--help` |
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

## typing skills

- quick count: who had keyboarding classes in elementary school?
- it's like talking or walking: it's assumed.
- take a [test](http://www.typingtest.com/test.html)
- invest in your typing skills! it will save you time and stress.

---
[previous](notes0906.html) & [next](notes0913.html)
