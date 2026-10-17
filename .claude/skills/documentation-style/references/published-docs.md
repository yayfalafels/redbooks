# Published docs

Rules for pages built into a published docs site, on top of the rules in `SKILL.md`.

### publish docs through a strict build

Build the site in strict mode, so every broken link and anchor fails the build. Published pages carry no release numbers, milestone ids or tracker references, since a published page describes the product as it is. List the hosting prerequisites, such as a workflow that runs only from the default branch and an access token with workflow permission, in the tracker as user actions.

**why**: relative links one level too shallow were already broken on the repository host, anchors written in the repository host's style were slugged differently by the docs builder, the dev server mounted pages under the site path, and a deploy failed on a token without the workflow permission. A lenient build published every one of them.

Example:

```yaml
# mkdocs.yml
strict: true
validation:
  links:
    anchors: warn          # strict mode turns the warning into a failure
```

### keep personal data off published pages

Published pages and their examples show no real account names, account numbers or personal details. Examples use hypothetical names at real institutions, such as `Checking at a national bank`. The docs build includes no data file, seed file or log.

**why**: a docs site is public, and anything built into it is cached and indexed even after it is removed.

Example: a page that explains a card payment names a hypothetical `Travel rewards card` and a `Checking` account, never the account the author really holds.
