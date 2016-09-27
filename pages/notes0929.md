---
layout: page
title: 9/29 notes
description: course notes
---
[previous](notes0927.html) & [next](notes1004.html)

---

## homework

due T 10/4: submit your solution to exercises 1 & 2 of homework 1
using git and github: see
[submission instructions](https://github.com/UWMadison-computingtools/coursedata#commit-push-and-submit-your-work).
Also see the [grading rubric](https://github.com/UWMadison-computingtools/coursedata#grading-rubric). Make sure

- your code is annotated with comments in the scripts
- you have readme files to give higher-level explanations and all
  the tools (commands) to reproduce your results.
- you do *not* need to commit the input files (in `out/` and `log/` directories).
  I already have them. No big deal if you did already, though.

## Git: continued

- [using git for hw 1](#recap-from-last-time-using-your-homework)
- [pushing to / pulling from github to work with others](#pushing-to--pulling-from-github-to-work-with-others)
- [resolving conflicts: merge commits](#resolving-conflicts-and-merge-commits)
- [checking out older versions](#checking-out-older-versions)
- [branches](#branches) and [merging branches](#merging-branches)
- [some other git subcommands](#some-other-git-subcommands)
- [sha checksums](#sha-checksums)
- a git-aware [shell-prompt](#changing-your-shell-prompt)

### recap from last time: using your homework

- how would you turn an existing git repository into a normal benign folder?
- go to your work folder (containing homework 1 only, for now):
  * ask git to track your script(s) for homework 1
  * commit your work
  * add some more documentation / explanations
  * commit these new changes
- add something silly: like remove 1 or 2 lines, as if accidentally (and save).  
  make sure you had committed your work **before** saving these mistakes.
- undo these mistakes using git

### pushing to / pulling from github to work with others

various repositories:
cecile (laptop) -- central (claudia's github) -- claudia (laptop)  
we can: `git push`, `git clone`, `git pull`, `git fetch` (to check before), `git merge`

To illustrate this, I will to create a central repository:
new repository owned by "UWMadison-computingtools", say. I'll go to
[github](https://github.com/UWMadison-computingtools), click "New repository",
name it "zmays-snps". Then back to my shell and link my private repository
to the new central repo on github:

```shell
git remote -v
git remote add git@github.com:UWMadison-computingtools/zmays-snps.git
git remote -v
git branch
git push origin master
```

Now let's go back to [github](https://github.com/UWMadison-computingtools/zmays-snps)
to check! Go check the "network" page to visualize the list of commits
(in Graphs tab)

your turn: push your homework to github:

```shell
git branch # to double-check which branch you are on. default: master
git remote -v # check the nickname for your central (github) repo. default: origin
git push origin master # pushes current local branch to repo "origin", its branch "master"
```

Now I need a collaborator. Volunteer? Jonathan?
(check that you can push to github easily: `ssh -T git@github.com` should
give you a "Hi!" message)

Jonathan can pull the repository: first navigate to a directory that is
*not* already a git repository (do `git status` to check). Then:

```shell
# Jonathan doing this:
git clone git@github.com:UWMadison-computingtools/zmays-snps.git
cd zmays-snps
git remote -v
```

Let me can start working on the project, say add metadata info:

```shell
# Cecile doing this:
echo "Samples expected from sequencing facility 2016-09-30" >> README.md
git commit -a -m "added information about samples"
git log --pretty=oneline --abbrev-commit
gl # this is my own alias for "git log" with particular options
type gl
git log --abbrev-commit --graph --pretty=oneline --all --decorate
```

(check the update on github). Jonathan can pull these changes from his shell:

```shell
$ git pull origin master # Jonathan doing this
remote: Counting objects: 5, done.
remote: Compressing objects: 100% (3/3), done.
￼...
From github.com:UWMadison-computingtools/zmays-snps
...
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)
-> FETCH_HEAD
-> origin/master
$ git log --pretty=oneline --abbrev-commit
```

Next, Jonathan can work on the project, say add more metadata still:

```shell
# Jonathan does this. -e to interpret \n as newline
echo -e "\n\nMaize reference genome version: refgen3" >> README.md
git commit -a -m "added reference genome info"
git push origin master
```

and I can get his work easily (also check on github):

```shell
git pull origin master # Cecile doing this
cat README.md
git log # viewed with less
git log -n 2
```

Very important:

- pull often!
- commit your changes before pulling. Any change to an uncommitted file
  would stop the pull update.

### resolving conflicts and merge commits

Now let's create a conflict to see how to resolve it.
Let me and Jonathan make changes to the same file, at roughly the same place:

```shell
# Jonathan does this:
echo -e ", downloaded 2016-09-27 from\nhttp://maizegdb.org into `/share/data/refgen3/`." >> README.md
git commit -a -m "added download info"
git push origin master
```

while I open the README.md file to change the last line to this:

> We downloaded refgen3 on 2016-09-27.

then I also commit and push:

```shell
# Cecile does this:
git commit -a -m "added genome download date"
git push origin master # Ahh, problem!!
```

The push was rejected!
I first need to pull Jonathan's update. Perhaps it will be smooth,
perhaps there will be conflict. If so, it's my responsibility to resolve
the conflicts:

```shell
# Cecile does this:
git pull origin master
git status # conflict. tells me what to do to resolve it
git log --pretty=oneline --abbrev-commit
```

I need to edit the file with the conflict: git told me it's `README.md`,
then search for:

- `<<<<<<< HEAD` : beginning of my version, then
- `=======` boundary: end of my version and beginning of fetched version, then
- `>>>>>>> SHA value`: end of new, fetched version,
  with Jonathan's commit indicated by its SHA.

I can now edit this file and remove these 3 marks (there may be multiple blocks
of conflicts, each with these 3 marks). Let me replace both versions with
some improved information:

  > We downloaded the B73 reference genome (refgen3) on 2016-09-27 from
  > http://maizegdb.org into `/share/data/refgen3/`.

let's continue to follow git's instructions:

```shell
# Cecile doing this:
git status
git add README.md
git status
git commit -a -m "resolved merge conflict in README.md"
git status
git log --abbrev-commit --pretty=oneline --graph
git push origin master
```

last step: quickly push the conflict resolution before Jonathan
does some more work. Lesson: both Jonathan and I should pull often!

```shell
# Jonathan does this:
git pull origin master
git log --graph
```

- merge commits have 2 parents, unlike usual commits.
- if you feel overwhelmed during a merge, do `git merge --abort`
  and start the various merge steps from scratch.
- remember: `git status` gives instructions

### checking out older versions

Let's recover some old version now, then go back to latest committed version:

```shell
git log # copy-paste the SHA from this result to xxx and yyy below
git checkout xxx -- README.md
cat README.md
gl # using my alias
git checkout yyy -- README.md
```

### branches

Branches are very useful to easily switch back and forth between different
versions. Each version can still evolve.

Imagine that I want to develop a new aspect of the project, not ready to
work with the rest of the pipeline --say risky edits to the README file (!):

```shell
git branch readme-changes # creates a branch
git branch # lists the existing branches
git checkout readme-changes # switches the current branch
git branch
git log --abbrev-commit --graph --pretty=oneline --all --decorate
```

Now let me make a bold move and make thorough edits to my README file,
then commit my changes:

```shell
git commit -a -m "reformatted readme, added sample info"
git log --abbrev-commit --pretty=oneline -n 3
git branch
git checkout master
git log --abbrev-commit --pretty=oneline -n 3
git log --abbrev-commit --pretty=oneline --graph --all --decorate
cat README.md # old version: on master branch
echo ">adapter-1\\nGATGATCATTCAGCGACTACGATCG" >> adapters.fa
git add adapters.fa # add a new file. on master branch here
git commit -a -m "added adapters file"
git log --abbrev-commit --pretty=oneline --graph --branches -n5
```

Branches are like pointers. They do not hold info. Commits do.

### merging branches

Imagine that I am happy with the new developments done in branch "readme-changes",
and it's ready to be used by my collaborators on the main "master" branch.

```shell
git checkout master
git branch # to triple-check we are on master
git merge readme-changes # no conflict, yes! enter commit message
git log --abbrev-commit --graph --pretty=oneline --all --decorate
git push origin master
```

This is a merge commit with 2 parents:
just like when we resolved a conflict earlier.  
We can use *remote* branches too. Jonathan could pull my changes,
including the new "readme-changes" branch, and switch to it if he wanted
to collaborate on this branch.  
When all done with this branch, I can delete it:

```shell
git branch -d readme-changes
```

<!--
### remote branches

Now Jonathan creates a branch "new-methods" ...
but pull first: remember to pull often!

```shell
# Jonathan does this:
git pull origin master
git branch new-methods
git branch
git checkout new-methods
```
-->

### some other git subcommands

- `git commit --amend` to add change the last commit message.
  But **do not** do this if you already pushed your change to github.
- `git revert` to revert changes (creates a new commit)
- `git reset` and `git rebase`: I very highly recommend that you **do not**
  use them, until you know exactly what you do. Even then, do **not**
  use them if you already pushed your commits to github.
- github provides more options: forks (multiple public repositories),
  pull requests.

### SHA checksums

SHA = security hash algorithm,
used by git to guard again data corruption.  
A small change in the input causes many changes in the SHA value.  
It is a good idea to record the SHA values of important data files
as metadata (in readme file).

```shell
$ echo "this sentence is super cool" | shasum
93aff6c8139fff6855797afc8ea7a7513ffabb6f  -
$ echo "this sentence is duper cool" | shasum
97c250becdaa49c62721478c7f82d116e1039e0e  -
$ shasum data/seqs/* # copy-paste results in readme file
$ md5 data/seqs/*    # alternatively: record MD5 checksums
```

check [RStudio](https://www.rstudio.com/products/rstudio/download/)
download page for MD5 checksums: to make sure that what you get
on your laptop is the true and uncorrupted thing:
`md5 RStudio-downloadedfile.zip` and compare with expected MD5 value.

<!--
example algorithm: consider each pair of byte as an integer in 0-15,
add them all up, return their value modulo 16: hexadecimal code in 0-9a-f
-->

## changing your shell prompt

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

last one: shows if in git repository, and if so,
name of current checked out branch  
to affect future sessions: pick the one you like best and add this at
the end of your `~/.bash_profile` file:
`export PS1=preferred_choice_here`


---
[previous](notes0927.html) & [next](notes1004.html)
