install:
	python -msrc.analyzer.explorer

clean:
	find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
	find . -name "*.pyc" -print0 | xargs -0 git rm -f --ignore-unmatch
