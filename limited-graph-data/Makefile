# Makefile to determine how ranks change when only top-ranked projects input their dependencies
.PHONY: all clean

# All!
all: ranks_compared.csv intersection_matrix.csv

clean:
	rm -rf *.csv

# Default vars
R ?= 100
N ?= 100 # 0 means use all projects
BIN ?= java -jar
JAR ?= ../../osrank-java/out/artifacts/osrank_jar/osrank.jar
COMMON_ARGS ?= metadataFilePath=$(META) contributionsFilePath=$(CONTRIBS) resultsFilePath=$@ projectDependencyWeight=4 projectContributionWeight=1 projectMaintainerWeight=2 accountMaintainerWeight=3 accountContributionWeight=2
META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv
COMPARE ?= ../util/CompareWinnersRanks.py
INTERSECTION ?= ../util/IntersectionMatrix.py

# Comparisons we want to make
RANKINGS_TO_COMPARE := ranks.csv winners_ranks-1000.csv winners_ranks-500.csv winners_ranks-250.csv winners_ranks-100.csv

# Run osrank with R given in filename
ranks.csv: $(JAR) $(META) $(DEPS) $(CONTRIBS)
	$(BIN) $(JAR) R=$(R) dependenciesFilePath=$(DEPS) $(COMMON_ARGS)

# Generates dependency list for top X projects
winners_dependencies-%.csv: ranks.csv RemoveLosersDependencies.py $(META) $(DEPS)
	python3 RemoveLosersDependencies.py $< $* $(META) $(DEPS) $@

# Generate ranks when we only have limited dependency information
winners_ranks-%.csv: winners_dependencies-%.csv $(JAR) $(META) $(CONTRIBS)
	$(BIN) $(JAR) R=$(R) dependenciesFilePath=$< $(COMMON_ARGS)

# Compare the different ranking lists
ranks_compared.csv: $(COMPARE) $(RANKINGS_TO_COMPARE)
	python3 $(COMPARE) $@ $(N) $(RANKINGS_TO_COMPARE)

intersection_matrix.csv: $(INTERSECTION) $(RANKINGS_TO_COMPARE)
	python3 $(INTERSECTION) $@ $(N) $(RANKINGS_TO_COMPARE)
