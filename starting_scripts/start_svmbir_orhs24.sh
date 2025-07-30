if [[ ! -d "/SNS/users/$USER/orhs24" ]]; then
   echo "Folder orhs24 does not exist, let's create it!"
   mkdir /SNS/users/$USER/orhs24
fi

echo "Copying everything from /SNS/users/j35/orhs24_source/* ~/orhs24"

cp -rf /SNS/users/j35/orhs24_source/* ~/orhs24/

echo "cd ~/orhs24/"
cd ~/orhs24

echo "Launching notebook"
/SNS/users/j35/micromamba/envs/svmbir/bin/jupyter notebook

