# QEMU

Needed to do multi-architecture builds.

## installation - ubuntu

```bash
    sudo apt-get install qemu binfmt-support qemu-user-static
    # test with running
    docker run --rm -t arm64v8/ubuntu uname -m
    # output: aarch64
```