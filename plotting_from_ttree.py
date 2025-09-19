import ROOT
import os
import sys
ROOT.gROOT.SetBatch(True)


# ----------------------------
# User settings
# ----------------------------
input_dir = "./"        # directory containing ROOT files
tree_name = "AnalysisMiniTree"    # name of the TTree
branch_name = "recojet_antikt4EMTopo_passesOR_displaced07_GNNDJbaselineallmasses_pLLPjet_NOSYS[0]:recojet_antikt4EMTopo_passesOR_displaced07_GNNDJbaselineallmasses_pLLPjet_NOSYS[1]"  # name of the branch to plot
output_dir = "./plots_correlation"  # where to save PNGs

# ----------------------------
# Make output directory
# ----------------------------
os.makedirs(output_dir, exist_ok=True)

# ----------------------------
# Loop over ROOT files
# ----------------------------
entries = 0
for filename in os.listdir(input_dir):
    if not filename.endswith(".root"):
        continue

    filepath = os.path.join(input_dir, filename)
    print(f"Processing {filepath}")

    # Open ROOT file
    f = ROOT.TFile.Open(filepath)
    if not f or f.IsZombie():
        print(f"Could not open {filepath}")
        continue

    # Get tree
    tree = f.Get(tree_name)
    if not tree:
        print(f"No TTree named {tree_name} in {filepath}")
        f.Close()
        continue

    if tree.GetEntries() == 0:
        print(f"{filepath} has empty tree")
        f.Close()
        continue

#    #th2
#    h2 = ROOT.TH2F("h2", "2 DJ correlation", 100, 0.7, 1., 100, 0.7, 1.)
    # Draw histogram
    canvas = ROOT.TCanvas("c", "c", 800, 600)
    tree.Draw(branch_name)
    canvas.SetLogy()
    print("entries for this dsid: ", tree.GetEntries())
    entries += tree.GetEntries()

    # Save PNG
    output_path = os.path.join(output_dir, filename.replace(".root", ".png"))
    canvas.SaveAs(output_path)

    # Cleanup
    f.Close()
    canvas.Close()

print("entries total: ", entries)
print("Done! All plots saved in", output_dir)
