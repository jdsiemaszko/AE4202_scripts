
from email import header
import matplotlib.pyplot as plt
import os
import pathlib
import pandas as pd
import numpy as np

DEFAULT_PLOTTING_STYLE = {
    'marker' : 'x',
    'color' : 'k'
}


class DataRange():
    def __init__(self, data:pd.DataFrame, plotting_style:dict = DEFAULT_PLOTTING_STYLE, name:str='Data'):

        self.data = data

        self.style = plotting_style
        self.name = name
        
    def get_data(self):
        return self.data

    def __repr__(self):
        return "data range {} of size {}".format(self.name, len(self.data))
    
    @staticmethod
    def from_file(file_path, plotting_style:dict = DEFAULT_PLOTTING_STYLE, name:str=None):
        """
        Static method to create a Data instance from a file.
        SPECIFIC FOR OPENFOAM PostProcessing Output
        """
        headers = []
        data_lines = []
        
        with open(file_path, 'r') as file:
            # Read all lines in the file
            lines = file.readlines()
            
            # Iterate through the lines in reverse to find the last header line
            for line in reversed(lines):
                if line.startswith('#'):
                    headers = [header.strip() for header in line.strip().lstrip('#').split()]
                    break  # Exit loop after finding the last header line
        
            
            # Now we have the headers, let's filter out the data lines
            # We start collecting data lines after the last header
            for line in lines:
                if not line.startswith('#') and line.strip():  # Skip empty lines
                    data_lines.append(line.strip())
        
        # Create a DataFrame from the data lines, using the extracted headers
        df = pd.DataFrame([x.split() for x in data_lines], columns=headers)
        
        # Convert appropriate columns to numeric types (if needed)
        df = df.apply(pd.to_numeric)  # Convert all numeric columns

        return DataRange(df, plotting_style, name)

class ReferenceData(DataRange):
    """
    Custom class for ref data (different format to case data)
    """
    def __init__(self, path_to_file, plotting_style:dict=DEFAULT_PLOTTING_STYLE, name:str='Reference Data'):
        
        data = np.loadtxt(path_to_file, skiprows=2)
        self.style = plotting_style
        self.name = name
        
        # Assuming the first column is theta and the second column is C_p
        self.x = data[:, 0]  # First column (angles)
        self.y = data[:, 1]  # Second column (pressure coefficients)

        data_frame = pd.DataFrame({"$\theta$ (degrees)" : data[:, 0],  "$C_p$": data[:, 1]})

        super().__init__(data_frame)
    

class CaseResults():
    def __init__(self, postprocessing_directory, case_name:str = "Case"):
        self.data_ranges = {}
        self.name = case_name
        self.postprocessing_directory = postprocessing_directory
        self.__data_fill_helper(postprocessing_directory)

    def __data_fill_helper(self, dir_path):
        """
        Recursively traverse the given directory to fill the data_ranges dictionary
        with Data instances parsed from files. Uses nested dictionaries based on 
        relative path structure.
        """
        for root, _, files in os.walk(dir_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                # split file_name to get name string
                name, _ = os.path.splitext(file_name)

                # Parse the file into a Data instance
                data_instance = DataRange.from_file(file_path, name = name)
                # Get the relative path and split it into components
                relative_path = os.path.relpath(file_path, self.postprocessing_directory)
                path_components = relative_path.split(os.sep)

                # Traverse the nested dictionary to create the required structure
                current_dict = self.data_ranges
                for component in path_components[:-1]:  # Go through all but the last component
                    component, _ = os.path.splitext(component)
                    if component not in current_dict:
                        current_dict[component] = {}
                    current_dict = current_dict[component]
                
                # Set the final component as the Data instance
                current_dict[name] = data_instance
    

# class Plotter():
#     def __init__(self, case_results_paths:list, ref_paths:list):

#     def parse_reference(self):

#         self.refData = ....
    
#     def parse_data_ranges(self):


if __name__ == "__main__":
    # ensure correct cwd
    os.chdir(pathlib.Path(__file__).parent)
    reference_path = os.path.join(os.pardir, 'ref', 'Cp_hD0.2.dat')
    case_path = os.path.join(os.pardir, 'example_data')

    ref_data = ReferenceData(reference_path, 'reference Cp')
    
    case_data_stack = CaseResults(case_path, "test case")
    print(case_data_stack.data_ranges)
    print(case_data_stack.data_ranges['sample']['10']['bottom'].data['x'])

