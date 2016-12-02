---
layout: page
title: 12/6 notes
description: course notes
---
[previous](notes1117.html) & [next](notes1208.html)

---

## homework

before today:

- install [julia](http://julialang.org) v0.5.0:
  * click on "downloads" then choose the command-line version for your system
  * On a Mac, I had to add the path to julia to my PATH shell variable,
    in file  `~/.bash_profile`:

    `export PATH="$PATH:/Users/ane/.julia/v0.5/Conda/deps/usr/bin"`

  * on Statistics servers: Julia is already installed in `/s/julia-0.5.0`.
    Simply add its path to your PATH variable: add to your file `~/.bashrc.local`
    this line:

    `export PATH="$PATH:/s/julia-0.5.0/bin"`

  * open a terminal and type "julia" to check that it works, then type
    `quit()` to close it.

- in jupyter lab: check that Julia 0.5.0 is available as a kernel
- in Atom: click on Packages, Setting View, Install Packages.
  In the new window, type "language-julia", click "Packages", then "Install".
  This "language-julia" package will highlight
  julia syntax for files with extension `.jl`.


## introduction to Julia

jump to:

- [types](#types)
- [(im)mutable](#immutable-types) types
- [modes](#modes)
- [JIT](#just-in-time-jit-compiled) compiled: fast, type declaration not needed
- type [stability](#type-stability)
- [syntax](#syntax-overview) overview: functions, docstrings, tests, loops

### types

- `Bool`: `true` and `false`
- `String` (double quotes) and `Char` (single quotes)
- floating point numbers: `Float16`, `Float32`, `Float64`;
  `Float` depends on the machine
- integers: `Int8`, `Int16`, `Int32`, `Int64`, `Int128`;
  `Int` depends on the machine
- unsigned (positive) integers: `UInt8` etc.
- arrays: somewhat like lists in Python
- tuples: like in Python, e.g. `(3,)` or `(3,"hohoho")`
- Vector (Matrix): shortcut for 1-dimensional (2-dimensional) array
- dictionaries: `Dict`

```julia
typeof(3)
Int
typeof(3.0)
typeof("hello")
a=[10,6,3,2] # Array{Int64,1}: 1-dimensional array, contains Int64 values
a[1]
push!(a,5)
push!(a,5.0) # converted 5.0 to Int to maintain type of "a"
push!(a,5.1) # error
convert(Array{Float64,1}, a) # new object
b = [1,6,3.0,2] # Array{Float64,1}: 1-dimensional, values converted to Float64
push!(b,5.1) # no problem
push!(b, "hello") # error
splice!(b,2:3)
b
c = ["hello", 3, "world", 5.1] # Array{Any,1}: contains anything possible
Vector{Int}
UInt8(4)
UInt8[8,9,10,11]
d = [1 2 3; 6 7 8] # 2-dimensional array, 2*3. note syntax
h = Dict("blue"=>10, "green"=>20)
```

julia is **1-indexed** (unlike Python, like R)  
convention: functions with a bang `!` modify one or more of their arguments.
Respect it!

```julia
b = [1,6,3,2]; # ; suppresses screen output
sort(b)
b
sort!(b) # same return value
b
pop!(b) # no pop() function
```

how to initialize arrays:

```julia
Vector(3)
Vector{Int}(3)
Array{Int}(3)    # uninitialized
Array{Int8}(3,4) # 2-dimensional array: 3x4
zeros(3) # Float by default
ones(3)
zeros(Int,3)
zeros(Bool,3)
```

see limits [here](http://docs.julialang.org/en/release-0.5/manual/integers-and-floating-point-numbers/)
and mind them, because potential errors otherwise:

```julia
x=2^63-1 # upper limit for Int64: 1bit for sign and 63 bits of 1
typemax(Int64)
x*2      # wrong! overflow
```
quasi-object-oriented: new types can be defined.  
types have fields, but no methods: functions have multiple methods instead
--more below.

### (im)mutable types

mutable: arrays, composite types (typically)  
immutable: numbers, tuples, strings

### modes

- help mode: type "?" in the REPL. goes back to julia mode right after.
- shell mode: type ";". goes back to julia mode right after.
- R mode (kinda): type "$", `using RCall` package.
  backspace to go back to julia mode.

### just-in-time (JIT) compiled

```julia
function foo(x)
  return x+1
end

foo(x) = x+1 # one-line form
```

let's use this function on various inputs:

```julia
foo(3) # compiles foo for Int arguments
foo(7) # re-use compiled foo(Int)
foo(7.2) # compiles a different version for Float64 arguments
foo([1,2,7,9]) # compiles 3rd version for Array{Int64,1}
code_llvm(foo, (Int,)) # inspect generated code
code_llvm(foo, (Float64,))
code_llvm(foo, (Array{Int64,1},))
code_native(foo, (Int,))
code_native(foo, (Float64,))
code_native(foo, (Array{Int64,1},))
```

Julia uses the type of the arguments to infer which compiled version to run:
multiple dispatch

- makes it really [fast](http://julialang.org)
(scroll down to High-Performance JIT Compiler)
- rare need to declare input types:

```julia
function addone(x::Number)
  return x+1
end
addone(3.5)
addone([1 2; 6 7])
```

better and no penalty because different
compiled versions for different input types anyway:

```julia
function addone(x) # no type declaration
  return x+one(1)  # + or one() will throw error is bad type
end
addone(3.5)
addone([1 2; 6 7])
```

### type stability

- a variable keeps the same type throughout
- a function returns an output with the same type for all input of a given type

crucial to make your code fast: compilation can be more efficient.
example from [here](http://www.johnmyleswhite.com/notebook/2013/12/06/writing-type-stable-code-in-julia/):

```julia
function sumofsins1(n::Integer)  
    r = 0  
    for i in 1:n  
        r += sin(3.4)  
    end  
    return r  
end  
```
version 2 with `r` initialized at `0.0`:

```julia
function sumofsins2(n::Integer)  
    r = 0.0  
    for i in 1:n  
        r += sin(3.4)  
    end  
    return r  
end
```

let's use these functions, check output type:

```julia
sumofsins1(0)
typeof(sumofsins1(0))
sumofsins1(1)
typeof(sumofsins1(1))
typeof(sumofsins2(0))
```

and compare their running time:

```
@time sumofsins1(100_000)
@time sumofsins2(100_000)

@time [sumofsins1(100_000) for i in 1:1000]
@time [sumofsins2(100_000) for i in 1:1000]
```

Julia has tools to diagnose type instability problems:

```julia
@code_warntype sumofsins2(3)
@code_warntype sumofsins1(3)
```

### syntax overview

docstring before the function:

```julia
"""
foo(x)

calculate x+1
"""
function foo(x)
  return x+1
end
```

`if` statements for tests:

```julia
x=5; y=6.2
if x>6 || y>6
  println("x or y is >6")
end
x>6 || error("x is not greater than 6: can't continue")
x>6 || warn("oops, x not >6, is this normal?")
x>6 && info("checked: x is greater than 6")

function test(x,y)
  if x ≈ y # type \approx then TAB. Same as isapprox(x,y).
    relation = "(approx) equal to"
  elseif x < y
    relation = "less than"
  else
    relation = "greater than"
  end
  println(x, " is ", relation, " ", y, ".")
end
test(x,y)
1.1+0.1 == 1.2
test(1.1+0.1, 1.2)

isxbig = x>3 ? "yes" : "no" # ternary expression: very short if/else
```

flow control with loops:

```julia
for i in 1:10^9 # this a Range object: very small
  println("i=",i)
  if i<3
    continue
  end
  # above, same as: i<3 && continue
  println("\t2i=", 2i) # * not needed
  i<6 || break
end
i # not defined!!
nmax=100_000
n=0
while n<nmax
  print("n=",n,"\r") # \r to "return carriage" only: re-write on same line
  n += 1
end
```

list comprehension:

```julia
paramvalues = [10.0^i for i in -3:2]
[v^2 for v in paramvalues if v >= 0.1]
h = Dict("xtolrel"=>0.01, "xtolabs"=>0.001, "Nfail"=>50)
h["xtolrel"]
[h[k]*2 for k in keys(h)]
[a * 10.0^i for i in -3:2 for a in [1,2]] # 1-dim
[a * 10.0^i for i in -3:2,    a in [1,2]] # 2-dim
```

---
[previous](notes1117.html) & [next](notes1208.html)
