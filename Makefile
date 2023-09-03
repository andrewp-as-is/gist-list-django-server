all:
	rm -fr base

	# git clone git@github.com:andrewp-as-is/gists42.com-base.git base
	rsync --delete -a --no-links --exclude=".*/" ~/git/gists42.com-base/ base

	find . -type d -name .git -mindepth 2 -exec rm -fr {} \; ;:
