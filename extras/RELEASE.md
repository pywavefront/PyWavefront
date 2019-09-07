

# Release Instructions

* Verify pass in [CircleCI](https://circleci.com/gh/greenmoss/PyWavefront)
  * Check against latest `master`
* Update `CHANGELOG.md` from merged PRs
* Update contributors in `README.md`
* Update version in `setup.py`
* Update version in `__init__`
* `python setup.py bdist_wheel`
* `twine upload dist/$(ls -tr dist/ | tail -1)`
* Create Github release, named as version
* Close Github issues associated with merged PR
