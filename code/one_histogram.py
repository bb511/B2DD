import ROOT as rt
import os, sys, glob

import data_handling as dhand
import produce_histograms as ph

# Preamble with all analysed decays.
decay_names = [os.path.basename(path) for path in
               glob.glob(os.path.join("bcdd_2011d", "*.root"))]

if __name__ == '__main__':

    decay_nb   = int(sys.argv[1]);     run        = int(sys.argv[2])
    branch     = sys.argv[3]     ;     lim1       = float(sys.argv[4])
    lim2       = float(sys.argv[5]);
    decay_name = decay_names[decay_nb]

    directory_name = os.path.join(os.path.expanduser("~"), decay_name[:-17])
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    moca_tree = dhand.combine_trees(run, decay_name, True)
    data_tree = dhand.combine_trees(run, decay_name, False)
    moca_tree = dhand.activate_branches(moca_tree, [branch])
    data_tree = dhand.activate_branches(data_tree, [branch])

    ph.create_overlay_histogram(data_tree, moca_tree, branch, run,
                                decay_name[:-17], lim1, lim2)


