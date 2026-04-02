#!/data/data/com.termux/files/usr/bin/bash
echo "Setting up TermuxDocker environment..."
mkdir -p $HOME/.termuxdocker/images
python3 -m pip install --upgrade pip requests
chmod +x $HOME/TermuxDocker/termuxdocker.py
echo "TermuxDocker setup complete!"
