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
** locust -f locust_files/my_locust_file.py --host=http://example.com (Used a specified locust file)
* Specify number of users and hatch rate to launch load
** Open GUI at http://127.0.0.1:8089 (if you are running Locust locally)
