#from numpy import VisibleDeprecationWarning
from ..abstractPlotter import AbstractPlotter
from matplotlib import pyplot as plt
import pandas as pd


class PlotFromConfig(AbstractPlotter):
    '''
    Class which takes CSV-formatted data from a
    given file and returns a matplot,
    with the option to save figure
    '''

    def __init__(self, config_dir: dir, filenames: str):
        '''
        Class is initialised by a list of .csv files containing
        the datapoints, and a directory of the configurable
        parameters given in the setup file.
        '''
        self.data_files = filenames
        self.config = config_dir

    def plot(self):
        '''
        Function which takes a csv data files, reads it and separates the data
        into different variables including dose and time. Outputs plots
        comparing given variables wth the option to include the Dose function
        and change line colours. It then saves to a given file format.
        '''
        # list the variables output that wants to be plotted
        vars_to_plot = self.config["plotVars"]

        for var in vars_to_plot:
            #Initialise an empty graph, and empty data matrix
            i = 0
            fig, axes1 = plt.subplots()
            for file in self.data_files:
                # Each run outputs in a separate .csv file so
                # loop through the information in each file
                full_run_data = pd.read_csv(file, delimiter=',')
                var_names = full_run_data.columns.tolist()
                # Variable names and data position may change 
                # depending on the model used.

                full_data = pd.DataFrame(full_run_data).to_numpy()
                time = full_data[:, 0]
                index = var_names.index(var)
                data = full_data[:, index]
                if not self.config["ParameterLabels"]:
                    Label = "run" + '=' + str(i + 1)
                else:
                    Label = self.config["ParameterLabels"][i]
                if not self.config["ParameterLineColour"]:
                    axes1.plot(time, data, label=Label)
                else:
                    axes1.plot(time, data, label=Label,
                               color=self.config["ParameterLineColour"][i])

                if self.config["DoseLine"]:
                    if len(self.config["DoseLineColour"]) == 0:
                        Dosecolor = 'r'
                    elif len(self.config["DoseLineColour"]) == 1:
                        Dosecolor = self.config["DoseLineColour"][0]
                    else:
                        Dosecolor = self.config["DoseLineColour"][i]
                    # if loop plots the Dose function on a second set of axes
                    axes1.plot([], [], color=Dosecolor, linestyle='dashed',
                               label='Dose')
                    axes2 = axes1.twinx()
                    axes2.set_ylabel('dose [ng/h]')
                    axes2.plot(time, full_data[:, 1], color=Dosecolor,
                               linestyle='dashed', label='Dose')

                i += 1

            # Formatting for the full figure
            axes1.set_ylabel('drug mass [ng]')
            axes1.legend()
            plt.xlabel('time [h]')
            axes1.legend()
            fig.tight_layout()
            file_root = str(var)
            fig_file = str(file_root) + '.' + ...
            str(self.config["ImageFileFormat"])
            # Figure is saved using the plotted variable name,
            # and saved in the given format.
            fig.savefig(fig_file)
            plt.show()
            fig.clf()