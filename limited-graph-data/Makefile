# Makefile to determine how ranks change when only top-ranked projects input their dependencies
.PHONY: all clean

# All!
all: winners_ranks_compared.csv

clean:
	rm -rf *.csv

# Default vars
R ?= 10
N ?= 100
OSRANK ?= ../osrank-rank
COMPARE ?= ../util/CompareWinnersRanks.py
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
DEPS_META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv

# remove contributors from ranked list
# used by other targets
%.projects.csv : %.csv
	grep $< -ve "@" > $@	

# run it and generate csv
all_ranks.csv: $(OSRANK) $(CONTRIBS) $(DEPS) $(DEPS_META)
	rm -rf $@
	RUST_LOG=debug $(OSRANK) -i $(R) --contribs $(CONTRIBS) --deps $(DEPS) --deps-meta $(DEPS_META) --output-path $@

# Generates dependency list for top X projects
winners_dependencies-%.csv: all_ranks.projects.csv RemoveLosersDependencies.py $(DEPS_META) $(DEPS)
	python3 RemoveLosersDependencies.py $< $* $(DEPS_META) $(DEPS) $@

# Generate ranks when we only have limited dependency information
winners_ranks-%.csv: winners_dependencies-%.csv $(OSRANK) $(CONTRIBS) $(DEPS_META)
	rm -rf $@
	RUST_LOG=debug $(OSRANK) -i $(R) --contribs $(CONTRIBS) --deps $< --deps-meta $(DEPS_META) --output-path $@

# Compare the different ranking lists
winners_ranks_compared.csv: $(COMPARE) all_ranks.projects.csv winners_ranks-1000.projects.csv winners_ranks-750.projects.csv winners_ranks-500.projects.csv winners_ranks-250.projects.csv winners_ranks-100.projects.csv
	python3 $(COMPARE) $@ 1000 all_ranks.projects.csv winners_ranks-1000.projects.csv winners_ranks-750.projects.csv winners_ranks-500.projects.csv winners_ranks-250.projects.csv winners_ranks-100.projects.csv
