# Models

The first implemented model is the fixed-representation spreading-activation baseline in `src/perspective_dynamics/associative.py`. It is a deliberately minimal computational reference, not a biologically complete neural model. Its equations, parameters, numerical method, and limitations are documented in `experiments/EXP001_baseline_association/`.

Matched perspective construction and matrix blending are implemented in `src/perspective_dynamics/perspectives.py`. EXP002 uses these frames one at a time or as a static equal blend; dynamic switching remains unimplemented.
