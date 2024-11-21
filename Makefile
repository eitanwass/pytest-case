create-tag:
	git tag -a v`poetry version -s` -m "Release version `poetry version -s`"
	git push --tags
