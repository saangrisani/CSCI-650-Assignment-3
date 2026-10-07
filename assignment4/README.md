# Assignment 4

- `tsp.py`: completed starter interface (renamed from tspSkeleton.py).
- `assignment_4_solutions.pdf`: written solutions, code snippets, six plots, and measured analysis.
- `assignment_4_solutions.tex`: standalone editable source, including vector drawings of the plots. The annealing drawings sample the trajectories; the PDF plots use full histories.
- `tspTests.py`: instructor-provided experiment script, unchanged.
- `run_experiments.py`: 434 correctness/property checks and a seeded run of the supplied script; saves plots and complete results.
- `experiment_results.json.gz`: compressed measured data, seed, and package versions.

## Reproduce

```bash
cd assignment4
python -m pip install -r requirements.txt
python run_experiments.py
```

The experiment script uses an Agg backend and saves figures instead of opening windows. To use the instructor's interactive plots, run `python tspTests.py` instead.

The report uses the step-count Busy Beaver convention from Assignment 3. No explicit AI-detection questions occur in the supplied assignment; every required part is covered. AI assistance is disclosed in the implementation and report.

The native LaTeX compiler failed before reading the source with "Unable to find standard directories for platform". The PDF was generated separately and visually verified. LaTeX compilation remains unverified.

Neither Canvas nor INGInious was submitted to.

