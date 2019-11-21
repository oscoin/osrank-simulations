# Makefile to determine how ranks change when only top-ranked projects input their dependencies
.PHONY: all clean

# All!
all: ranks_compared.csv num_intersections.csv intersection_matrix.csv

clean:
	rm -rf *.csv

# Default vars
R ?= 100
N ?= 1000 # 0 means use all projects
BIN ?= java -jar
JAR ?= ../../osrank-java/out/artifacts/osrank_jar/osrank.jar
COMMON_ARGS ?= R=$(R) metadataFilePath=$(META) dependenciesFilePath=$(DEPS) resultsFilePath=$@ projectDependencyWeight=4 accountMaintainerWeight=3 accountContributionWeight=2
META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv
COMPARE ?= ../util/CompareWinnersRanks.py
INTERSECTION_COUNT ?= ../util/CountIntersections.py
INTERSECTION_MATRIX ?= ../util/IntersectionMatrix.py

# Comparisons we want to make
RANKINGS_TO_COMPARE := ranks-contribs-1.csv ranks-contribs-4.csv ranks-contribs-8.csv

# Compare the different ranking lists
ranks_compared.csv: $(COMPARE) ranks-no-contribs.csv $(RANKINGS_TO_COMPARE)
	python3 $(COMPARE) $@ $(N) ranks-no-contribs.csv $(RANKINGS_TO_COMPARE)

# Count intersections in different ranking lists
num_intersections.csv: $(INTERSECTION_COUNT) ranks-no-contribs.csv $(RANKINGS_TO_COMPARE)
	python3 $(INTERSECTION_COUNT) $@ 1000 ranks-no-contribs.csv $(RANKINGS_TO_COMPARE)

intersection_matrix.csv: $(INTERSECTION_MATRIX) $(RANKINGS_TO_COMPARE)
	python3 $(INTERSECTION_MATRIX) $@ 1000 $(RANKINGS_TO_COMPARE)

# Generate baseline rankings
ranks-no-contribs.csv: $(JAR) $(META) $(DEPS)
	$(BIN) $(JAR) $(COMMON_ARGS)

# Generate rankings with different contributor weights
ranks-contribs-%.csv: $(JAR) $(META) $(DEPS) $(CONTRIBS)
	$(BIN) $(JAR) $(COMMON_ARGS) contributionsFilePath=$(CONTRIBS) projectContributionWeight=$*
