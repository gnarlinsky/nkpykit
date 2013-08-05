=======================
nkpykit [0]_
=======================

.. contents::


Decorators
===========
``callinfo``
--------
Keeps track of and prints call count and parameter name/value info, with
multiple colors for readability.


* **Count individual function calls:**

``` python
>>> from nkpykit.dec import callinfo
>>>
>>> @callinfo
... def a(): pass
...
>>> a(); a(); a()
a(): call #1 ( )
a(): call #2 ( )
a(): call #3 ( )
>>> a.count()
3
```

* **Ask for all decorated functions' call counts:**
``` python
>>> from nkpykit.dec import callinfo
>>>
>>> @callinfo
... def a(): pass
...
>>> @callinfo
... def b(): pass
...
>>> a(); a(); a()
>>> b(); b()
>>> callinfo.all_counts()
{'a': 3, 'b': 0}
```

* **Reset an individual function's call count:**
``` python
>>> from nkpykit.dec import callinfo
>>>
>>> @callinfo
... def a(): pass
...
>>> a(); a(); a()
a(): call #1 ( )
a(): call #2 ( )
a(): call #3 ( )
>>> a.count()
3
>>> a.reset_count()
>>> a.count()
0
```

* **Reset all decorated functions' call counts:**
``` python
>>> from nkpykit.dec import callinfo
>>>
>>> @callinfo
... def a(): pass
...
>>> @callinfo
... def b(): pass
...
>>> a(); a(); a(); b(); b()
>>> callinfo.all_counts()
{'a': 3, 'b': 2}
>>> callinfo.reset_all_counts()
>>> callinfo.all_counts()
{'a': 0, 'b': 0}
```

* **See all currently registered/decorated functions:**
``` python
>>> from nkpykit.dec import callinfo
>>>
>>> @callinfo
... def a(): pass
...
>>> @callinfo
... def b(): pass
...
>>> callinfo.all_func()
{<function a at 0x1005c52a8>: <nkpykit.dec.callinfo object at 0x1004ea450>,
<function b at 0x1005c5668>: <nkpykit.dec.callinfo object at 0x1004f6910>}
```

* **Keep track of parameter names and values, including default keyword arguments:** 
``` python
>>> from nkpykit.dec import callinfo
>>>
>>> @callinfo
... def a(foo, key1=1, key2=2, key3=3):
...     print foo, key1, key2, key3
...
>>> a('hi', key2=200)
a(): call #1 ( foo = hi, key1 = 1, key2 = 200, key3 = 3, )
hi 1 200 3
```

Here's what happens with recursion [1]_:
``` python
>>> from nkpykit.dec import callinfo
>>>
>>> @callinfo
... def merge(left, right):
...     result = []
...     i, j = 0, 0
...     while i < len(left) and j < len(right):
...         if left[i] <= right[j]:
...             result.append(left[i])
...             i += 1
...         else:
...             result.append(right[j])
...             j += 1
...     result += left[i:]
...     result += right[j:]
...     return result
...
>>> @callinfo
... def mergesort(lst):
...     if len(lst) <= 1:
...         return lst
...     middle = int(len(lst) / 2)
...     left = mergesort(lst[:middle])
...     right = mergesort(lst[middle:])
...     return merge(left, right)
...
>>> mergesort([3, 4, 8, 0, 6, 7])
mergesort(): call #1 ( lst = [3, 4, 8, 0, 6, 7], )
mergesort(): call #2 ( lst = [3, 4, 8], )
mergesort(): call #3 ( lst = [3], )
mergesort(): call #4 ( lst = [4, 8], )
mergesort(): call #5 ( lst = [4], )
mergesort(): call #6 ( lst = [8], )
merge(): call #1 ( left = [4], right = [8], )
merge(): call #2 ( left = [3], right = [4, 8], )
mergesort(): call #7 ( lst = [0, 6, 7], )
mergesort(): call #8 ( lst = [0], )
mergesort(): call #9 ( lst = [6, 7], )
mergesort(): call #10 ( lst = [6], )
mergesort(): call #11 ( lst = [7], )
merge(): call #3 ( left = [6], right = [7], )
merge(): call #4 ( left = [0], right = [6, 7], )
merge(): call #5 ( left = [3, 4, 8], right = [0, 6, 7], )
[0, 3, 4, 6, 7, 8]
```

More examples will be in the test files.

Other decorators
---------------
*(in progress)*


Not decorators
==============
*(in progress)*


Tests
======
``callinfo``
------------
*(in progress)*


Future/Wishlist
=============
*(currently being drafted, will be here and/or in Issues)*


.. [0] Yeah, there's definitely some wheel reinvention here. So? :)
.. [1] The merge sort code below is based on the code at http://en.literateprograms.org/Merge_sort_(Python)?oldid=19008.
