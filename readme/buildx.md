# buildx
You will need a builder to do the multi-arch building
for whatevever reason the default does not work

```bash
    docker buildx create --name multiarchbuilder
    docker buildx use multiarchbuilder
    docker buildx inspect --bootstrap
```
_creates an image and starts it, ensure it is not `inactive` or do the bootstrap again_

refer to documentation for more information on [verifying proper install] etc.

[verifying proper install]: https://docs.docker.com/docker-for-mac/multi-arch/#build-and-run-multi-architecture-images
