from ROOT import TMVA
from ROOT import TCut,TFile,TTree,TChain
from sys  import argv
import glob,os
import data_handling as dhand

# Preamble
decay_names    = [os.path.basename(path) for path in
                  glob.glob(os.path.join("bcdd_2011d", "*.root"))]
decay_nb       = int(argv[1])
run            = argv[2]
kfold          = argv[3]

branches    = ["_TAU", "_BPVIPCHI2", "_VCHI2", "_PT", "_MIPCHI2DV", "_PIDK", "_M"]

def add_variables(data_loader, good_variables):

    for variable in good_variables:
        if variable != "Bc_M":
            data_loader.AddVariable(variable, "F")

    return data_loader


if __name__ == '__main__':
    decay_name  = decay_names[decay_nb]
    output_file = TFile("~/TMVA/TMVAoutput" + decay_name + str(run) + ".root","RECREATE")
    factory     = TMVA.Factory("TMVA_" + decay_name, output_file, "DrawProgressBar=True")
    data_loader = TMVA.DataLoader("dataloader")

    moca_tree = dhand.combine_trees(run, decay_name, True)
    data_tree = dhand.combine_trees(run, decay_name, False)
    branches_to_keep  = dhand.branch_selection(data_tree, branches, [])
    moca_tree = dhand.activate_branches(moca_tree, branches_to_keep)
    data_tree = dhand.activate_branches(data_tree, branches_to_keep)

    add_variables(data_loader, branches_to_keep)
    sgcut_test  = TCut("runNumber%5==" + kfold + "&& (Bc_M > 5200 && Bc_M < 5400)")
    sgcut_train = TCut("runNumber%5!=" + kfold + "&& (Bc_M > 5200 && Bc_M < 5400)")
    bgcut_test  = TCut("runNumber%5==" + kfold + "&& Bc_M > 5400")
    bgcut_train = TCut("runNumber%5!=" + kfold + "&& Bc_M > 5400")

    data_loader.AddTree(moca_tree, "Signal",     1.0, sgcut_test,  "test")
    data_loader.AddTree(moca_tree, "Signal",     1.0, sgcut_train, "train")
    data_loader.AddTree(data_tree, "Background", 1.0, bgcut_test,  "test")
    data_loader.AddTree(data_tree, "Background", 1.0, bgcut_train, "train")

    os.chdir("/home/odagiu/code")
    data_loader.PrepareTrainingAndTestTree(TCut(""),TCut(""),"")

    factory.BookMethod(data_loader, TMVA.Types.kBDT, "BDT_I", "MaxDepth=2:UseRandomisedTrees=True")

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    output_file.Close()
