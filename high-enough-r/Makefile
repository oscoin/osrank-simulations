# Makefile to determine the right level of R, compare ranks of top 100 projects across many different R's

.PHONY: all clean

# All!
all: ranks_compared.csv

clean:
	rm -rf *.csv

# Default vars
R ?= 1000
N ?= 100 # 0 means use all projects
BIN ?= java -jar
JAR ?= ../../osrank-java/out/artifacts/osrank_jar/osrank.jar
META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv
COMPARE ?= ../util/CompareWinnersRanks.py

# Comparisons we want to make
RANKINGS_TO_COMPARE := ranks_for_r_5.csv ranks_for_r_10.csv ranks_for_r_25.csv ranks_for_r_50.csv ranks_for_r_100.csv ranks_for_r_150.csv ranks_for_r_200.csv ranks_for_r_1000.csv 

# Run osrank with R given in filename
ranks_for_r_%.csv: $(JAR) $(META) $(DEPS) $(CONTRIBS)
	$(BIN) $(JAR) R=$* metadataFilePath=$(META) dependenciesFilePath=$(DEPS) contributionsFilePath=$(CONTRIBS) resultsFilePath=$@ projectDependencyWeight=4 projectContributionWeight=1 projectMaintainerWeight=2 accountMaintainerWeight=3 accountContributionWeight=2

# Compare the different ranking lists
ranks_compared.csv: $(COMPARE) $(RANKINGS_TO_COMPARE)
	python3 $(COMPARE) $@ $(N) $(RANKINGS_TO_COMPARE)
