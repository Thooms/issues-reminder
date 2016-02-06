
# Install

```
$ virtualenv -p `which python3` venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ cp settings.yaml.example settings.yaml
```

And fill the right sections in the `settings.yaml`. Please note that
the `(user, token)` should have access to the desired organization's
issues.

# Usage

```
$ python issues-reminder.py
```
