import sys
import anyio
import dagger
from dagger import Container, Platform
from typing import List


RUST_LAMBDA_VERSION = "0.3.0"
IMAGE_NAME = "doe0003p/rust-lambda-base:" + RUST_LAMBDA_VERSION


async def build_image():
    
    platforms = [Platform("linux/arm64"), Platform("linux/amd64")]
    platformVariants: List[Container] = []
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        async def build(plt: Platform):
            rust_lambda = (
                
                client.container(platform=plt).from_("rust:1.67-slim")
                .with_exec(["rustup", "target", "add", "x86_64-unknown-linux-musl"])
                .with_exec(["apt-get", "update"])
                .with_exec(["apt-get", "install", "-y", "gcc-x86-64-linux-gnu"])
                .with_env_variable("CARGO_TARGET_X86_64_UNKNOWN_LINUX_GNU_LINKER", "x86_64-linux-gnu-gcc")
                .with_env_variable("CC", "x86_64-linux-gnu-gcc")
                .with_env_variable("RUSTFLAGS", "-C linker=x86_64-linux-gnu-gcc")
            )
            print(f"Start building image for platform: {plt}")
            
            print(f"Add platform variant for container: {plt}")
            platformVariants.append(rust_lambda)
            
            print(f"Building image for {plt} succeeded!")

            print("Push images to registry!")
            await rust_lambda.publish(IMAGE_NAME, platform_variants=platformVariants)
            print("Images published to registry!")
            
        async with anyio.create_task_group() as tg: 
            for platform in platforms:
                tg.start_soon(build, platform)

if __name__ == "__main__":    
    anyio.run(build_image)
    
