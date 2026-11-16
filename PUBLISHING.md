# Publishing

Extract the ZIP (keep dot-directories), run `python3 scripts/validate_repository.py` and `python3 -m unittest discover -s tests -v`. Replace the contents of your existing repository (or create a branch `v2`), then:

```bash
git add -A
git commit -m "Requirements Skills v2.0.0"
git push
```

Check license, sources and manual CLI evaluations before tagging a release. No remote has been touched by this package.
