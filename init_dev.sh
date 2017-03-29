#!/bin/bash
# exit immediately if a command exits with a nonzero exit status.
set -e
# treat unset variables as an error when substituting.
set -u

pytest -x
