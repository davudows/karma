---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

```
your error, e.g.

SOCKSHTTPConnectionPool(host='example.com', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.contrib.socks.SOCKSConnection object at 0x10871d410>: Failed to establish a new connection: [Errno 61] Connection refused'))
```

**To Reproduce**
Steps to reproduce the behavior:
1. Install with the command: '...'
2. Run this: '....'
3. See error

**Desktop (please complete the following information):**
 - OS: [e.g. Ubuntu 18.04]
 - Python Version [e.g. Python 3.6.8]
 -  Command output: `pip3 freeze | grep -i -f requirements.txt `. e.g.
```
docopt==0.6.2
PySocks==1.7.1
requests==2.18.4
requests-unixsocket==0.1.5
texttable==1.6.2
```
