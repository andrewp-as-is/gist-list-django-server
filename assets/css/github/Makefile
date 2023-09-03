all:
	find . -type f -name "*.css" ! -name "hx_*.css" ! -name build.css -maxdepth 1 | xargs cat > build.css
	find . -type f -name "hx_*.css" ! -name build.css -maxdepth 1 | xargs cat >> build.css
