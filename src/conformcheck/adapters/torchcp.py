"""TorchCP (ml-stat-Sustech/TorchCP, LGPL-3.0; imported, never vendored), CPU only.

Methods: regression SplitPredictor with ABS and CQR scores (the fixed model is wrapped
as an identity torch module over precomputed predictions); classification
SplitPredictor with LAC, APS and RAPS (randomized False and True) and
ClassConditionalPredictor with LAC, driven through calculate_threshold /
predict_with_logits on log-probabilities. ``import torchcp`` pulls in torchsort,
torch_geometric and transformers, which are not installed here: the adapter installs
import stubs for the missing ones (docs/DESIGN.md, section 5.4).
"""

from __future__ import annotations
