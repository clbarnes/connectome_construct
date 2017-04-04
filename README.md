# connectome_construct
The extrasynaptic and physical connectome data and data integration scripts.

## Re-use

Much of this repo is self-explanatory, but there may be a number of hardcoded file paths.
It also depends on some code from `connectome_utils` here http://github.com/clbarnes/connectome_utils
(which may break trying to set up a conda environment directly from the `environment.yml`)

## Edge list validation

To ensure we're using the same edge lists, feel free to fork this repo and raise a pull request when you update your edge lists.

To check them at your end, run `python3 -m unittest test/validate_data.py`

If the tests fail, you can regenerate the diff files to see what's wrong with `python3 test/validate_data.py`.
