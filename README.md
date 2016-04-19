# connectome_construct
The extrasynaptic and physical connectome data and data integration scripts.

## Edge list validation

To ensure we're using the same edge lists, feel free to fork this repo and raise a pull request when you update your edge lists.

To check them at your end, run `python3 -m unittest test/validate_data.py`

If the tests fail, you can regenerate the diff files to see what's wrong with `python3 test/validate_data.py`.
