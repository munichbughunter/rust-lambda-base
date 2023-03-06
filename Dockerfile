FROM rust:1.67-slim

RUN rustup target add x86_64-unknown-linux-musl
RUN apt-get update
RUN apt-get install -y musl-tools \
    gcc-x86-64-linux-gnu

ENV CARGO_TARGET_X86_64_UNKNOWN_LINUX_GNU_LINKER x86_64-linux-gnu-gcc
ENV CC x86_64-linux-gnu-gcc
ENV RUSTFLAGS -C linker=x86_64-linux-gnu-gcc
