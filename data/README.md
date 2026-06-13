# Data README

Do not commit private or identifiable human data.

For every dataset, document:
- source
- accession
- download date
- license
- organism
- reference genome
- annotation version
- sample inclusion/exclusion
- preprocessing pipeline

## Toy data caveat

`data/metadata/samples.csv` is a tiny toy dataset for pipeline/CI smoke tests only.
`condition` is fully confounded with `batch` (control=B1, disease=B2), so condition
and batch effects are not separable. Do NOT use it for any statistical inference or
biological conclusion. Replace it with real, documented data before running experiments.
