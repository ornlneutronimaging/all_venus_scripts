echo "Update laminography notebook ... "
/SNS/VENUS/shared/software/setup_laminography
echo "Done!\n"

cd ~/Imaging/notebooks/laminography/

echo 'Starting Jupyter with tomoornl310 environment ... (be patient please while we set up your system!)'
#os.system("/opt/anaconda/envs/imars3d-dev/bin/jupyter notebook")
/SNS/users/j35/mambaforge/envs/tomoornl310/bin/jupyter notebook

