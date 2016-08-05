## Parallel Stable Kmeans
This project is a parallel implementation of the stable kmeans presented by Benhur et al [here](http://psb.stanford.edu/psb-online/proceedings/psb02/benhur.pdf).

This project was done in Python and used Python's multiprocessing module comparing the serial, multithreaded and multiprocessed runtimes. The effect of Python's GIL along the project's outcome is discussed in the [report](https://github.com/plumSemPy/parallel_kmeans/blob/master/report/parallel-kmeans.pdf).

The [code](https://github.com/plumSemPy/parallel_kmeans/blob/master/code/stable_kmeans.py) is showcased [here](https://github.com/plumSemPy/parallel_kmeans/blob/master/code/Plots_better.ipynb). 

Since the plots were in [bokeh](http://bokeh.pydata.org/en/latest/), they have problem rendering in Github. They are shown as statis images [here](https://github.com/plumSemPy/parallel_kmeans/tree/master/Figures).
