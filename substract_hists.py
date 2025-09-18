import ROOT
import sys
import os
ROOT.gROOT.SetBatch(True)


histname = "/Iteration1/IPbiases_1/h_d0_mean_vs_eta_phi"
file1_name = sys.argv[1]
file2_name = sys.argv[2]

# Open ROOT files
f1 = ROOT.TFile.Open(file1_name)
f2 = ROOT.TFile.Open(file2_name)

if not f1 or not f2:
    print("Error opening files")
    sys.exit(1)

# Get histograms (assuming same name in both files)
h1 = f1.Get(histname)
h2 = f2.Get(histname)  # adjust name if needed

if not h1 or not h2:
    print("Histogram not found in one of the files")
    sys.exit(1)

# Make sure Sumw2 is enabled for proper error propagation
h1.Sumw2()
h2.Sumw2()

# Subtract histograms
hdiff = h1.Clone("hdiff")  # clone to keep original
hdiff.Add(h2, -1)          # hdiff = h1 - h2

# Draw result
c = ROOT.TCanvas("c", "Difference", 800, 600)
ROOT.gPad.SetRightMargin(0.15)
hdiff.Draw("COLZ")
c.Update()

# Optionally save to file
c.SaveAs(f"{os.path.basename(histname)}_diff.png")

