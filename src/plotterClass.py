from pdb import post_mortem
import matplotlib.pyplot as plt
import os
import pathlib
import pandas as pd
import numpy as np
from src.dataRange import CaseResults, DataRange, ReferenceData

# TODO: fix relative paths if they break stuff
DEFAULT_REFERENCE_DIR = os.path.join('ref', 'Cp_hD0.4.dat')
DEFAULT_CASE_DIR = os.path.join('example_data')
DEFAULT_PLOTS_DIR = os.path.join('plots')

class Plotter():
    def __init__(self, case_results_dir = None, reference_dir = None,
                  plots_dir = DEFAULT_PLOTS_DIR, case_name = None,
                    save=True, show=False, plot_reference=True,
                 plots_file_extension = 'svg'):

        self.save = save
        self.show = show
        self.plot_reference = plot_reference
        self.plots_file_extension = plots_file_extension
        plt.style.use("ggplot") # plot styling

        if case_results_dir is not None:
            self.case_results  = CaseResults(case_results_dir, case_name=case_name)
        else:
            self.case_results = None
        
        if reference_dir is not None:
            self.reference_data = ReferenceData(reference_dir, name='reference')
        else:
            self.reference_data = None

        self.plots_dir = plots_dir

    

    def plot_pressure_coefficient(self, title='pressure coefficient', plot_file_extension='svg'):
        """
        wrapper around self.plot_from_keys()
        """

        self.plot_from_keys(
            "$\theta$ (degrees)", "$C_p$", 
            title, plot_file_extension
        )


    def plot_from_keys(self, xkey, ykey, title='plot', styles=None, data_choice_key='last'):
        """
        plotting generic 2 variables
        need xkey and ykey to exist in all plotted elements (reference and case)
        """

        fig, ax = plt.subplots()

        # plot reference
        if self.plot_reference:
            ax.plot(self.reference_data.data[xkey], self.reference_data.data[ykey],
                    **self.reference_data.style, label=self.reference_data.name)

        # plot case results

        # TODO: change file match our results

        dc = self.case_results.data_ranges

        if data_choice_key == 'last':  # default - last saved data range
            key = str(max(dc['sample'], key=int))  # pick max of existing keys
        elif isinstance(data_choice_key, (str, int)): # alternative - input-specified key
            key = str(data_choice_key)
        else:
            raise ValueError('input parameter data_choice_key has an unsupported type')

        data_files = dc['sample'][key]
        # last_data_entry = last_data_files['bottom']

        if isinstance(styles, dict): # if only one style param is passed
            styles = [styles] * len(data_files) # create a list of same style

        for style, last_data_entry in zip(styles, data_files.values()):
            if style is None:
                style = last_data_entry.style
            ax.plot(last_data_entry.data[xkey], last_data_entry.data[ykey], **style,
                    label=last_data_entry.name)
        
        ax.set_xlabel(xkey)
        ax.set_ylabel(ykey)
        ax.legend()

        if self.save:
            plt.savefig(os.path.join(self.plots_dir, '{}.{}'.format(title, self.plots_file_extension)))
        if self.show:
            plt.show()
        plt.clf()

    # TODO
    def plot_time_evolution(self):
        pass

    # TODO
    def plot_yplus_histogram(self):
        pass # where tf is yplus stored?



if __name__ == "__main__":
    # ensure correct cwd
    os.chdir(pathlib.Path(__file__).parent)
    reference_path = os.path.join(os.pardir, 'ref', 'Cp_hD0.2.dat')
    case_path = os.path.join(os.pardir, 'example_data')

    ref_data = ReferenceData(reference_path, 'reference Cp')
    
    case_data_stack = CaseResults(case_path, "test case")
    print(case_data_stack.data_ranges)
    print(case_data_stack.data_ranges['sample']['10']['bottom'].data['x'])


        



        


