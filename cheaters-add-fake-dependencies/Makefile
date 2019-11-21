# Makefile to determine how ranks change when projects add fake dependencies and contributors,
# To get more visits
.PHONY: clean

clean:
	rm -rf *.csv
	rm -rf cheater_dependencies

# Default vars
R ?= 100
N ?= 100 # 0 means use all projects
BIN ?= java -jar
JAR ?= ../../osrank-java/out/artifacts/osrank_jar/osrank.jar
COMMON_ARGS ?= metadataFilePath=$(META) resultsFilePath=$@ projectDependencyWeight=4 projectContributionWeight=1 projectMaintainerWeight=2 accountMaintainerWeight=3 accountContributionWeight=2
META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv
ASSEMBLE ?= ../util/AssembleCheatersGains.py

# Run osrank with R given in filename
ranks.csv: $(JAR) $(META) $(DEPS) $(CONTRIBS)
	$(BIN) $(JAR) R=$(R) dependenciesFilePath=$(DEPS) contributionsFilePath=$(CONTRIBS) $(COMMON_ARGS)

# generate csvs for the top N winners in ranks.csv, giving dependencies as if that prereq was cheating
# produces a bunch of dependencies_except_*.csv files
cheater_dependencies: ranks.csv AddFakeDependencies.py $(DEPS) $(CONTRIBS)
	python3 AddFakeDependencies.py $< $(N) $(DEPS) $(CONTRIBS)

# get ranks for modified dependency files
cheater_dependencies/cheater.%.ranks: cheater_dependencies/cheater.%.deps cheater_dependencies/cheater.%.contribs $(JAR) $(META)
	$(BIN) $(JAR) R=$(R) dependenciesFilePath=cheater_dependencies/cheater.$*.deps contributionsFilePath=cheater_dependencies/cheater.$*.contribs $(COMMON_ARGS)

CHEATERS := $(patsubst %.deps,%.ranks,$(wildcard cheater_dependencies/*.deps))

cheater_ranks: $(CHEATERS)
	@echo "Generated ranks for cheaters." 

cheater_gains.csv: $(ASSEMBLE) ranks.csv $(CHEATERS)
	python3 $(ASSEMBLE) $@ ranks.csv $(CHEATERS)