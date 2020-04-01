# Patrick Odagiu - 05.04.2020
# B-decay to D mesons ntuple analysis.

import ROOT as rt
import os, sys, glob

import data_handling as dhand

# Preamble with all analysed decays and branches of interest.
decay_names = [os.path.basename(path) for path in
               glob.glob(os.path.join("bcdd_2011d", "*.root"))]
branches    = ["_TAU", "_BPVIPCHI2", "_VCHI2", "_PT", "_M13", "_M23",
               "_MIPCHI2DV", "_PIDK", "_DM", "_M"]

def cut_and_fill(tree, histo, branch, is_mc):
    """
    Applies a cut at 5400 MeV (above the B mass) and fills the histograms
    with background data in the trees.

    @tree   :: TTree containing the B decay data.
    @histo  :: TH1D to be filled with the data.
    @branch :: The branch that is currently being analysed.
    @is_mc  :: Bool whether dealing with MC or not.

    @returns :: The filled histogram (TH1D).
    """
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        if "TAU" in branch and getattr(tree, branch) > 0.05: continue
        if getattr(tree, branch) > -999:
            if not is_mc:
                if tree.Bc_M > 5400:
                    exec("histo.Fill(tree." + branch + ")")
            else:

                exec("histo.Fill(tree." + branch + ")")

    return histo

def stack(histo_data, histo_simu, branch):
    """
    Creates a histogram stack of the data and MC histograms.

    @histo_data :: TH1D of the data.
    @histo_simu :: TH1D of the monte carlo.

    @returns    :: Stacked histogram of the two.
    """
    histo_stack = rt.THStack(branch + "_stack", branch)

    histo_stack.Add(histo_simu)
    histo_stack.Add(histo_data)

    return histo_stack

def create_legend(histo_data, histo_simu, run):
    """
    Creates legend for the overlayed mc and data histogram.

    @histo_data :: TH1D of the data.
    @histo_simu :: TH1D of the monte carlo.

    @returns    :: Legend for the overlayed plot.
    """
    legend = rt.TLegend(0.7,0.6,0.85,0.75)
    legend.AddEntry(histo_data, "Run " + str(run) + " data")
    legend.AddEntry(histo_simu, "Run " + str(run) + " MC")
    legend.SetLineWidth(0)

    return legend

def draw_histo(histo_stack, legend, branch, decay_name):
    """
    Draws the histogram and the legend on a canvas and saves it as png.

    @histo_stack :: Stack of the two histograms.
    @legend      :: The legend of the overlayed histograms.
    @branch      :: The branch name that is being analysed.
    @decay_name  :: The name of the decay that is being analysed.

    @returns     :: Nothing but saves png of the overlayed histogram.
    """
    canvas = rt.TCanvas("can", "histograms", 1400, 700)
    histo_stack.Draw("hist,nostack")
    legend.Draw("same")
    canvas.SetLogy()
    canvas.SaveAs(os.path.join(os.path.expanduser("~"), decay_name, branch + ".png"))
    canvas.Close()

def create_overlay_histogram(data_tree, moca_tree, branch, run, decay_name, lim1, lim2):
    """
    Creates an overlayed histogram of the mc and data in a run for a certain
    decay mode of the B meson and a certain branch.

    @data_tree  :: The TTree containing the data.
    @moca_tree  :: The TTree containing the mc data.
    @branch     :: The branch that is currently being analysed.
    @run        :: Int of the run number (either 1 or 2).
    @decay_name :: The name of the decay currently studied.
    @lim1       :: The inferoir limit of the histogram.
    @lim2       :: The superior limit of the histogram.

    @returns    :: Nothing but saves png of histogram.
    """
    histo_data = rt.TH1D(branch + "data" + decay_name,
                         "Histogram of " + branch + ";" + branch + "; Events",
                         100, lim1, lim2)
    histo_simu = rt.TH1D(branch + "simu" + decay_name,
                         "Histogram of " + branch + ";" + branch + "; Events",
                         100, lim1, lim2)
    histo_simu.SetStats(0); histo_data.SetStats(0)

    histo_data = cut_and_fill(data_tree, histo_data, branch, False)
    histo_simu = cut_and_fill(moca_tree, histo_simu, branch, True)
    histo_data.Scale(1./histo_data.Integral())
    histo_simu.Scale(1./histo_simu.Integral())
    histo_data.SetLineColor(1)
    histo_data.SetLineWidth(3)

    histo_simu.SetLineColor(2)
    histo_simu.SetFillColorAlpha(2, 0.3)
    histo_simu.SetLineStyle(1)

    histo_stack = stack(histo_data, histo_simu, branch)
    legend = create_legend(histo_data, histo_simu, run)
    draw_histo(histo_stack, legend, branch, decay_name)
    histo_data.Reset()
    histo_simu.Reset()

if __name__ == '__main__':
    """
    Takes the run number and creates an overlayed histogram of the mc and data
    for a certain decay using all ntuples in that run.
    """
    run   = sys.argv[1]

    for decay_name in decay_names:
        directory_name = os.path.join(os.path.expanduser("~"), decay_name[:-17])
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)

        moca_tree = dhand.combine_trees(run, decay_name, True)
        data_tree = dhand.combine_trees(run, decay_name, False)
        existing_histos   = [file.split(".")[0] for file in os.listdir(directory_name)]
        branches_to_keep  = dhand.branch_selection(data_tree, branches, existing_histos)
        print("\n\nDECAY CURRENTLY PROCESSING: " + decay_name)
        print("BRANCHES TO PROCESS: ")
        if not branches_to_keep: print("NO BRANCHES TO PROCESS!")
        else:                    print(branches_to_keep)
        moca_tree = dhand.activate_branches(moca_tree, branches_to_keep)
        data_tree = dhand.activate_branches(data_tree, branches_to_keep)
        # Overlay data and MC for each branch.
        for branch in branches_to_keep:
            create_overlay_histogram(data_tree, moca_tree, branch, run, decay_name[:-17], 0, 0)





