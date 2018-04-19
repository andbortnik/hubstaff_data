Hubstaff timelog importer
=========================

How to install
----------

```bash
$ git clone https://github.com/andbortnik/hubstaff_data.git
$ cd hubstaff_data
$ pip install .
```

How to use
----------
1. Set authentication configuration in `hubstaff_data.ini`:
```ini
[hubstaff]
app_token=
email=
password=
```
2. Run
```bash
$ hubstaff_data.py --config hubstaff_data.ini --date 2017-01-01
```
3. File is saved locally
