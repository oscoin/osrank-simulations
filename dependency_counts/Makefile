# Makefile to add dependency counts to winners

.PHONY: all clean

# All!
all: ranks_with_dependencies.csv

clean:
	rm -rf *.csv

# Default vars
BIN ?= java -jar
JAR ?= ../../osrank-java/out/artifacts/osrank_jar/osrank.jar
META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv

ranks_with_dependencies.csv: AddDependencyCounts.py ranks.csv $(DEPS)
	python3 $^ $@

ranks.csv: $(JAR) $(META) $(DEPS) $(CONTRIBS)
	$(BIN) $(JAR) metadataFilePath=$(META) dependenciesFilePath=$(DEPS) contributionsFilePath=$(CONTRIBS) resultsFilePath=$@