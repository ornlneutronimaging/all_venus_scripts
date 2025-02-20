import os
import h5py

# to activate python310
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate /SNS/users/j35/miniconda3/envs/python310

# nexus = "/SNS/VENUS/IPTS-33699/nexus/VENUS_3673.nxs.h5ß"
nexus = "/SNS/VENUS/IPTS-34969/nexus/VENUS_6357.nxs.h5"
assert os.path.exists(nexus)

with h5py.File(nexus, 'r') as hdf5_data:
    # run_number = hdf5_data["entry"]["entry_identifier"][:][0].decode("utf8")
    # print(f"run_number: {run_number}")
    # filename = hdf5_data["entry"]["DASlogs"]["BL10:Exp:IM:FileName"]['value'][0][0].decode("utf8")
    # print(f"{filename =}")
    # ipts_number = hdf5_data["entry"]["experiment_identifier"][:][0].decode("utf8")
    # print(f"{ipts_number}")
    # experiment_title = hdf5_data['entry']['experiment_title'][:][0].decode("utf8")
    # print(f"{experiment_title =}")
    # detector_used = hdf5_data['entry']['DASlogs']['BL10:Exp:Det']['value_strings'][0][0].decode("utf8")
    # print(f"{detector_used =}")
    # end_time = hdf5_data['entry']['end_time'][0].decode("utf8")
    # print(f"{end_time =}")
    # start_time = hdf5_data['entry']['start_time'][0].decode("utf8")
    # print(f"{start_time =}")
    # file_path = hdf5_data["entry"]["DASlogs"]["BL10:Exp:IM:ConfigTpxFilePath"]['value'][0][0].decode("utf8")
    # print(f"{file_path =}")
    # guide_pressure = hdf5_data['entry']['DASlogs']["BL10:Guide:Pres"]['value'][0]
    # print(f"{guide_pressure =}")
    # ft_pressure = hdf5_data['entry']['DASlogs']["BL10:EN:PLC:FTPressure"]['value'][0]
    # print(f"{ft_pressure =}")
    # proton_charge = hdf5_data['entry']["proton_charge"][0]
    # print(f"{proton_charge = }")
    # second_proton_charge = hdf5_data['entry']['DASlogs']['proton_charge']['value'][:]
    # print(f"{second_proton_charge =}")
    # print(f"{len(second_proton_charge) =}")
    # print(f"")
    # acq_number = hdf5_data['entry']['DASlogs']['BL10:Det:PIXELMAN:ACQ:NUM']['value'][:][-1]
    # print(f"{acq_number = }")
    # collimator = hdf5_data['entry']['DASlogs']['BL10:Mot:coll:BeamSize_RBV']['value_strings'][0][0].decode("utf8")
    # print(f"{collimator = }")
    # slits_width = hdf5_data['entry']['DASlogs']['BL10:Mot:s1:X:Gap.RBV']['value'][:][0]
    # print(f"{slits_width = }")

#    tof_data = hdf5_data['entry']['bank100_events']['event_time_zero'][:]
    #tof_data = hdf5_data['entry']['bank_unmapped_events']['total_counts'][:]
    # tof_data = hdf5_data['entry']['bank_unmapped_events']['event_time_zero'][:]

    bank_list = ['bank100_events', 'bank200_events', 'bank300_events']

    data = hdf5_data['entry']['bank100_events']
    print(f"list of members:")
    for member in data:
        print(member)

    print(f"")
    for _bank in bank_list:
        print(f"bank: {_bank}")

        _data = hdf5_data['entry'][_bank]  
        print(f"{len(_data) = }")
        print(f"{_data =}")
      
        event_id = _data['event_id']
        print(f"{len(event_id) =}")

        event_index = _data['event_index']
        print(f"{len(event_index) =}")


        print(f"")