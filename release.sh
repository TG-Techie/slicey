rm -rf dist
rm -rf build
rm -rf sized_ints.egg-info

python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository pypi dist/*