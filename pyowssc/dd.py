#!/usr/bin/python

import sys
from pyowssc import model
from pyowssc import view

if len(sys.argv) != 3:
    print 'Usage: %s <service_type> <url>' % sys.argv[0]
    sys.exit(1)

s = model.Service(sys.argv[1], sys.argv[2])
s.test()

format = view.Xml()
results = format.encode(s)
print results
