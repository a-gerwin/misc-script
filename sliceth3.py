import ROOT
import os
import sys
ROOT.gROOT.SetBatch(True)

# ----------------------------
# User settings
# ----------------------------
th3names = ["mistag_rate_disp_track_count_vs_jet_pt_vs_jets_DL1_btag_score_09DJ_photonCR",
            "mistag_rate_disp_track_count_vs_eta_vs_DL1_09DJ_photonCR",
            "mistag_rate_track_count_vs_jet_pt_vs_jets_DL1_btag_score_09DJ_photonCR",
            "mistag_rate_track_count_vs_eta_vs_DL1_09DJ_photonCR"]


filename = sys.argv[1]

# Open ROOT file
f = ROOT.TFile.Open(filename,"READ")
if not f or f.IsZombie():
    raise ExceptionType("invalid/inexist root file")

for th3name in th3names:
    th3 = f.Get(th3name).Clone()
    
    # Make output directory
    os.makedirs(f"slicesof_{th3name}", exist_ok=True)

    n_zaxis = th3.GetNbinsZ()
    for i in range(1,n_zaxis+1):
        th3.GetZaxis().SetRange(i,i)
        project = th3.Project3D("XY")

        #canvas, as usual
        canvas = ROOT.TCanvas("c", "c", 800, 600)

        project.Draw("COLZ")
        canvas.SaveAs(os.path.join(f"slicesof_{th3name}",f"{i}.png"))

        canvas.Close()
f.Close()



