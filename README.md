# bel2scm

<p>
<a href="https://github.com/bel2scm/bel2scm/actions?query=workflow%3ATests">
    <img alt="GitHub Actions" src="https://github.com/bel2scm/bel2scm/workflows/Tests/badge.svg" />
</a>
<a href="https://pypi.org/project/bel2scm">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/bel2scm" />
</a>
<a href="https://pypi.org/project/bel2scm">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/bel2scm" />
</a>
<a href="https://github.com/bel2scm/bel2scm/blob/main/LICENSE">
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/bel2scm" />
</a>
</p>

This package is for creating Structural Causal Models (SCMs) in Pyro and evaluating various conditions with those
models.

## Installation

Install directly from GitHub with:

```bash
$ pip install git+https://github.com/bel2scm/bel2scm.git
```

Install in development mode with:

```bash
$ git clone https://github.com/bel2scm/bel2scm
$ cd bel2scm
$ pip install --editable .
```

Where `--editable` symlinks the git repository into your python's `site-packages/` directory so you don't have to
reinstall on changes.

## Contributing

- All python code goes in `src/bel2scm/`
- All Jupyter notebooks go in `notebooks/`. Code in Jupyter notebooks should be refactored into the `bel2scm` package
  such that most of the code in the notebook just imports code, does I/O, then makes visualizations.

## Discussion

The causal model (example) can be created from a list of BEL statements strings (
causal_graph.str_graph; http://biological-expression-language.github.io), a PyBEL graph (
causal_graph.bel_graph; https://pypi.org/project/pybel/), or a json file created by exporting a causal graph from Causal
Fusion (causal_graph.cf_graph; https://causalfusion.net/login). Each causal model consists of nodes connected by
directed edges. Each node then has parameters defining the distribution of that node's variables conditioned on the
values of the parent nodes. These parameters are learned from data -- each graph can learn these parameters either using
Maximum Likelihood Estimation (for point estimates) or Stochastic Variational Inference (for Bayesian estimates).
Currently, Bernoulli, Normal, Lognormal, Exponential, and Gamma output distributions are supported; the choice of
distribution is either specified during the initialization or defaults to a hard-coded mapping from BEL object types to
distributions.

Once the training process is complete, the causal model can be queried in several different fashions. The basic query is
to sample all of the nodes of the model and return a dictionary of node names and samples (example.model_sample). Using
built-in Pyro functionality, the model can then leverage this to calculate conditioned samples (
example.model_cond_sample), interventional samples using the do-calculus (example.model_do_sample,
example.model_do_cond_sample), and counterfactual samples (example.model_counterfact).

The package includes a method to calculate the Conditional Mutual Information of a target node with respect to a test
node of interest (example.cond_mut_info). This calculation relies only on the input data, not the model itself. However,
the SCM also has a built-in method to perform the G-test on a variable of interest (example.g_test) to determine if the
SCM sufficiently captures the distribution represented by the provided data. Note that performing both of these
calculations requires binning the data to produce discrete distributions.

With the various methods for sampling conditional, interventional, and counterfactual distributions from the model, the
SCM can estimate the Controlled Direct Effect (example.cd_effect), the Natural Direct Effect (example.nd_effect), and
the Natural Indirect Effect (example.ni_effect). Finally, the SCM can write itself to a json file that can then be
imported directly to Causal Fusion (example.write_to_cf).

## Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `Tests/` folder can be
run reproducibly with:

```bash
$ tox -e finish
```

Additionally, these tests are automatically re-run with each commit in a GitHub action.

## Making a Release

After installing the package in development mode and installing
`tox` with `pip install tox`, the commands for making a new release are contained within the `finish` environment
in `tox.ini`. Run the following from the shell:

```bash
$ tox -e finish
```

This script does the following:

1. Uses BumpVersion to switch the version number in the `setup.cfg` and
   `src/bel2scm/version.py` to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel
3. Uploads to PyPI using `twine`. Be sure to have a `.pypirc` file configured to avoid the need for manual input at this
   step
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion minor` after.
