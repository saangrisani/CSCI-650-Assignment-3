# CSCI 650 - Test 2

The original materials are preserved byte for byte in `originals/`; their SHA-256 hashes are recorded in `originals/SHA256.json`. The original files in Downloads were not edited.

## Files

- `exam_2_completed.pdf`: original exam followed by written answers, code snippets, the greedy counterexample, and the measured GA plot.
- `exam_2_completed.tex`: original TeX content with an added listings configuration and an appended solutions input. Existing exam text is retained.
- `solutions_body.tex`: the added written answers.
- `dominatingSets.py`: implemented copy of the skeleton, with the original interfaces, setup, and comments retained. The untouched skeleton is in `originals/`.
- `dominatingSetsTests.py`: unchanged supplied test script, located beside the module it imports.
- `run_experiment.py`: reproducible population-50, 1000-generation experiment with random seed 650.
- `fitness.png`, `fitness_history.csv`, `experiment_results.json`: plot, all recorded statistics, and final solution.
- `greedy_counterexample.png`: six-vertex counterexample illustration.
- `verify.py`, `verification_results.json`: independent checks and results.

## Run

Use Python 3.12 and install the pinned dependencies:

```sh
python -m pip install -r requirements.txt
python dominatingSetsTests.py
python verify.py
python run_experiment.py
```

The skeleton's main program still supports interactive plotting with `python dominatingSets.py`. The experiment script saves the plot without opening a window.

Compile the document from this directory with a TeX distribution that includes the listed packages, for example:

```sh
tectonic exam_2_completed.tex
```

## Results and conventions

The verifier passed 33,873 comparisons against an independent implementation on every graph in NetworkX's graph atlas with at most six vertices, plus checks for invalid vertices, isolated vertices, greedy gains, GA operators, and elitism. The supplied script also ran successfully with seed 650.

The experiment returned a valid dominating set of size 39 with fitness 0.025. The optimum on this path is 34, so this run does not establish optimality. The path has 100 vertices and 99 edges, matching the supplied skeleton; “length 100” interpreted literally as number of edges would instead require 101 vertices. Statistics record the populations before reproduction, generations 0 through 999. The returned individual is from the population after the final reproduction.

Greedy ties use NetworkX insertion order, which in the supplied setup is determined by adding edges before adding the explicit node list. The counterexample and its trace use that same rule. Vertex Cover was chosen for the NP-hardness proof; the supplied materials do not identify the list of NP-complete problems discussed in class.

Files are uploaded to GitHub only. Canvas and INGInious submissions are not performed by these scripts.
