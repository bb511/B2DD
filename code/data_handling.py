# Handles the root ntuples used in the analysis (directory structre, etc.).

import ROOT as rt
import os
import glob

# Pathing. Going to directory where all the data is.
os.chdir("/panfs/tully/B2DD")

# Preamble. Contains names of the data and mc sample folders.
prefix_data = "bcdd_"
prefix_mont = "MC_"
run1_sets   = ["2011d", "2011u", "2012d", "2012u"]
run2_sets   = ["2015d", "2015u", "2016d", "2016u", "2017d", "2017u", "2018d", "2018u"]
mon1_sets   = ["2012"]
mon2_sets   = ["2015", "2016"]

def get_run_paths(run, ntup_name, is_mc):
    """
    Gets the paths to the data files.

    @run       :: The run number (either 1 or 2).
    @ntup_name :: The name of the ntuple to be searched for.
    @is_mc     :: Bool of wether the ntup is mc or data.

    @returns   :: Array of paths to the root ntuples.
    """
    if(int(run) == 1):
        if(is_mc): return get_paths_mont(mon1_sets, ntup_name)
        else:      return get_paths_data(run1_sets, ntup_name)
    elif(int(run) == 2):
        if(is_mc): return get_paths_mont(mon2_sets, ntup_name)
        else:      return get_paths_data(run2_sets, ntup_name)
    else:
        raise ValueError('Wrong run number given!')

def get_paths_mont(ntup_sets, ntup_name):
    """
    Gets the paths of the monte carlo root ntuples.

    @ntup_sets :: The run 1 or run 2 ntuple sets in preamble.
    @ntup_name :: The name of the ntuple being searched for.

    @returns   :: Array of paths to all ntuples with the name in the dir struct.
    """
    paths = []
    for ntup_set in ntup_sets:
        mont_fold = prefix_mont + ntup_set
        ntup_name = ntup_name[:-5] + "_pScaled_PIDCorr.root"
        und_pos1 = ntup_name.find('_')
        und_pos2 = ntup_name.replace('_', 'XXX', 1).find('_') - 1
        sim_name = os.path.join(mont_fold, "*Bp2" + ntup_name[3:und_pos1] \
            + "_" + ntup_name[und_pos2:-33] + "_*")
        if "Dst" in sim_name:
            sim_name = sim_name.replace("Dst", "Dpst", 1)
            sim_name = sim_name[:19] + "DzPp_" + sim_name[19:]
        sim_folds = glob.glob(sim_name)
        for sim_fold in sim_folds:
            paths.append(os.path.join(sim_fold, ntup_name))
    return paths

def get_paths_data(ntup_sets, ntup_name):
    """
    Gets the paths of the data root ntuples.

    @ntup_sets :: The run 1 or run 2 ntuple sets in preamble.
    @ntup_name :: The name of the ntuple being searched for.

    @returns   :: Array of paths to all ntuples with the name in the dir struct.
    """
    paths = [os.path.join(prefix_data + ntup_set, ntup_name)
             for ntup_set in ntup_sets]
    return paths

def tree_merging(decay_name, ntuple_paths):
    """
    Creates a TChain of multiple root files of a certain decay.

    @decay_name   :: The name of the decay studied.
    @ntuple_paths :: Array of the paths to the ntuples of the decay.

    @returns       :: TChain of all root ntuples for a decay in a run.
    """
    merged_tree = rt.TChain("Tuple" + decay_name[:-17] + "/DecayTree")
    for path in ntuple_paths: merged_tree.Add(path)

    return merged_tree

def branch_selection(tree, branches, existing):
    """
    Selects all the branches of interest to the analysis.

    @tree     :: Root tree containing all the branches.
    @branches :: Array containing the names of the branches of interest.
    @existing :: Branches that are already histograms.

    @returns  :: Array of the branches of interest found in given tree.
    """
    branches_to_keep = []
    for branch in tree.GetListOfBranches():
        branch_name = branch.GetName()
        for good_branch in branches:
            if branch_name.endswith(good_branch) and branch_name not in existing:
                branches_to_keep.append(branch_name)
    return branches_to_keep

def combine_trees(run, decay_name, is_mc):
    """
    Combine all the trees in a run with a certain decay name.
    All branches are deactivated in the output TTree.

    @run        :: Int of the run number (1 or 2).
    @decay_name :: The name of the studied B meson decay.
    @is_mc      :: Bool of whether the data or monte carlo is processed.

    @returns    :: TChain of all the root files of a decay in a run.
    """
    paths = get_run_paths(run, decay_name, is_mc)
    mtree = tree_merging(decay_name, paths)
    mtree.SetBranchStatus("*", 0)

    return mtree

def activate_branches(mtree, branches_to_keep):
    """
    Activates the branches of interest for an analysis in a TTree.

    @mtree            :: All the root files of a decay in a run (deactivated).
    @branches_to_keep :: Array of branches of interest in that Tree.

    @returns          :: The TTree with the branches of interest active.
    """
    for keep_branch in branches_to_keep: mtree.SetBranchStatus(keep_branch, 1)
    mtree.SetBranchStatus("Bc_M", 1)
    mtree.SetBranchStatus("runNumber", 1)

    return mtree
