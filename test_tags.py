#!/usr/bin/env python
import re

s = "I love #stackoverflow because ###people are very #helpful!"
#tags = set([re.sub(r"(\W+)$", "", j) for j in set([i for i in s.split() if i.startswith("#")])])
tags = list(map(lambda s:s.replace('#',''),re.findall(r'\B#\w*[a-zA-Z]+\w*', s)))
print(tags)
