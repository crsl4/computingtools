---
layout: page
title: 12/15 notes
description: course notes
---
[previous](notes1208.html)

---

## job scheduling with slurm

### simple test example

This slurm script, in file `echo_submit.sh`,
runs a pair of `echo` commands 10 times:

```shell
#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cecile.ane@wisc.edu
#SBATCH -o screen/echo_%a.log
#SBATCH -J echo
#SBATCH --array=0-9

# to get Perl to send emails:
export PERL5LIB="/s/slurm/lib/perl/5.18.2"

# launch the "echo" script
echo "slurm task ID = $SLURM_ARRAY_TASK_ID"
echo "today is $(date)" > output/echo_$SLURM_ARRAY_TASK_ID.out
```

The key line that makes 10 repeats is `#SBATCH --array=0-9`.
This line also creates a shell variable `SLURM_ARRAY_TASK_ID`,
which is used as we would with any other shell variable.  
The first `echo` command produces standard output written to
a file `screen/echo_?.log`.  
The second `echo` produces an output file `output/echo_?.out`.  
To run the script:

```shell
sbatch echo_submit.sh
```

### example to run a bunch of julia scripts

Save the following script in file `onesnaq_submit.sh`:

```shell
#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cecile.ane@wisc.edu
#SBATCH -o snaq/onesnaq_%a.log
#SBATCH -J onesnaq
#SBATCH --array=0-239

# to get Perl to send emails:
export PERL5LIB="/s/slurm/lib/perl/5.18.2"

# use Julia packages in /worskpace/, not defaults in ~/.julia/ (on AFS):
export JULIA_PKGDIR="/workspace/ane/.julia"

# launch Julia script, using Julia in /workspace/ again, with full paths:
echo "slurm task ID = $SLURM_ARRAY_TASK_ID"
/workspace/software/julia-0.5.0/julia /workspace/ane/timetest/onesnaq.jl 1 30 $SLURM_ARRAY_TASK_ID
```

It will run the julia script [`onesnaq.jl`](../assets/julia/onesnaq.jl)
(last line) 240 times (from `#SBATCH --array=0-239`).  
The julia script gets 3 arguments: 1, 30, and the value of
`SLURM_ARRAY_TASK_ID` (0,1,...,239).
Julia will use this last integer argument to set an array of parameter values.

**preparation**

- copy your input file, julia file, submit file etc:

```shell
scp onesnaq* lunchbox.stat.wisc.edu:/workspace/ane/timetest/
```

- `ssh` to lunchbox and go to your folder in `workspace`.
- check that the julia script is working, by running it once,
  with the 3<sup>rd</sup> argument set to 0 for instance:

```shell
export JULIA_PKGDIR="/workspace/ane/.julia"
/workspace/software/julia-0.5.0/julia onesnaq.jl 1 30 0
```

**run slurm**

- run the slurm script for a few trials only, to run the julia script
  3 times only (not 240 times yet):

```shell
sbatch onesnaq_submit.sh --array=0-2
squeue
```

- monitor the jobs for these first few trials, predict the running time
  for the full 240 julia runs.
- run the full array of 240 jobs:

```shell
sbatch onesnaq_submit.sh
squeue
```

### converting the array task ID

single integer: but can be used to set parameter values
within your Julia/Python/R script.  
example: run this Julia command with various values
for `Nfail`, and for tolerance parameters `ftolAbs` etc.
to stop the likelihood optimization:

```julia
snaq!(startingNet, tableCF, hmax=h, Nfail=NF,
      ftolAbs=FTA, ftolRel=FTR, xtolRel=XTR, xtolAbs=XTA,
      liktolAbs=LTA, runs=runs, seed=s, filename=rootname)
```

We want to have these parameters take these values:

```julia
lFTA = [0.000001, 0.00001, 0.0001, 0.001, 0.01]
lNF    = [100, 75, 50, 25]
lRatio = [1, 100, 10000]   # controld LTA: Ratio=LTA/FTA
lXTR   = [0.001,    0.01]
lXTA   = [0.000001, 0.001]
```

It makes for a total of 5\*4\*3\*2\*2 = 240 combinations of parameter values,
so 240 calls to the `snaq!` function.
We can convert an integer in 0,...,239 into exactly one combination
with the `comb` function below.
To explain its algorithm,
imagine that we only had the first 2 parameters to vary: FTA and NF,
with a total of 5\*4 = 20 combinations. The algorithm would map:

- the first 5 integers 0,1,2,3,4 to NF=100
- the next 5 integers 5,6,7,8,9 to NF=75
- ...
- the last 5 integers 15,16,17,18,19 to NF=25.

Within each set of 5 integers, the first would get FTA=0.000001, ...,
and the 5<sup>th</sup> would get FTA=0.01.
To code this, we do the integer division of the input integer `i` by 5
(number of FTA values) using `d,r = fldmod(i,5)`

- the remainder `r` is in 0,...,4 and gives us the index for the FTA value
- the quotient `d` is in 0,...,3 (i<20) and gives us the index for the NF value.

In general, we would again divide `d` by 4 (number of values for NF), and so on.

```julia
nparams = 5
nlevels = [length(lFTA),length(lNF),length(lRatio),length(lXTR),length(lXTA)]
"""
comb(index of parameter combination)

Take an integer as input, return a tuple of parameter values.
External objects are used: nparams, nlevels, and lFTA etc.
The integer input should be between 0 and 239, or
between 0 and the total # combinations -1 in general.
index 0 -> first values of all parameters
index 239 -> last values of all parameters
"""
function comb(combID)
  paramID = Vector{Int}(nparams)
  d = combID
  for par in 1:nparams
    d,r = fldmod(d, nlevels[par]) # combid = d * nlevels + r
    paramID[par] = r+1 # indexing in parameter list starts at 1, not 0
  end
  println("parameter levels: ",paramID)
  return lFTA[paramID[1]], lNF[paramID[2]], lRatio[paramID[3]], lXTR[paramID[4]], lXTA[paramID[5]]
end

FTA, NF, Ratio, XTR, XTA = comb(id)
LTA = FTA*Ratio;
```

---
[previous](notes1208.html)
