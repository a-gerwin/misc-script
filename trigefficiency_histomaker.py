from ROOT import TH1F, TFile, TEfficiency, TF1, std, TArrayD
import sys, array
import numpy as np

filename = sys.argv[1]

numerator = ["leading_jet_pt_zee_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "leading_jet_pt_zee_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"]
denominator = ["leading_jet_pt_zee_selection"]

### convention: {denominator1:[list of numerators 1], deno2:[list2], etc}
plotbranches = {
				"leading_jet_pt_zee_selection":["leading_jet_pt_zee_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "leading_jet_pt_zee_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"],
				#"leading_jet_pt_0to400gev_zee_selection":["leading_jet_pt_0to400gev_zee_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "leading_jet_pt_0to400gev_zee_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"],
				}

file = TFile.Open(filename, "UPDATE")
file.cd("NOSYS")

### variable binning edges
region1 = list(range(0,400,10))
region2 = list(range(400,1050,50))

handler_binedges = [*region1,*region2]

### convert into array, list dont play nicely with cpp
binedges = array.array('d',handler_binedges)

print(binedges)
for deno in plotbranches.keys():
	deno_handler = file.Get(f"/NOSYS/{deno}")
	deno_handler = deno_handler.Rebin(len(binedges) - 1, "rebinned_deno",binedges)
	for nume in plotbranches[deno]:
		nume_handler = file.Get(f"/NOSYS/{nume}")
		nume_handler = nume_handler.Rebin(len(binedges) - 1, "rebinned_nume",binedges)
		efficiency = TEfficiency(nume_handler,deno_handler)
		efficiency.SetTitle(f"efficiency_{nume}")
		efficiency.SetName(f"efficiency_{nume}")
		erf = TF1("f1","[0]*TMath::Erf((x-[1])/[2])",0,1000)
		erf.SetParameters(0.1,150,50)
		fitresult = efficiency.Fit(erf,"S")
		print(f"fit result for {nume}/{deno}: {fitresult.Parameter(0)}*Erf((x-{fitresult.Parameter(1)})/{fitresult.Parameter(2)})")
#		efficiency.Draw()
		efficiency.Write()
		nume_handler.Write(f"test_{nume}")
#		nume_handler.Divide(deno_handler)
#		file.Write()

file.Close()

