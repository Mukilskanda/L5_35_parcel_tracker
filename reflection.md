# Reflection

*(The handout PDF did not include the four questions, so these answer the usual Lab 5 reflection prompts. Adjust headings if your instructor's wording differs.)*

**1. Which issues were easiest and which hardest to fix?**
Style issues (Flake8 spacing, snake_case names, docstrings) were easiest because they are mechanical. The hardest was `shell=True` in `ping_hub`: it needed input validation (`ipaddress`) plus switching to an argument list, and I had to be sure the behaviour for valid addresses stayed the same.

**2. Did the tools report any false positives or anything you disagreed with?**
Bandit's B404 (importing `subprocess`) is only informational; the import is needed, so I kept it with a justified `# nosec`. Pylint's docstring warnings are low value on tiny helpers but still cheap to satisfy.

**3. How would you integrate static analysis into a development workflow?**
Run flake8/pylint/bandit as a pre-commit hook and again in CI on every pull request, failing the build on Bandit High/Medium findings or a Pylint score below a threshold (e.g. 9.5). That catches problems before review rather than after release.

**4. What is the contribution of static analysis to code quality, and what are its limits?**
It found real bugs (the shared mutable default list), real vulnerabilities (command injection, insecure temp file, predictable OTP) and consistency problems in seconds, without running the code. It cannot check business logic (e.g. whether the shipping tariff is right) or runtime behaviour, so it complements tests and code review rather than replacing them.
