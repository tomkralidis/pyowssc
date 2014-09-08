[![Build Status](https://travis-ci.org/tomkralidis/pyowssc.png?branch=master)](https://travis-ci.org/tomkralidis/pyowssc)

Python OGC Web Services Status Checker
======================================

This library implements simple service status checking. 

Installation
------------

```bash
virtualenv pyowssc
cd pyowssc
. bin/activate
git clone https://github.com/tomkralidis/pyowssc.git
cd pyowssc
pip install -r requirements.txt
python setup.py build
python setup.py install
```

Running
-------

From command line:
```bash
# initial setup
pyowssc-admin.py init
# add a service
pyowssc-admin.py add_service OGC:WMS http://host/wms
# delete a service
pyowssc-admin.py delete_service http://host/wms
# show simple app (default port 8000)
pyowssc-admin.py run
# show simple app on specific port
pyowssc-admin.py run -p 8881
```
