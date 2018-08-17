To release:
* Verify pass in [CircleCI](https://circleci.com/gh/greenmoss/PyWavefront)
    * Check against latest `master`
* Update `CHANGELOG.md` from merged PRs
* Update contributors in `README.md`
* Update version in `setup.py`
* `git push origin master`
* Create/activate virtualenv, and `pip install twine`
    * **MUST** be Python 3.7 or later!
* `python setup.py bdist_wheel`
* `twine upload dist/$(ls -tr dist/ | tail -1)`
* Create Github release, named as version
