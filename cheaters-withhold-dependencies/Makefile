# Makefile to determine how ranks change when only top-ranked projects input their dependencies
.PHONY: all clean

# All!
all: cheater_dependencies

clean:
	rm -rf *.csv
	rm -rf cheater_dependencies

# Default vars
R ?= 10
N ?= 10
OSRANK ?= ../osrank-rank
COMPARE ?= ../util/CompareWinnersRanks.py
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
DEPS_META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv

# remove contributors from ranked list
# used by other targets
%.projects : %
	grep $< -ve "@" > $@	

# run it and generate csv
ranks.csv: $(OSRANK) $(CONTRIBS) $(DEPS) $(DEPS_META)
	rm -rf $@
	RUST_LOG=debug $(OSRANK) -i $(R) --contribs $(CONTRIBS) --deps $(DEPS) --deps-meta $(DEPS_META) --output-path $@

# generate csvs for each entry in prereq, giving dependencies as if that prereq was cheating
# produces a bunch of dependencies_except_*.csv files
cheater_dependencies: ranks.csv.projects RemoveWinnersDependencies.py $(DEPS_META) $(DEPS)
	python3 RemoveWinnersDependencies.py $< $(N) $(DEPS_META) $(DEPS)

# get ranks for modified dependency files
cheater_dependencies/cheater.%.ranks: cheater_dependencies/cheater.%.deps $(OSRANK)
	rm -rf $@
	RUST_LOG=debug $(OSRANK) -i $(R) --contribs $(CONTRIBS) --deps $< --deps-meta $(DEPS_META) --output-path $@

CHEATERS := $(patsubst %.deps,%.ranks.projects,$(wildcard cheater_dependencies/*.deps))

cheaters_gains.csv: $(CHEATERS)
	@echo $(CHEATERS)
	python3 AssembleCheatersGains.py $@ $^