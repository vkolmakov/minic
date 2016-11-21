watch:
	./.venv/bin/when-changed -s	. ./.venv/bin/py.test

test:
	./.venv/bin/py.test

clean:
	find . -name '*.pyc' -delete
