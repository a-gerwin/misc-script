import ROOT
import os
import glob
import sys
ROOT.gROOT.SetBatch(True)


# ----------------------------
# User settings
# ----------------------------
input_dir = "./output_oct07_full*"        # directory containing ROOT files
#input_dir = "recommendationrun3maybe.root"        # directory containing ROOT files
hists_name = ["/Iteration1/IPbiases_1/h_d0_mean_vs_eta_phi"]    # name of the TTree
#hists_name = ["/Iteration1/IPbiases_1/h_d0_mean_vs_eta_phi","/Iteration1/IPbiases_1/h_z0_mean_vs_eta_phi"]    # name of the TTree
#hists_name = ["d0/d0_theNominal","z0/z0_theNominal","sagitta/sagitta_theNominal"]    # name of the TTree
output_dir = "./data22th2"  # where to save PNGs

# ----------------------------
# Make output directory
# ----------------------------
os.makedirs(output_dir, exist_ok=True)

# ----------------------------
# Loop over ROOT files
# ----------------------------
print("listoffiles: ", glob.glob(input_dir))
for filename in glob.glob(input_dir):
    if not filename.endswith(".root"):
        continue
    #filepath = os.path.join(input_dir, filename)
    print(f"Processing {filename}")

    # Open ROOT file
    f = ROOT.TFile.Open(filename)
    if not f or f.IsZombie():
        print(f"Could not open {filepath}")
        continue

    for hist in hists_name:
        # Get tree
        h = f.Get(hist)
        if not h:
            print(f"No hist named {hist} in {filepath}")
            f.Close()
            continue
    
        if h.GetEntries() == 0:
            print(f"{hist} in {filepath} is empty")
            f.Close()
            continue
    
        # Draw histogram
        canvas = ROOT.TCanvas("c", "c", 800, 600)
        if isinstance(h,ROOT.TH2):
#            h.RebinX(2)
#            h.RebinY(2)
            ROOT.gPad.SetRightMargin(0.15)
            h.Draw("COLZ")
        else:
            #canvas.SetLogy()
            h.Draw()


        output_path = os.path.join(output_dir, filename.replace(".root", f"_{os.path.basename(hist)}.png"))
        canvas.SaveAs(output_path)
        # Save PNG
        canvas.Close()

    # Cleanup
    f.Close()


print("Done! All plots saved in", output_dir)