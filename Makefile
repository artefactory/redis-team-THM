MAKEFLAGS += --no-print-directory

# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help:
# help: Redis arXiv Search App Makefile help
# help:

SHELL:=/bin/bash
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

# help: help                      - display this makefile's help information
.PHONY: help
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'

.PHONY: env
env:
	@conda create -n arXiv python=3.9 -y
	$(CONDA_ACTIVATE) arXiv
	@cd backend/ && pip install -r requirements.txt

publish_blog:
	pelican blog/content -o blog/output -s blog/pelicanconf.py
	# ghp-import blog/output -b gh-pages
	# git push origin gh-pages

generate_index:
	python3 scripts/generate_index.py

load_index:
	python3 scripts/load_data.py

download_data:
	open https://www.kaggle.com/datasets/Cornell-University/arxiv