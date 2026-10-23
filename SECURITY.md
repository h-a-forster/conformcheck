# Security policy

## Supported versions

Security fixes go into the latest release.

## Reporting a vulnerability

Report privately through the repository's **Security** tab ("Report a vulnerability").
Do not open a public issue.

Include the conformcheck version, your OS, what goes wrong, and how to reproduce it.
Expect an acknowledgement within a week.

## Threat model

conformcheck is a local testing tool. It makes no network calls at run time and needs no
credentials.

- **It executes the libraries under test.** Adapters import and call MAPIE, crepes,
  puncc and TorchCP from your environment. Install them from sources you trust.
- **Generated repro scripts are code.** `conformcheck repro --verify` runs the scripts it
  generated in `runs/<name>/repros/` in a subprocess. Do not run repro scripts from
  untrusted run directories.
- **Import stubs.** The TorchCP adapter registers placeholder modules for `torchsort`,
  `torch_geometric` and `transformers` when they are not installed, in the importing
  process only. It never shadows an installed package.
- **Data.** Only synthetic data and datasets bundled with scikit-learn are used; nothing
  is downloaded.
