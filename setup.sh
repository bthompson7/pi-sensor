echo "Starting setup..."
sudo apt-get update
pip3 install -r requirements.txt
echo "Done installing python3 requirements"
echo "Installing MariaDB..."
sudo apt-get install MariaDB
echo "Done"
