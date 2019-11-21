# Makefile to determine how ranks change when only top-ranked projects input their dependencies
.PHONY: clean

# Need to figure out how to make "cheater_dependencies" and "cheaters_gains.csv" in one command

clean:
	rm -rf *.csv
	rm -rf cheater_dependencies

# Default vars
R ?= 100
N ?= 10 # 0 means use all projects
BIN ?= java -jar
JAR ?= ../../osrank-java/out/artifacts/osrank_jar/osrank.jar
COMMON_ARGS ?= metadataFilePath=$(META) contributionsFilePath=$(CONTRIBS) resultsFilePath=$@ projectDependencyWeight=4 projectContributionWeight=1 projectMaintainerWeight=2 accountMaintainerWeight=3 accountContributionWeight=2
META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv
COMPARE ?= ../util/CompareWinnersRanks.py
ASSEMBLE ?= ../util/AssembleCheatersGains.py

# Run osrank with R given in filename
ranks.csv: $(JAR) $(META) $(DEPS) $(CONTRIBS)
	$(BIN) $(JAR) R=$(R) dependenciesFilePath=$(DEPS) $(COMMON_ARGS)

# generate csvs for the top N winners in ranks.csv, giving dependencies as if that prereq was cheating
# produces a bunch of dependencies_except_*.csv files
cheater_dependencies: ranks.csv RemoveWinnersDependencies.py $(META) $(DEPS)
	python3 RemoveWinnersDependencies.py $< $(N) $(META) $(DEPS)

# get ranks for modified dependency files
cheater_dependencies/cheater.%.ranks: cheater_dependencies/cheater.%.deps $(JAR) $(META) $(CONTRIBS)
	$(BIN) $(JAR) R=$(R) dependenciesFilePath=$^ $(COMMON_ARGS)

CHEATERS := $(patsubst %.deps,%.ranks,$(wildcard cheater_dependencies/*.deps))

cheater_ranks: $(CHEATERS)
	@echo "Generated ranks for cheaters." 

cheater_gains.csv: $(ASSEMBLE) ranks.csv $(CHEATERS)
	python3 $(ASSEMBLE) $@ ranks.csv $(CHEATERS)