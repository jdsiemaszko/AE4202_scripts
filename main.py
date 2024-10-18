from matplotlib.pyplot import plot
from src.plotterClass import DEFAULT_CASE_DIR, DEFAULT_PLOTS_DIR,DEFAULT_REFERENCE_DIR, Plotter


plotter = Plotter(DEFAULT_CASE_DIR, DEFAULT_REFERENCE_DIR, DEFAULT_PLOTS_DIR, plot_reference=False)
plotter.plot_from_keys('x', 'p'
                       , styles = {'linestyle' : 'dashed'},
                       title='p_vs_x')