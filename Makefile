# Makefile for osrank-rank
# TODO dirs for osrank
.PHONY: all cheater_dependencies clean

# All!
all: enriched_cargo_ranks.projects.csv

clean:
	rm -rf *.csv
	rm -rf cheater_dependencies

# Default vars
R ?= 25
N ?= 1000

# Osrank-rank

# build osrank-rs
./release/osrank-rank:
	cargo build --release --features build-binary --bin osrank-rank --manifest-path=../osrank-rs/Cargo.toml --target-dir .

# run it and generate csv
cargo_ranks.csv: ./release/osrank-rank
	rm -rf $@
	RUST_LOG=debug ./release/osrank-rank -i $(R) --contribs ../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv --deps ../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv --deps-meta ../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv --output-path $@

# remove contributors from ranked list
%.projects.csv : %.csv
	grep $< -ve "@" > $@

# add dependency counts to ranks
enriched_%.csv : %.csv AddDependencyCounts.py
	python3 AddDependencyCounts.py $< $(N)

# generate csvs for each entry in prereq, giving dependencies as if that prereq was cheating
# produces a bunch of dependencies_except_*.csv files
cheater_dependencies: cargo_ranks.projects.csv RemoveWinnersDependencies.py
	python3 RemoveWinnersDependencies.py $< $(N)

# get ranks for modified dependency files
cheater_dependencies/dependencies_except_%.csv.ranks: cheater_dependencies/dependencies_except_%.csv ./release/osrank-rank
	rm -rf $@
	RUST_LOG=debug ./release/osrank-rank -i $(R) --contribs ../osrank-rs-ecosystems/ecosystems/cargo_contributions.csv --deps $< --deps-meta ../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv --output-path $@

CHEATERS := $(patsubst %.csv,%.csv.ranks,$(wildcard cheater_dependencies/*.csv))

cheaters_ranks: $(CHEATERS)
	@echo $(CHEATERS)