To release:
* Verify pass in CircleCI
* Update `CHANGELOG.md`
* Update version in `setup.py`
* `git push origin master`
* Create/activate virtualenv: `pip install twine`
* `python setup.py bdist_wheel --universal`
* `twine upload dist/$(ls -tr dist/ | tail -1)`
* Create Github release, named as version
