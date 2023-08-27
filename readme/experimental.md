# Experimental Features
Currently multi-arch builds require experimental [buildx] features to be enabled.

## Installation Ubuntu

You must open the `~/.docker/config.json`

```bash
    vi ~/.docker/config.json

    # {
    #     "auths": {
    #         ...
    #     },
    #     "experimental": "enabled"
    # }
```
also update the `/etc/docker/daemon.json

```bash
    sudo vi /etc/docker/daemon.json
    # { "experimental": true }
```




[buildx]: https://github.com/docker/buildx#docker-ce