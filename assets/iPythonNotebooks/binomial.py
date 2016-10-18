#!/usr/bin/env python

import math

def logfactorial(n, denom=0):
    """calculate the log of factorial n: log(1) + ... + log(n).
    If denom is provided, calculates: log(denom+1)+ ... + log(n).

    Requires integer, non-negative arguments, but does not require denom<n.
    If denom >= n then returns 0.
    Examples:

    >>> round(math.exp(logfactorial(5)),5)
    120.0
    >>> round(math.exp(logfactorial(5,3)),5)
    20.0
    >>> round(math.exp(logfactorial(5,5)),5)
    1.0
    >>> round(math.exp(logfactorial(5,6)),5)
    1.0
    """
    assert type(n)==int, "argument to logfactorial should be an integer"
    assert n>=0, "argument to logfactorial should be non-negative"
    assert type(denom)==int, "argument to logfactorial should be an integer"
    assert denom>=0, "argument to logfactorial should be non-negative"
    res = 0
    for i in range(denom,n):
        res += math.log(i+1)
    return res

def choose(n, k, log=False):
    """returns the binomial coefficient choose(n,k)
    for non-negative integers n and k.
    If log=True, returns the log of the binomial coefficient.
    Examples:

    >>> round(choose(5,3),5)
    10.0
    >>> round(choose(5,0),5)
    1.0
    >>> round(choose(500,410,True),5)
    232.62616
    """
    assert k <= n, "choose(n,k) requires k <= n"
    # other option: return 0 if not log, -infinity if log
    logres = logfactorial(n,k) - logfactorial(n-k)
    return logres if log else math.exp(logres)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print("done with tests")
    print("there are",choose(10,2),"ways to choose 2 people in a group of 10.")
