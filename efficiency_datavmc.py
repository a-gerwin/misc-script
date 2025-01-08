import ROOT
from ROOT import TH1F, TFile, TEfficiency, TF1, std, TArrayD, TCanvas, gPad, gStyle, TPad, TLegend
from ROOT import kCircle, kPlus, kStar, kRed, kFullCircle, kFullSquare, kBlue, kGreen
import sys, array
import numpy as np

ROOT.gROOT.LoadMacro("/raid03/users/agerwin/atlasstyle/AtlasStyle.C")
ROOT.SetAtlasStyle()

filename_data = sys.argv[1]
filename_mc = sys.argv[2]

numerator = ["leading_jet_pt_zee_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "leading_jet_pt_zee_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"]
denominator = ["leading_jet_pt_zee_selection"]

### convention: {denominator1:[list of numerators 1], deno2:[list2], etc}
plotbranches = {
				"leading_jet_pt_zee_selection":["leading_jet_pt_zee_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "leading_jet_pt_zee_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"],
				"subleading_jet_pt_zee_selection":["subleading_jet_pt_zee_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "subleading_jet_pt_zee_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"],
				#"leading_jet_pt_0to400gev_zee_selection":["leading_jet_pt_0to400gev_zee_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "leading_jet_pt_0to400gev_zee_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"],
				}

file_data = TFile.Open(filename_data, "READ")
file_mc = TFile.Open(filename_mc, "READ")

### variable binning edges
region1 = list(range(0,400,10))
region2 = list(range(400,1050,50))

handler_binedges = [*region1,*region2]

### convert into array, list dont play nicely with cpp
binedges = array.array('d',handler_binedges)

print(binedges)
for deno in plotbranches.keys():
	deno_handler = file_data.Get(f"/NOSYS/{deno}")
	deno_handler = deno_handler.Rebin(len(binedges) - 1, "rebinned_deno",binedges)
	deno_handler_mc = file_mc.Get(f"/NOSYS/{deno}")
	deno_handler_mc = deno_handler_mc.Rebin(len(binedges) - 1, "rebinned_deno",binedges)
	for nume in plotbranches[deno]:
		canvashandler=TCanvas("canvas",'canvas',800, 850)
		canvashandler.cd()
		# todo: set better ratio, we want around 800x600? maybe?
		pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1)
		pad1.SetBottomMargin(0.02)
	
		pad1.Draw()
		pad1.cd()

		hist_rangesetter = TH1F("hist", f"efficiency_{nume}", 100, 0, 1000)
		hist_rangesetter.SetMaximum(0.6)
		hist_rangesetter.GetYaxis().SetTitle("Trigger Efficiency")
		hist_rangesetter.GetXaxis().SetLabelSize(0)
		hist_rangesetter.GetYaxis().SetLabelSize(0.035)
		hist_rangesetter.GetYaxis().SetTitleSize(0.035)
		hist_rangesetter.Draw()

		nume_handler = file_data.Get(f"/NOSYS/{nume}")
		nume_handler = nume_handler.Rebin(len(binedges) - 1, "rebinned_nume",binedges)
		efficiency_data = TEfficiency(nume_handler,deno_handler)
		efficiency_data.SetTitle(f"efficiency_data_{nume}")
		efficiency_data.SetName(f"efficiency_data_{nume}")
		erf_data = TF1("f1","[0]*TMath::Erf((x-[1])/[2])",0,1000)
		erf_data.SetParameters(0.25,180,2)
		erf_data.SetLineColor(kBlue)
		fitresult_data = efficiency_data.Fit(erf_data,"S")
		print(f"\n\ndata: fit result for {nume}/{deno}: {fitresult_data.Parameter(0)}*Erf((x-{fitresult_data.Parameter(1)})/{fitresult_data.Parameter(2)})\n\n")
		erf_data.SetParameters(fitresult_data.Parameter(0),fitresult_data.Parameter(1),fitresult_data.Parameter(2))

		nume_handler_mc = file_data.Get(f"/NOSYS/{nume}")
		nume_handler_mc = nume_handler_mc.Rebin(len(binedges) - 1, "rebinned_nume",binedges)
		efficiency_mc = TEfficiency(nume_handler_mc,deno_handler_mc)
		efficiency_mc.SetTitle(f"efficiency_mc_{nume}")
		efficiency_mc.SetName(f"efficiency_mc_{nume}")
		erf_mc = TF1("f2","[0]*TMath::Erf((x-[1])/[2])",0,1000)
		erf_mc.SetParameters(0.25,180,2)
		erf_mc.SetLineColor(kRed)
		fitresult_mc = efficiency_mc.Fit(erf_mc,"S")
		print(f"\n\nmc: fit result for {nume}/{deno}: {fitresult_mc.Parameter(0)}*Erf((x-{fitresult_mc.Parameter(1)})/{fitresult_mc.Parameter(2)})\n\n")
		erf_mc.SetParameters(fitresult_mc.Parameter(0),fitresult_mc.Parameter(1),fitresult_mc.Parameter(2))

#		efficiency_data.GetXaxis().SetTitle(nume)
		efficiency_data.SetMarkerStyle(kFullCircle)
		efficiency_data.SetMarkerSize(1)
		efficiency_data.SetMarkerColor(kBlue)
		efficiency_data.SetLineColor(kBlue)

		xaxis = efficiency_data.GetPassedHistogram().GetXaxis()
		xaxis.SetRangeUser(0,1000)
		efficiency_data.Draw("EP SAME")

		efficiency_mc.SetMarkerStyle(kFullSquare)
		efficiency_mc.SetMarkerSize(1)
		efficiency_mc.SetMarkerColor(kRed)
		efficiency_mc.SetLineColor(kRed)

		efficiency_mc.Draw("EP SAME")

#		gPad.BuildLegend()
		legend = TLegend(0.75, 0.75, 0.9, 0.9)
		legend.AddEntry(efficiency_data, f"efficiency_data", "lp")
		legend.AddEntry(efficiency_mc, f"efficiency_mc", "lp")
		legend.SetTextSize(0.03)
		legend.SetBorderSize(0)
		legend.SetFillColor(0)
		legend.SetFillStyle(0)
		legend.SetTextFont(42)


		legend.Draw()

		gStyle.SetOptStat(0)

		canvashandler.cd()
		pad2 = TPad("pad2", "pad2", 0, 0, 1, 0.3)
		pad2.SetTopMargin(0.01)
	#	pad2.SetBottomMargin(0.4)
		pad2.Draw()
		pad2.cd()

		efficiency_ratio = nume_handler.Clone("")
		efficiency_ratio.SetMarkerStyle(kFullCircle)
		n_bins = efficiency_ratio.GetNbinsX()
		efficiency_ratio.GetYaxis().SetTitle("Data/MC")
		efficiency_ratio.GetYaxis().SetLabelSize(0.075)
		efficiency_ratio.GetYaxis().SetTitleSize(0.075)
		efficiency_ratio.GetYaxis().SetTitleOffset(1)
		efficiency_ratio.GetXaxis().SetTitleOffset(1)
		efficiency_ratio.GetXaxis().SetLabelSize(0.075)
		efficiency_ratio.GetXaxis().SetTitleSize(0.075)


		for i in range(1, n_bins + 1):
    		# Get the efficiency for each bin of eff1 and eff2
			eff1_val = efficiency_data.GetEfficiency(i)
			eff2_val = efficiency_mc.GetEfficiency(i)

			# Avoid division by zero
			if eff2_val != 0:
			    ratio = eff1_val / eff2_val
			else:
			    ratio = 0  # or set it to NaN or some other indicator if needed

			# Set the ratio in the new TEfficiency object
			efficiency_ratio.SetBinContent(i, ratio)
			efficiency_ratio.SetBinError(i, 0)

		efficiency_ratio.Draw("EP")

		fit_ratio = TF1("f3",f"{fitresult_data.Parameter(0)}*TMath::Erf((x-{fitresult_data.Parameter(1)})/{fitresult_data.Parameter(2)})/{fitresult_mc.Parameter(0)}*TMath::Erf((x-{fitresult_mc.Parameter(1)})/{fitresult_mc.Parameter(2)})",180,1000)#fitresult_mc.Parameter(1),1000)
		fit_ratio.SetLineColor(kRed)
#		fit_ratio.SetLineWidth(1)
		fit_ratio.Draw("SAME")

		line_at_one = TF1("line","1",0,1000)
		line_at_one.SetLineStyle(2)
		line_at_one.SetLineWidth(1)
		line_at_one.Draw("SAME")

		#fsd

		canvashandler.Print(f"efficiency_datavmc_{nume}.png")
		canvashandler.Close()


file_data.Close()
file_mc.Close()

