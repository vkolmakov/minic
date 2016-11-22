watch:
	./.venv/bin/when-changed -s -r . ./.venv/bin/py.test -p no:cacheprovider

test:
	./.venv/bin/py.test -p no:cacheprovider

clean:
	find . -name '*.pyc' -delete
