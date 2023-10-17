all:
	rm -fr base

	# git clone git@github.com:andrewp-as-is/gist-list-base.git base
	rsync --delete -a --no-links --exclude=".*/" ~/git/webpack-config/ assets/webpack-config
	rsync --delete -a --no-links --exclude=".*/" ~/git/gist-list-base/ base

	find . -type d -name .git -mindepth 2 -exec rm -fr {} \; ;:
