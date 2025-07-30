#!/bin/bash

# this script will jump to the IPTS specfied of the instrument speciefied (default VENUS)
# using the conda environment number from a given list (default neutron-imaging)

ipts=""   
instrument="VENUS"
conda_environment_index=1
facility="SNS"

# function to display usage
usage() {
    echo "usage:"
    echo "$0 -i <ipts_number> [-I VENUS|MARS|SNAP] [-c 1|2]"
    echo "$0 -h        to display this help"
    echo ""
    echo "list of instrument: "
    echo "  VENUS   (default)"
    echo "  MARS" 
    echo "  SNAP"
    echo ""
    echo "list of conda env:"
    echo "   1 (neutron-imaging)    (default)"
    echo "   2 (j35-notebook)"
    echo ""
    exit 1
}

# parse command line options
while getopts "i:I:c:h" opt; do
    case "$opt" in
        i)
            ipts="IPTS-$OPTARG"
            ;;
        I)
            instrument="$OPTARG"
            ;;
        c)
            conda_environment_index="$OPTARG"
            ;;
        h)
            usage
            ;;
        *)
            usage
            ;;
    esac
done

if [ $# -lt 1 ]; then
    usage
fi

# check if mandatory arguments are provided
if [ -z "$ipts" ]; then
    usage
    exit 1
fi

# rename instrument if MARS (to match DAS) and change facility name from default SNS
if [ $instrument = "MARS" ]; then
    instrument="CG1D"
    facility="HFIR" 
fi

# check argument
echo "IPTS folder: $ipts"
echo "Instrument: $instrument"
echo "Facility: $facility"
echo "Conda environment index: $conda_environment_index"

# conda environment
if [ $conda_environment_index = 1 ]; then
    full_conda_environment="/opt/anaconda/envs/neutron-imaging"
elif [ $conda_environment_index eq 2 ]; then
    full_conda_environment='SNS/users/j35/miniconda3/envs/python310'
else
    usage
    exit 1
fi

# create notebook folder path
notebook_folder_path="/$facility/$instrument/$ipts/shared/notebooks"
if [ -d "$notebook_folder_path" ]; then
    folder_exists=true
else
    folder_exists=false
fi

echo ""
echo "Notebook folder path: $notebook_folder_path"
echo " - folder exists? $folder_exists"

if ! $folder_exists; then
    echo "Creating folder $notebook_folder_path"
    mkdir -p $notebook_folder_path
fi

echo "Launching the notebooks found in $notebook_folder_path using $full_conda_environment"
cd "$notebook_folder_path"
notebook_command="$full_conda_environment/bin/jupyter notebook"
#notebook_command="$full_conda_environment/bin/jupyter notebook --no-browser --port=9000"

echo "$notebook_command"
eval "$notebook_command"
