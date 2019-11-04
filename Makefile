# Makefile to determine the right level of R
.PHONY: all clean

# All!
all: osrank-rank

clean:
	rm -rf osrank-rank

# Default vars
BIN ?= osrank-rank
MANIFEST_PATH ?= ../../osrank-rs/Cargo.toml

# build osrank-rs
# TODO want this to end up in current directory, not release directory
osrank-rank:
	cargo build --release --features build-binary --bin $(BIN) --manifest-path=$(MANIFEST_PATH) --target-dir .