Locust Usage
======
**Locust** is an open source load testing tool.

## Home Page
http://locust.io/
Doc: http://docs.locust.io/en/latest/

## Install
```
$ sudo pip install locustio

# Install dependency
$ pip install -r requirements.txt
```

## Usage
* Start Locust, by typical commands as follows:
** locust --host=http://example.com (Will use locustfile.py in current directory)
** locust -f ambry_load.py --host=http://192.168.33.21:1174 (Used a specified locust file)
** locust -f ambry_balanced_load.py --host=http://192.168.33.21:1174 (A list of hots was specfied inside the file, and will chose one of them randomly for each task execution. Still need the --host option, although useless.)
* Specify number of users and hatch rate to launch load
** Open GUI at http://127.0.0.1:8089 (if you are running Locust locally)
