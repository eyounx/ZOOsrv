This repository is out of maintenance. ZOOpt is now in the Ray project for distributed computing.

# ZOOsrv

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/eyounx/ZOOjl/blob/master/LICENSE)

ZOOsrv is the server part of Distributed [ZOOpt](https://github.com/eyounx/ZOOpt). In order to improve the efficiency of handling distributed computing, we use Julia language to code the client end for its high efficiency and Python-like features. Meanwhile, the servers are still coded in Python. Therefore, users programs their objective function in Python as usual, and only need to change a few lines of the client Julia codes (just as easy to understand as Python). 

**Documents:** [Wiki of Distributed ZOOpt](https://github.com/eyounx/ZOOpt/wiki/Tutorial-of-Distributed-ZOOpt)

**Single-thread version:** [ZOOpt](https://github.com/eyounx/ZOOpt)

**Client part of Distributed ZOOpt**: [ZOOclient](https://github.com/eyounx/ZOOjl.jl)

## Installation

The easiest way to get ZOOsrv is to type `pip install zoosrv` in you terminal/command line.

If you want to install ZOOsrv by source code, download this project and sequentially run following commands in your terminal/command line.

```
$ python setup.py build
$ python setup.py install
```

## Release 0.1

- Implement general control server and evaluation server
