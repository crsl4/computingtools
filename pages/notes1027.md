---
layout: page
title: 10/27 notes
description: course notes
---
[previous](notes1025.html) & [next](notes1101.html)

---

## introduction to python

[software carpentry workshop](http://swcarpentry.github.io/python-novice-inflammation/)  
ipython notebook #1: [download](../assets/iPythonNotebooks/swcarpentry1.ipynb)
or [view](https://github.com/cecileane/computingtools/blob/gh-pages/assets/iPythonNotebooks/swcarpentry1.ipynb) (input only)  
ipython notebook #2: [download](../assets/iPythonNotebooks/swcarpentry2.ipynb)
or [view](https://github.com/cecileane/computingtools/blob/gh-pages/assets/iPythonNotebooks/swcarpentry2.ipynb) (input only)  
[code](https://github.com/swcarpentry/python-novice-inflammation/tree/gh-pages/code)
from software carpentry

[10/25 notes](notes1025.html) with basic python types etc.

## regular expressions in python

recall regular expression
[syntax](http://cecileane.github.io/computingtools/pages/notes0922.html#regular-expressions-regexp) from 9/22 notes  
see [notebook 2](https://github.com/cecileane/computingtools/blob/gh-pages/assets/iPythonNotebooks/swcarpentry2.ipynb), but quick reference summary here.

operate on **strings** for simple things:
 `.strip`, `.split`, `.join`, `.replace`, `.index`, `.find`, `.count`,
 `startswith`, `.endswith`, `.upper`, `.lower`

otherwise use the **re library** and its functions
`re.search`, `re.findall`,  `re.sub`, `re.split` etc.

- `r''` to write the regular expression pattern
- multipliers are greedy by default: `*`, `+`, `?`. Add `?` to make them non-greedy
- info from match objects: `.group`, `.start`,  `.end`  
  when pattern not found: match object is None: False as a boolean
- capture with parentheses in the regular expression  
  captured elements in `.group(1)`, `.group(2)` etc. in the match object  
  recall captured elements with `\1`, `\2` etc. in a regular expression,
  to use them in a replacement for example

---
[previous](notes1025.html) & [next](notes1101.html)
