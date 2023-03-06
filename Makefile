RUST_LAMBDA_VERSION = 0.2.0
IMAGE_NAME ?= doe0003p/rust-lambda-base:$(RUST_LAMBDA_VERSION)
TAG = $(RUST_LAMBDA_VERSION)

build:
	docker buildx build \
		--push \
		--platform linux/arm64/v8,linux/amd64 \
		--tag $(IMAGE_NAME) .
