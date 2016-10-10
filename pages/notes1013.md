---
layout: page
title: 10/13 notes
description: course notes
---
[previous](notes1011.html) & [next](notes1018.html)

---

<!-- ## homework -->


## quick text processing: awk

language for quick text-processing tasks on tabular data.
by Aho, Weinberger & Kernighan.  
`bioawk`: for biological formats.

- command lines: `awk pattern { action } filename`
- pattern: expression or regexp pattern (in slashes, e.g. `/^chr\d/`).  
  If true or match for a given line (record): the actions are run.  
  If no stated action: the line is printed.
- `a ~ b` true if `a` matches regexp pattern `b`. no match: `a !~ b`
- combine patterns with `&&` (and) and `||` (or)
- special patterns: BEGIN and END
- variables: `$0` for entire record (line),
  `$1` for first field (columns)'s value,
  `$2` for second field's value, etc.  
  `NR` = current record (line) number  
  `NF` = number of fields (columns) on current line
- can do arithmetic operations on field values, standard comparisons (`<=`, `==` etc.)
- extra fields can be printed
- new variables can be introduced, modified, used
  (no `$` to use them: not like shell language)
- actions: `if`, `for`, `while` statements can be used
- many built-in functions, like `exit`, `sub(regexp, replacement, string)`
  `substr(string, i, j)` or `split(string, array, delimiter)`
- default field (column) separator in input file: tab.
  For csv file: change to comma with `-F","`

examples:

```shell
awk '{ print $0 }' example.bed # like cat. No pattern: defaults to true
awk '{ print $2 "\t" $3 }' example.bed # like cut -f2,3
awk '$3 - $2 > 18' example.bed # prints lines (default action) if end-start position > 18
awk '$1 ~ /chr1/ && $3 - $2 > 10' example.bed
awk '$1 ~ /chr2|chr3/ { print $0 "\t" $3 - $2 }' example.bed
awk 'BEGIN{ s = 0 }; { s += ($3-$2) }; END{ print "mean: " s/NR };' example.bed # mean feature length
awk 'NR >= 3 && NR <= 5' example.bed # lines 3 to 5 only
awk -F "\t" '{print NF; exit}' Mus_musculus.GRCm38.75_chr1.bed # number of columns on 1st line
grep -v "^#" Mus_musculus.GRCm38.75_chr1.gtf | awk -F "\t" '{print NF; exit}' # deals with header (start with #) in gtf file
awk '/Lypla1/ { feature[$3] += 1 };
    END { for (k in feature)
    print k "\t" feature[k] }' Mus_musculus.GRCm38.75_chr1.gtf  | column -t
```

last example:

- two pattern-action pairs separated by `;`
- new variable `feature` introduced: associative array.
  like list but indexed by keys (dictionaries in Python & Julia, hashes in Perl)
- `for` loop, new variable `k` inside.

---

## parameter expansion

use `${variable_name extra stuff}`.

```shell
var="coolname.txt.pdf.md"
i=3678
echo "var=$var and i=$i"
echo "substrings of parameter values: ${i:1} and ${var:4:5}"
echo "strip from the end: ${var%.*}"  # strips shortest occurrence
echo "strip from the end: ${var%%.*}" # strips longest  occurrence
echo "strip from beginning: ${var#*.}"  # strips shortest occurrence
echo "strip from beginning: ${var##*.}" # strips longest  occurrence
echo "substitute: ${var/cool/hot}"
echo "delete:     ${var/cool}"
```

---

## getting data from the web: wget and curl

`wget` not available by default on Mac: get it using Homebrew:
`brew install wget`.

goal: get all lizard data from this
[dryad repository](http://datadryad.org/resource/doi:10.5061/dryad.mm11q).
DNA in ".fasta" files, morphology in ".txt" files.


```shell
mkdir lizard; cd lizard
wget http://datadryad.org/resource/doi:10.5061/dryad.mm11q # gives link to data files
ls # new file: dryad.mm11q
grep "fasta" dryad.mm11q
grep ".txt" dryad.mm11q
grep "fasta" dryad.mm11q | wc # 6 fasta files
wget --accept *.fasta* --accept *.txt* -r -l 1 -nd http://datadryad.org/resource/doi:10.5061/dryad.mm11q
```

`wget` can download files recursively: `-r`, but dangerous (aggressive). put limits with options:

- `-l` to limit the level, or maximum depth: `-l 1` to go only 1 link away
- `--accept xxx` to limit what's accepted: here fasta or txt files.

`nd` or `--no-directory`: to not re-create the directory hierarchy  
lots of other options, like: `--no-parent`, `-O`, `--user`, `--ask-password`, `--limit-rate`

The host may block your IP address if you are downloading too much too fast.

`curl` writes to standard output.

`curl http://datadryad.org/bitstream/handle/10255/dryad.56970/cten_16s.fasta?sequence=1`

- can use more protocols, like `sftp`
- can follows redirected pages with `--location`
- some options: `-O`, `-o`, `--limit-rate`  
`-I` or `--head`: to get header only. On ftp files: file size  
`-s`: silent, no progress meter, no error message
`-#`: simple progress bar, no progress meter

## connecting to remote machines: scp, ssh

`ssh`: secure shell

```shell
ssh ane@desk22.stat.wisc.edu # need to authenticate. password: # characters not shown
hostname
logout
hostname # just in case I switch a lot and don't remember
cat ~/.ssh/known_hosts
ssh desk22.stat.wisc.edu # login name not needed if same as on local machine
cd private/st679/
ls
emacs -nw notes/statservers.md # or nano: no new window. ^X^C to quit.
logout
```

To use an editor that needs a new window: need to enable X11 forwarding.
can be a headache, and can makes things a lot slower.

To avoid typing your password each time: copy the *public* key from your laptop
(in `id_rsa.pub`) to the file `~/.ssh/authorized_keys` on the remote server.
You created a key pair earlier for github, and copied your public key to your
github profile.

`scp`: secure copy. Same as `cp`, but need to provide user name,
machine name and full path on the remote machine. works over ssh.

```shell
scp ane@desk22.stat.wisc.edu:private/st679/notes/statservers.md ../notes/
cd ..
ls -l notes/statservers.md
scp -r desk22.stat.wisc.edu:private/st679/coursedata/hw1-snaqTimeTests/log .
ls -l
ls -l log/
echo "hi Cecile" > coolfile
scp coolfile ane@desk22.stat.wisc.edu:private/ # works both directions
```

slight difference between cp and scp:  
`cp log/ target/path/` copies the *content* of the `log/` directory  
`cp log  target/path/` copies the directory itself *and* its content

```shell
rm -rf log/
cp -r coursedata/hw1-snaqTimeTests/log/ .
ls -l
cp -r coursedata/hw1-snaqTimeTests/log .
ls -l log/
rm -rf *.log log/
```


---
[previous](notes1011.html) & [next](notes1018.html)
