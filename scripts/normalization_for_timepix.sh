#!/bin/bash

source /opt/anaconda/etc/profile.d/conda.sh
conda activate ImagingReduction


# Initialize variables
sample=""
ob=""
output=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --sample) sample="$2"; shift ;;
        --ob) ob="$2"; shift ;;
        --output) output="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check if all required arguments are provided
if [[ -z "$sample" || -z "$ob" || -z "$output" ]]; then
    echo "Usage: $0 --sample <path_to_sample> --ob <path_to_ob> --output <path_to_output>"
    exit 1
fi

# Example operation
echo "Sample path: $sample"
echo "OB path: $ob"
echo "Output path: $output"

python /SNS/VENUS/shared/software/git/venus_scripts/scripts/normalization_for_timepix.py --sample $sample --ob $ob --output $output

# running test
# ./normalization_for_timepix.sh --sample /SNS/VENUS/IPTS-34808/shared/autoreduce/mcp/November17_Sample6_UA_H_Batteries_1_5_Angs_min_30Hz_5C 
#                                --ob /SNS/VENUS/IPTS-34808/shared/autoreduce/mcp/November17_OB_for_UA_H_Batteries_1_5_Angs_min_30Hz_5C 
#                                --output /SNS/VENUS/IPTS-34808/shared/processed_data/jean_test
