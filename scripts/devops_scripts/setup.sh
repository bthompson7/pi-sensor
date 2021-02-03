echo "Updating..."
sudo apt-get update
echo "Installing python requirements"
pip3 install -r requirements.txt
echo "Done installing python requirements"
echo "Installing MariaDB..."
sudo apt install mariadb-server
echo "Done"
