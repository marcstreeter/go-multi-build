# go-multi-build
Builds multi-arch docker containers, just run 
```
guilder build [name] --version 1
```
Assumes you've already installed docker and have logged in

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