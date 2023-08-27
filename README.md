# Guilder
Builds [multi-arch docker containers], just run 
```
guilder build [name] --version 1
```
Assumes you've already installed docker and have logged in

# requirements
In order to run guilder successfully you need to ensure that
- [Experimental Features are enabled]
- [QEMU is installed properly]
- [buildx builder created]

# installation

```
pip install .
```

# development

```
pip install --editable .
```

# issues
- easier calling without `build` https://github.com/pyinvoke/invoke/issues/562
- default task help broken https://github.com/pyinvoke/invoke/issues/673
- unable to determine current docker user like mentioned
- error: "requested \[arch\] and received \[different arch\]" - issues with building when the image is not tagged properly (an arm image tagged as a amd64 image), will give errors. Need to get an image that has been tagged properly.
- error: "does not match the detected host platform", make sure buildx builder created, selected (and not inactive, may need to do `docker buildx inspect --bootstrap` will create a mobyx container that must be running or your `docker buildx ls` will be reported as `inactive`

[Experimental Features are enabled]: ./readme/experimental.md
[QEMU is installed properly]: ./readme/qemu.md
[multi-arch docker containers]: https://docs.docker.com/buildx/working-with-buildx/#build-multi-platform-images
[buildx builder created]: ./readme/buildx.md
