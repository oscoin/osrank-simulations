# Makefile to determine the right level of R, compare ranks of top 100 projects across many different R's

.PHONY: all clean

# All!
all: ranks_compared.csv

clean:
	rm -rf *.csv

# Default vars
OSRANK ?= ../osrank-rank
COMPARE ?= ../util/CompareWinnersRanks.py
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
DEPS_META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv

# remove contributors from ranked list
# used by other targets
%.projects : %.csv
	grep $< -ve "@" > $@	

# Run osrank with R given in filename
ranks_for_r_%.csv: $(OSRANK)
	rm -rf $@
	RUST_LOG=debug $(OSRANK) -i $* --contribs $(CONTRIBS) --deps $(DEPS) --deps-meta $(DEPS_META) --output-path $@

# Compare the different ranking lists
ranks_compared.csv: $(COMPARE) ranks_for_r_10.projects ranks_for_r_20.projects ranks_for_r_30.projects ranks_for_r_40.projects ranks_for_r_50.projects
	python3 $(COMPARE) $@ 100 ranks_for_r_10.projects ranks_for_r_20.projects ranks_for_r_30.projects ranks_for_r_40.projects ranks_for_r_50.projects
