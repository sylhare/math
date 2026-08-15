# Working attempts (kept on purpose)

Exploration behind `../perron_tree.py`. Preserved so we don't lose the dead ends and what each
taught us. Run any with `uv run --with matplotlib --with shapely python <file>`.

- **`attempt1_topdown_subtree_shift.py`** - top-down: split by cevian, translate the whole right
  *subtree* by a fraction of the current half-base. Area plateaus at ~0.50 of the triangle; the
  needles converge at the base rather than forming a canopy. Verdict: not the true Perron shift
  (deep sprouts barely overlap).
- **`attempt2_bottomup_asymmetric.py`** - bottom-up pairwise merge, sliding the right shape left only.
  Correct canopy-at-top shape appears, area ~0.20 (47%). Includes a Monte-Carlo direction-coverage
  test that proved unreliable (chord too long) - kept as a caution: verify coverage analytically
  (fans are preserved by translation), not by random chords.
- **`attempt3_bottomup_symmetric.py`** - symmetric merge (push both halves to the pair centre) so the
  tree stays centred and the 3 rotated copies tile symmetrically. This is the basis for
  `../perron_tree.py`. Confirms the area **plateaus** at ~0.20 for a fixed-fraction schedule (does NOT
  reach 0), which is why `../kakeya.md` (sec 2f) flags that the true area->0 needs the Schoenberg/
  Keich schedule and is only ~1/log N slow.

Key finding across all three: **60 deg is not a limitation** (3 rotations cover 180 deg), rendering is
never the blocker; the only subtlety is that a fixed-fraction cut-and-shift bottoms out at ~47% area,
so a truthful "area -> 0" figure needs the correct shift schedule (or, per user guidance, we show the
minimum visible approximation with the real area readout).
