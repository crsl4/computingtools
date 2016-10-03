---
layout: page
title: 10/4 notes
description: course notes
---
[previous](notes0929.html) & [next](notes1006.html)

---

## homework

due Tuesday next week 10/11: do and [submit](https://github.com/UWMadison-computingtools/coursedata#commit-push-and-submit-your-work)
exercise 3 from [homework 1](https://github.com/UWMadison-computingtools/coursedata/tree/master/hw1-snaqTimeTests).
The goal of this exercise is to write a shell script with
search/replace components, with a loop
and with test statements (for, if/then).

## more shell tools

examples of commands not used earlier --see summary [here](notes0908.html)

### cut

```shell
cd bds-files/chapter-07-unix-data-tools
ls -lh # 1.6M = size of Mus_musculus.GRCm38.75_chr1.bed
head Mus_musculus.GRCm38.75_chr1.bed # chromosome number, start & end position
cut -f 1 Mus_musculus.GRCm38.75_chr1.bed | sort | uniq # check chromosome 1 only
cut -f 2 Mus_musculus.GRCm38.75_chr1.bed | head -n 3
```

other ways to use options for `cut`:

- `-f2`, `-f 1,3`, `-f1-3`
- `-c2` to cut (extract) the second character, not the second field (column)
- `-d` to change the delimiter between columns fields instead of tab:
  `-d ' '` for a space, `-d,` `-d ,` or `-d ','` for a comma (csv files).


example from research: data used in
[Baum et al. 2016](http://onlinelibrary.wiley.com/doi/10.1111/evo.12934/full)
originally from [Perelman et al. 2011](http://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1001342).  
54 genes in 178 primate species, from 186 individuals
(different subspecies).  
data cleaning: needed to identify and remove duplicates from the same species.  
step I used repeatedly to get the list of "taxa" in my cleaned file:
<!-- see more in readme.md in that folder -->

```shell
cd ../../coursedata/lecturedata
head -n 6 combined.nex
head -n 7 combined.nex
wc combined.nex
grep '_' combined.nex | cut -f 1 -d ' ' > taxa
wc taxa
head taxa
```

### sort

`-k` to sort by specific columns (keys). example below:
`-k1,1` to sort by keys in column1 to 1,
then `-k2,2` to resolve ties by to sorting columns 2 to 2, and
`n` to sort that 2nd column numerically,
`r` to sort that 2nd column it in reverse order.  
`-c` to check if the file is sorted already (fast)  
`-t,` or `-t ","` to change the separator to a comma instead of tab (default)

```shell
cd ../../bds-files/chapter-07-unix-data-tools
sort -k1,1 -k2,2n example.bed
sort -k1,1 -k2,2nr example.bed
sort -k1,1 -k2,2n -r example.bed
sort -k1,1 -k2,2n -c example.bed
sort -t, -nc Mus_musculus.GRCm38.75_chr1_bed.csv
sort -t, -n Mus_musculus.GRCm38.75_chr1_bed.csv | head
sort -t, -nr Mus_musculus.GRCm38.75_chr1_bed.csv | head
```

exercise: extract all the features (and counts) for gene "ENSMUSG00000033793".
[the feature name is in the 3rd column]
<!--
grep "ENSMUSG00000033793" Mus_musculus.GRCm38.75_chr1.gtf | cut -f3 | sort | uniq -c
-->

exercise: extract all the combinations of distinct feature names
(like "gene" or "exon") and strands (+ or -), with their counts (sorted).
[the strand in the 7th column]
<!--
grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf | cut -f3,7 | sort | uniq -c | sort -rn
-->

### column

`column` formats tabular data to visualize in the terminal

```shell
cd ../../bds-files/chapter-07-unix-data-tools
head Mus_musculus.GRCm38.75_chr1.gtf # format for genomic features. 1 line = 1 feature, e.g. 1 gene. start & end positions are 1-based
grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf | cut -f1-8 | head
grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf | cut -f 1-8 | column -t | head
column -s"," -t Mus_musculus.GRCm38.75_chr1_bed.csv | head
```

`-s","` sets the separator to a comma instead of a tab (default)

### basename & dirname

`basename` and `dirname` extract the file/folder name and its path
from a string (the file/folder need not exist).  
`-s suffix`: to removed known suffix (like an extension)

```shell
pwd
basename $(pwd)
dirname $(pwd)
basename "relative/path/to/myfile.txt"
dirname  "relative/path/to/myfile.txt"
basename "/absolute/path/to/myfolder"
dirname  "/absolute/path/to/myfolder"
dirname "myfile.txt" # current directory: .
basename -s "txt" "relative/path/to/myfile.txt"
basename -s "txt" "relative/path/to/myfile.txt"
basename -s ".txt" "relative/path/to/myfile.txt"
basename -s "le.txt" "relative/path/to/myfile.txt"
```

---

## stream editor: sed

edits the file without having to load it all in memory!
most important use: to substitute things

```shell
sed s/pattern/replacement/ filename > newfile # do NOT redirect to input file!
sed -i s/pattern/replacement/ filename # for in-place replacement
```

`s///` to replace first occurrence of a match,
`s///g` to replace globally (all instances),  
`s///i` and `s///gi` for case-insensitive search  
option `-E` for Extended (not basic) regular expressions

`-n` option to *not* print every line  
p flag to print: `s///p` print if there is a match

*warning*: unlike `grep`, `sed` does *not* recognize "enhanced" (Perl-like)
expressions like `\d` (digit), `\s` (space) or `\w` (word character).
use classes instead: like `[0-9]` or `[a-zA-Z_]`.

```shell
cat chroms.txt # "chrom1" in first column
sed 's/chrom/chr/' chroms.txt
```

we can capture and re-use a match: with `()` to capture a pattern
and `\i` to print the ith match.

example: transform a file with lines of the form
"chromosomename:startposition-endposition" to a tabular table "chromosomename startposition endposition" (3 columns separated with tabs)

```shell
echo "chr12:74-431" | gsed -E 's/^(chr[^:]+):([0-9]+)-([0-9]+)/\1\t\2\t\3/'
```

(We have to use GNU sed, `gsed` on my machine, to have `\t` be understood as a tab,
see [grep section](notes0922.html#GNU-vs-BSD-command-line-tools) to install it.)

Other ways to do the same thing below:

```shell
echo "chr12:74-431" | gsed 's/[:-]/\t/g' # why g flag?
echo "chr12:74-431" | gsed 's/:/\t/' | gsed 's/-/\t/'
echo "chr12:74-431" | gsed -e 's/:/\t/' -e 's/-/\t/'
echo "chr12:74-431" | tr ':-' '\t' # tr = translate
```

The first way is more specific, so probably more robust.
Always check for weird errors.

exercise: extract the unique transcript names in the data file
`Mus_musculus.GRCm38.75_chr1.gtf`: string after "transcript_id".

option 1: search for (and output) "transcript_id" and the following string,
extract this string, remove the quotes, remove duplicates.
recall `uniq` removes consecutive duplicates.

option 2: search for lines not starting by #, then replace 'transcript_id "anything but double quote, captured"' by what was captured (inside the double quotes).

```shell
less Mus_musculus.GRCm38.75_chr1.gtf # type /transcript_id to search and highlight instances
grep -E -o 'transcript_id "\w+"' Mus_musculus.GRCm38.75_chr1.gtf |
  cut -f2 -d" " | sed 's/"//g' | sort | uniq | head # or redirect: > newFileName.txt
grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf |
  sed -E 's/.*transcript_id "([^"]+)".*/\1/' | head # wait: doesn't work: extract lines!
grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf |
  sed -E -n 's/.*transcript_id "([^"]+)".*/\1/p' | sort | uniq | head
```

`sed` can do much more. just one example, to print lines 20 to 23:
`sed -n '20,23p' Mus_musculus.GRCm38.75_chr1.gtf | cut -f1-5 | column -t`

greedy matching: problem if we try to capture between quotes like this
`"(.+)"`

```shell
grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf |
  sed -E -n 's/.*transcript_id "(.+)".*/\1/p' | head -n 1
grep "^[^#].*transcript_id" Mus_musculus.GRCm38.75_chr1.gtf | head -n 1
echo 'before transcript_id "E0160944"; gene_name "Gm16088" after' > greedy_example.txt # simpler example
cat greedy_example.txt
sed -E 's/.*transcript_id "(.+)".*/\1/' greedy_example.txt
sed -E 's/.*transcript_id "([^"]+)".*/\1/' greedy_example.txt
sed -E 's/transcript_id ".*([^"]+)".*/\1/' greedy_example.txt # what happened here? explain
```

---

## shell scripts

### script arguments

command-line arguments stored in variables `$1`, `$2`, etc.  
`$0`: name of script
`$#`: number of arguments

example: script to show both the beginning and
the end of a file.
argument: file name  
create a new file `headtail.sh` containing this:

```shell
echo "script name: $0"
echo "first argument: $1"
echo "number of arguments: $#"
(head -n 2; tail -n 2) < "$1"
```

by the way: `<` redirect the standard input, and  
subshell between `(  )`: both head and tail get the same standard input.  
execute the script like this (for now):

```shell
bash headtail.sh Mus_musculus.GRCm38.75_chr1.bed
bash headtail.sh Mus_musculus.GRCm38.75_chr1.bed | column -t
```

### safe options and permissions

always start your script with this:

```shell
#!/bin/bash
set -e # script terminates if any command exits with non-zero status
set -u # terminates if any variable is unset
set -o pipefail # terminates if command within a pipes exits unsuccessfully
```

`#!` "shebang": tells how to run the script.
Would be `#!/usr/bin/perl` for a perl script.
do `which bash` or `which perl` to know what to put on this line:
path to bash or to perl.

With the first line and with the execute permission, we can run the script
with `./myscript.sh filename` instead of `bash myscript.sh filename`.  
To change permission:

```shell
ls -l
chmod u+x headtail.sh
ls -l
./headtail.sh Mus_musculus.GRCm38.75_chr1.bed
./headtail.sh Mus_musculus.GRCm38.75_chr1.bed | column -t
```

`u`, `g`, `o`: user, group, other; `a` for all  
`+` or `-` to add or remove permissions  
`r`, `w`, `x`: read, write, execute

**~/bin directory**:

- create one if you don't already have one,
  put your own programs there, to call them from anywhere.
- add it to your PATH variable. Do you see it when you do `echo $PATH`?
- if not: edit your file `~/.bash_profile`, add the line
  `export PATH="$PATH:~/bin"`, run `source ~/.bash_profile`
  or simply exit your shell and re-open it.

With that, I can move my script `headtail.sh` into `~/bin`, and run
it from anywhere I would like, as `headtail.sh filename`:

```shell
mv headtail.sh ~/bin/
headtail.sh Mus_musculus.GRCm38.75_chr1.bed
headtail.sh Mus_musculus.GRCm38.75_chr1.bed | column -t
```

### arithmetic expansion

use `(( ))`. If you need anything elaborate, it means
that you should use a Python / Perl / R script,
not a shell script.

```shell
i=3678
echo "my variables is: i=$i"
((i = i+6))
echo "I incremented i by 6: now i=$i"
((i--))
echo "I decremented i by 1: now i=$i"
((i++)); echo "I incremented i by 1: now i=$i"
((i+=1)); echo "I incremented i by 1 again: now i=$i"
((i/=5)); echo "finally, I divided i by 5: now i=$i"
echo $((i++))
echo $i # i++ executes the command and increments i after
echo $((++i))
echo $i # ++i increments i first, then executes the command
```

### `if` statements and checks

example:

```shell
if [ $i -lt 800 ] # the spaces after `[` and before `]` are REQUIRED
then
  echo "i is less than 800"
else
  echo "i is not less than 800"
fi
```

headtail script: let's test and check for at least one argument
(file name), and if so, test that this file is readable:

```shell
if [ $# -lt 1 -o ! -f $1 -o ! -r $1 ]
then
  echo "error: no argument, or no file, or file not readable"
  exit 1 # exit script with error code (1). 0 = successful exit
fi
```

exit code: 0 if successful, 1 if unsuccessful (for the shell, 0=true, 1=false!!)

|------|-------------|
| test expressions &nbsp;&nbsp;|             |
|:-----|:------------|
| `-z str` | string `str` is empty |
|`str1 = str2`| strings `str1` and `str2` are identical. different: `str1 != str2` |
|`int1 -eq int2`| integers `int1` and `int2` are equal. not equal: `int1 -ne int2` |
|`int1 -lt int2`| integer int1 is less than int2. greater: `int1 -gt int2` |
|`int1 -le int2`| integer int1 is less than or equal to int2. greater or equal: `int1 -ge int2`|
|`-d thing` | `thing` is a directory. file: `-f`, link: `-h` |
|`-e thing`| `thing` exists |
|`-r file`| `file` is readable. writable: `-w`, executable: `-x`|
|`-o`, `-a`, `!`| or, and, negation |
|`( )`| to group tests |
|--------|------------|
|        |            |
{: rules="groups"}

<!-- `-x`: accessible, if argument is expression -->

short-circuit evaluation: convenient, and *the order is important!*

- "A or B": B is not evaluated if A is true, because
  the result would be true anyway.  
  We can do "zero arguments or argument 1 is a file" without causing
  an error, but there could be an error if we did
  "argument 1 is a file or zero arguments".
- "A or B": B is not evaluated if A is false: the result would be false anyway.


Let's add a second, optional argument to our `headtail.sh` script:
number of lines to show at each end. default: 2

```shell
nl=2 # number of lines to show, on each end
if [ $# -ge 2 ]
then
  nl=$2
fi
(head -n $nl; tail -n $nl) < "$1"
```

### exercise: do
["tracking a species"](http://swcarpentry.github.io/shell-novice/07-find/#tracking-a-species)
from the software carpentry workshop: combines `grep`, `cut`, pipes
and script arguments usage.

---
[previous](notes0929.html) & [next](notes1006.html)
