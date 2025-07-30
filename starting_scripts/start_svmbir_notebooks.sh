if [[ ! -d "/SNS/users/$USER/svmbir_orhs24" ]]; then
   echo "Folder svmbir_orhs24 does not exist, let's create it!"
   mkdir /SNS/users/$USER/svmbir_orhs24
fi

echo "Copying everything from /SNS/VENUS/shared/softare/git/svmbir_notebooks/ ~/svmbir_orhs24"

cp -rf /SNS/VENUS/shared/software/git/svmbir_notebooks/* ~/svmbir_orhs24/

echo "cd ~/svmbir_orhs24/notebooks"
cd ~/svmbir_orhs24/notebooks

echo "Launching notebook"
/SNS/users/j35/.conda/envs/hsnt/bin/jupyter notebook svmbir_reconstruction_in_tof_mode.ipynb
