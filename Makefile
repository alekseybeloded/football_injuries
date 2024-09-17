.PHONY: style tests check

style:
	ruff check sportinj

tests:
	pytest

check:
	make -j3 style tests
