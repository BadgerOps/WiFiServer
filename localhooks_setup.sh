#!/bin/bash

# link pre-commit hooks
ln -s $PWD/.localhooks/pre-commit $PWD/.git/hooks/pre-commit
ln -s $PWD/.localhooks/post-commit $PWD/.git/hooks/post-commit


echo "DONE"
