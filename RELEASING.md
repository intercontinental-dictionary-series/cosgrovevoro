# Releasing the dataset

```shell
git clone https://github.com/intercontinental-dictionary-series/cosgrovevoro
cd cosgrovevoro
pip install -e .[test]
```

```shell
cldfbench lexibank.makecldf lexibank_cosgrovevoro.py --glottolog-version v5.3 --concepticon-version v3.4.0 --clts-version v2.3.0
pytest
```

```shell
cldfbench cldfreadme lexibank_cosgrovevoro.py
```

