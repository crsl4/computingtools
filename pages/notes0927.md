---
layout: page
title: 9/27 notes
description: notes, links, example code, exercises
---
[previous](notes0922.html) & [next](notes0929.html)

---

## homework

Submit your solution to exercises 1 & 2 of homework 1
using git and github: see
[instructions](https://github.com/UWMadison-computingtools/coursedata#commit-push-and-submit-your-work).
Make sure

- your code is annotated with comments in the scripts
- you have readme files to give higher-level explanations and all
  the tools (commands) to reproduce your results.

## Git: track and share versions of a project

- you take snapshots of your project once in a while. one "commit" = one snapshot
- git stores the changes between snapshots, not the whole files
- git stores its data (changes) in a special `.git` directory
- you can easily restore the whole project to a previous snapshot, then
  get back to the latest snapshot
- each collaborator has the project on her/his local machine, and
  another remote copy of the project is on GitHub.
  Collaborators can "pull" from GitHub and "push" to GitHub.

### first examples

history of repository for the course website:

```shell
git log --abbrev-commit --graph --pretty=oneline --all --decorate
```

example when it was useful to get back to an old version:

![email about recovering old version](../assets/notesFigs/navigateGitHistory_email.png)

we can get the old version of this file in a few clicks:

- go to the project on [github](https://github.com/crsl4/PhyloNetworks.jl)
- click on "863 commits" (or whatever the number is) near top left
- scroll down to a commit that seems to have affected our file of interest

![scrolling git history](../assets/notesFigs/navigateGitHistory_repo3.png)

- click on "Browse the repository at this point in the history"
  to see all the files as they were *just before* the change that affected our
  file (June 8th). Tada!
- notice the commit SHA near the top: "Tree: 019f0ff78d".
  Click on it to get back to the current version of the files, typically
  "Branch: master"

---
let's create a repository from our corn SNPs project

```shell
cd ~/Documents/private/st679/zmays-snps
ls -lR
git init # initialize repo: creates .git/
git status
git add readme.md data/readme # git now tracks these files
git status
echo "Zea Mays SNP Calling Project" >> readme.md
cat readme.md
git status # readme.md is tracked, previous version in staging area, new version not
```

### commits, staging area, working directory

commit -- ... -- commit -- staging area -- working directory: tracked files, untracked files

```shell
git diff # differences between new version and staged area (if present) or last commit
git add readme.md # adding new edits to staging area
git status        # readme.md only in staging area
git diff          # no differences btw working dir and staging area
git diff --staged # diff between staging area and last commit
```

now take the snapshot

```shell
git commit -m "initial commit, main readme only"
```
With `git commit` only, an editor will show up to let you edit your
commit message. If you get a weird-behaving editing window (vim),
type `:q!` (to quit without saving) then change your git configuration to use
nano instead of vim:

```shell
git config --global core.editor nano
```

### commit messages

- first line: title
  * informative. forbidden: "update", "continued", "new code", "misc", "edits"
  * 50 of fewer characters is strongly recommended
- if more explanations are needed: add one blank line
- then your explanation paragraph

informativeness: helps to recover old versions (example above)  
separation of title vs paragraph: good example
[here](https://github.com/crsl4/PhyloNetworks.jl/commit/310a81a90db2661bbba3efae1db2378d3f15f88b), suboptimal example
[here](https://github.com/khabbazian/l1ou/commit/bc8df7a9caffbb06d7bef298bdf6c5f7c1df92f9)

### looking at history

let's check:

```shell
git show   # shows last commit: title, paragraph, diffs: change "hunks"
git status # nothing in staging area, but some files not tracked
git log
```

add more edits:

```shell
echo "Project started 2016-09-14" >> readme.md
git diff
git commit -a -m "added project info to main readme"
git log
```

option `-a` in git commit: to add all changes in tracked file to the commit.

### use git to move or delete tracked files

```shell
git mv data/readme data/readme.md
git status
git commit -m "added markdown extension to data readme"
git log
```

### what files (not) to track / commit

track:

- scripts
- text documentation with metadata: explain where the data are archived,
  how to reproduce result files
- notebooks (code + explanations + interpretations) in text format
  (md or html): but preferably only final version of 'compiled'/knitted version.

do **not** track:

- large files that can be reproduced by the pipeline
- large data files: if can be obtained from outside archive
- binary files: document where they were obtained or how to recompile
- pdf and figures: document how they can be reproduced

We can tell git to ignore files that we do not want to track.

```shell
touch .gitignore
echo "data/seqs/*.fastq" >> .gitignore
cat .gitignore
git status # fastq files not listed anymore. but need to track .gitignore
git commit -a -m "added .gitignore, to ignore large fastq data files"
git status # all good
```

### your turn

- how would you turn an existing git repository into a normal benign folder?
- go to your work folder (containing homework 1 only, for now):
  * ask git to track your script(s) for homework 1
  * commit your work
  * add some more documentation / explanations
  * commit these new changes
  * add something silly: like remove 1 or 2 lines, as if accidentally (and save).  
    make sure you had committed your work **before** saving these mistakes.

### using older commits to fix mistakes

```shell
echo "todo: ask sequencing center about adapters" > readme.md
cat readme.md # oops
git status    # git tells us how to undo our change
git checkout -- readme.md # to checkout 'readme.md' from the last commit
cat readme.md # yes!
git status
```

your turn: undo your mistake from above

What if the mistake has been staged?

```shell
echo "todo: ask sequencing center about adapters" > readme.md
git add readme.md
git status  # again, follow git's instructions
git reset HEAD readme.md
git status
cat readme.md # mistake still there, but unstaged
git checkout -- readme.md
cat readme.md # yes!
git status
```

### pushing to github and working with others

various repositories:
cecile (laptop) -- central (claudia's github) -- claudia (laptop)  
we can: `git push`, `git clone`, `git pull`, `git fetch` (to check before), `git merge`

Push your homework to github:

```shell
git branch # to double-check which branch you are on. default: master
git remote -v # check the nickname for your central (github) repo. default: origin
git push origin master # pushes current local branch to repo "origin", its branch "master"
```

## changing your sheel prompt

variable PS1 contains your shell prompt (prompt string):

```shell
echo $PS1 # save this output, to go back to original prompt in same session
PS1="hiCecile% "
PS1="hiCecile$ "
PS1="$ "
PS1="\$(parse_git_branch)$ "
PS1="\[\033[33m\]\$(parse_git_branch)$ "
PS1="\[\033[33m\]\$(parse_git_branch)\[\033[00m\]$ "
```

The last one shows if you are in a git repository, and if so,
the name of the current branch that's checked out.

These changes affect your current session only.
To affect future sessions: pick the one you like best and add this at
the end of your file `~/.bash_profile`:

`export PS1=preferred_choice_here`

---
[previous](notes0922.html) & [next](notes0929.html)
