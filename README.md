# ad.fly
Implemented the cmd line interface based on the official python api example

# Environment
- OS : MacOS 10.13.6
- Language: Python 2.7.10

# Prerequisite
- Create a .py file `setting.py` within following lines
```python
SECRET_KEY = 'Your secret key'
PUBLIC_KEY = 'Your public key'
# Notice that below it needs integear type
USER_ID = 'Your user id'
```
along with the file README.md.

# Usage
```
usage: adfly_shorten.py [-h] -u URL [-t TYPE]

Randomly shorten your url via adf.ly

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     the single url you wanna shorten
  -t TYPE, --type TYPE  the ads type you wanna use, and this arg is 'banner'
                        by default,and pass 'int' to get interstitial
                        advertising
```
  
# Demo
```bash
$ python2.7 adfly_shorten.py -u 'www.google.com' -t int
The shortened url is:
http://turboagram.com/CCr8
```

# Reference
- [Official Documentation](https://adf.ly/static/other/adfly_api_v1_documentation.pdf?v=20171213)
- [Official API Client Examples](https://adf.ly/static/other/adfly_api_v1_documentation.pdf?v=20171213)
