if [[ ! -f $(pwd)/main.py ]]
then
    echo main.py file not found
    exit 1
fi

if [[ -f ~/.local/bin/ramsim ]]
then
    echo rm ~/.local/bin/ramsim
    rm ~/.local/bin/ramsim
fi

echo "python3 $(pwd)/main.py \$@"> run.sh
echo created run.sh
chmod +x run.sh
echo "$(pwd)/run.sh -> ~/.local/bin/ramsim"
ln $(pwd)/run.sh ~/.local/bin/ramsim