source /opt/anaconda/etc/profile.d/conda.sh
conda activate ImagingReduction

instrument=$1
ipts=$2
folder_name=$3

python /SNS/VENUS/shared/software/code/automate_mcp_correction.py $instrument $ipts $folder_name