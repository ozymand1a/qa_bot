echo "Run pytest checking ..."
pytest .
echo "Everything is fine with pytest :) \n"

echo "Run mypy checking ..."
mypy .
echo "Everything is fine with pytest :) \n"

echo "Run flake8 checking ..."
flake8 .
echo "Everything is fine with pytest :) \n"
