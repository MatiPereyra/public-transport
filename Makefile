# example: make rollback file=data/data.csv
rollback:
	@echo "Rollbacking file: $(file)"
	git checkout -- $(file)
