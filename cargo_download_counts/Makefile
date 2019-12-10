# Makefile to add dependency counts to winners

.PHONY: all clean

# All!
all: ranks_with_downloads.csv

clean:
	rm -rf *.csv

# Default vars
R ?= 100
BIN ?= java -jar
JAR ?= ../../osrank-java/out/artifacts/osrank_jar/osrank.jar
META ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv
DEPS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv
CONTRIBS ?= ../../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv

ranks.csv: $(JAR) $(META) $(DEPS) $(CONTRIBS)
	$(BIN) $(JAR) R=$(R) metadataFilePath=$(META) dependenciesFilePath=$(DEPS) contributionsFilePath=$(CONTRIBS) resultsFilePath=$@

top_cargo_downloads.csv: GetDownloadCounts.py
	python3 $^ 2000 $@

ranks_with_downloads.csv: AddDownloadCounts.py ranks.csv top_cargo_downloads.csv
	python3 $^ $@

