import numpy as np
import h5py

def dic_to_h5(file_path, data_dict):   #dictionary to hdf5

    with h5py.File(file_path, 'w') as hf:
        try:
        # Create a group for each key in the dictionary
            for key, values in data_dict.items():
                # Create a group for the current key
                group = hf.create_group(key)
                # Store the values in the group as a dataset
                group.create_dataset('data', data=values)
            print(f"HDF5 file '{file_path}' created successfully.")
            hf.close()
        except Exception as e:
            print(f"HDF5 file '{file_path}' not created.")

def h5_to_dic(file_path):       #hdf5 to dictionary
    
    dic = dict()
    try:
        with h5py.File(file_path, 'r') as hf:
            # Access each group in the HDF5 file
            for key in hf.keys():
                group = hf[key]
                dataset = group['data'] # Access the dataset named 'data' within each group
                data_array = dataset[:] # Get the data as a NumPy array
                dic.update({key: list(data_array)})
                hf.close()
    
    except Exception as e:
        print(f"Error opening the file: {e}")
            
    return dic

def dict_to_structured_array(data_dict):
    # Extract keys and values from the dictionary
    keys = list(data_dict.keys())
    values = list(data_dict.values())

    # Determine the number of rows based on the length of one of the lists
    rows = len(values[0])

    # Create a dtype for the structured array
    dtype = [(key, float) for key in keys]

    # Use numpy.core.records.fromarrays to create the structured array
    structured_array = np.core.records.fromarrays(values, dtype=dtype)

    return structured_array

def open_h5(file_path):
    try:
        with h5py.File(file_path, 'r') as hf:
            # Access each group in the HDF5 file
            for key in hf.keys():
                group = hf[key]

                # Access the dataset named 'data' within each group
                dataset = group['data']

                # Get the data as a NumPy array
                data_array = dataset[:]

                # Now you can work with the data_array as a NumPy array
                print(f"Contents of the group '{key}':")
                print(data_array)
                hf.close()
    except Exception as e:
        print(f"Error opening the file: {e}")