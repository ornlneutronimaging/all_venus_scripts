#!/bin/bash

echo $USER

bad_input() {
    # fixme
    exit 1
}

## instrument

IFS="|"
instrument=$(zenity --radiolist --list --title="Select your instrument" --column "Selected" --column="Instrument" --column="Facility" --print-column='2,3' \
'TRUE' "VENUS" "SNS" \
'FALSE' "SNAP" "SNS" \
'FALSE' "CG1D" "HFIR")

# split with white spaces
IFS="|"
read -a strarr1<<<$instrument
instrument="${strarr1[0]}"
facility="${strarr1[1]}"

## ipts

path="/$facility/$instrument"
echo "path: $path"
#list_of_files=$(ls $path)

#list_of_files=$(ls -p $path)
ls -p $path > ~/remove_me.txt

list_of_files=()
if [ -f ~/remove_me.txt ]; then
    while IFS= read -r line; do

# create full file name to check file permission
	full_file_name="$path/$line"

# check full_file_name permission
	if [ -d $full_file_name ] && [ -r $full_file_name ]; then  list_of_files+=($line)
        fi
    done < ~/remove_me.txt
else
    echo "file not found"
fi

echo "list of files: $list_of_files"

# more ~/remove_me.txt

if [ -e ~/remove_me.txt ]; then
    rm ~/remove_me.txt  # remove file
fi

ipts=$(zenity --list --title="
IPTS for $facility/$instrument" --column "IPTS" \
${list_of_files[@]}  --height=500)

if [ "$ipts" ]; then
    echo "ipts: $ipts"
else
    exit 1
fi

## conda 
conda_env=$(zenity --radiolist --list --title="Conda environment" --column "Activated" --column="Conda env." \
'FALSE' "neutron-imaging" \
'TRUE' "j35-notebook")

echo "ipts: $ipts_text"
echo "conda_env: $conda_env"

if [ $conda_env = "neutron-imaging" ]; then
    full_conda_environment="/opt/anaconda/envs/neutron-imaging"
elif [ $conda_env = "j35-notebook" ]; then
    full_conda_environment='/SNS/users/j35/miniconda3/envs/python310'
else
    bad_input
    exit 1
fi

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

echo "$notebook_command"
eval "$notebook_command"
