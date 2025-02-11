import ROOT
from ROOT import TH1F, TFile, TEfficiency, TF1, std, TArrayD, TCanvas, gPad, gStyle, TPad, TLegend
from ROOT import kCircle, kPlus, kStar, kRed, kFullCircle, kFullSquare, kBlue, kGreen
import sys, array
import numpy as np

ROOT.gROOT.LoadMacro("/raid03/users/agerwin/atlasstyle/AtlasStyle.C")
ROOT.SetAtlasStyle()
ROOT.gROOT.SetBatch(True)

filename_data = sys.argv[1]
filename_mc = sys.argv[2]

#numerator = ["leading_jet_pt_5gev_bins__zee_jetmutiplicitycut_only_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "leading_jet_pt_5gev_bins__zee_jetmutiplicitycut_only_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"]
#denominator = ["leading_jet_pt_5gev_bins__zee_selection_jetmutiplicitycut_only"]

### convention: {denominator1:[list of numerators 1], deno2:[list2], etc}
plotbranches = {
				"leading_jet_pt_zee_selection_jetmutiplicitycut_only":["leading_jet_pt_zee_jetmutiplicitycut_only_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100","leading_jet_pt_zee_jetmutiplicitycut_only_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100"],
#				"leading_jet_pt_5gev_bin_zee_selection_jetmutiplicitycut_only":["leading_jet_pt_5gev_bin_zee_jetmutiplicitycut_only_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "leading_jet_pt_5gev_bin_zee_jetmutiplicitycut_only_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"],
				#"subleading_jet_pt_zee_selection":["subleading_jet_pt_zee_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "subleading_jet_pt_zee_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"],
				#"leading_jet_pt_0to400gev_zee_selection":["leading_jet_pt_0to400gev_zee_trigPassed_HLT_j180_dispjet50_3d2p_dispjet50_1p_L1J100", "leading_jet_pt_0to400gev_zee_trigPassed_HLT_j180_2dispjet50_3d2p_L1J100"],
				}

file_data = TFile.Open(filename_data, "READ")
file_mc = TFile.Open(filename_mc, "READ")
#file_new = TFile.Open("efficiency.root","RECREATE")

### variable binning edges
region1 = list(range(0,510,10))
#region2 = list(range(400,1100,100))

handler_binedges = [*region1]#,*region2]

### convert into array, list dont play nicely with cpp
binedges = array.array('d',handler_binedges)

print(binedges)

# deno loop
for deno in plotbranches.keys():
	# getting deno histogram for data
	deno_handler_data = file_data.Get(f"/NOSYS/{deno}")
#	deno_handler_data.Write(f"deno_data_{deno}")
	#rebinning
	deno_handler_data = deno_handler_data.Rebin(len(binedges) - 1, "rebinned_deno",binedges)
	
	#getting deno histo for MC
	deno_handler_mc = file_mc.Get(f"/NOSYS/{deno}")
#	deno_handler_mc.Write(f"deno_mc_{deno}")
	# rebinning
	deno_handler_mc = deno_handler_mc.Rebin(len(binedges) - 1, "rebinned_deno",binedges)
	
	# numerator loop
	for nume in plotbranches[deno]:
		#trigger name
		trigger_name = nume.replace("leading_jet_pt_zee_jetmutiplicitycut_only_","")
		# upped pad
		canvashandler=TCanvas("canvas",'canvas',800, 850)
		canvashandler.cd()
		# todo: set better ratio, we want around 800x600? maybe?
		pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1)
		pad1.SetBottomMargin(0.02)
	
		pad1.Draw()
		pad1.cd()

		# invisible histogram to set x y range, title, etc
		# since we cant to such with TEfficiency object
		hist_rangesetter = TH1F("hist", f"efficiency_{nume}", 100, 0, 500)
		hist_rangesetter.SetMaximum(0.6)
		hist_rangesetter.GetYaxis().SetTitle("Trigger Efficiency")
		hist_rangesetter.GetXaxis().SetLabelSize(0)
		hist_rangesetter.GetYaxis().SetLabelSize(0.035)
		hist_rangesetter.GetYaxis().SetTitleSize(0.035)
		hist_rangesetter.Draw()

		# getting nume hist for data
		nume_handler_data = file_data.Get(f"/NOSYS/{nume}")
#		nume_handler_data.Write(f"nume_data_{nume}")
		
		# rebinning
		nume_handler_data = nume_handler_data.Rebin(len(binedges) - 1, "rebinned_nume",binedges)
		
		# efficiency of data
		efficiency_data = TEfficiency(nume_handler_data,deno_handler_data)
		efficiency_data.SetTitle(f"efficiency_data_{nume}")
		efficiency_data.SetName(f"efficiency_data_{nume}")
		efficiency_data.Write(f"efficency_data_{nume}")
		
		# Erf fit function
		erf_data = TF1("f1","0.5*[0] * (TMath::Erf((x-[1])/[2]) + 1)",150,500)
		erf_data.SetParameters(2.25,500,100)
		erf_data.SetLineColor(kBlue)

		# arctan fit function
		arctan_data = TF1("tan1","([0]/TMath::Pi()) * (TMath::ATan((x - [1])/[2]) + (TMath::Pi()/2))",100,500)
		arctan_data.SetParameters(2.25,500,100)
		arctan_data.SetLineColor(kBlue)


#		line_data = TF1("l1","[0]",50,350)
#		line_data.SetParameters(1)

		#fitting the data
#		fitresult_data = efficiency_data.Fit(erf_data,"WL S R")
		fitresult_data = efficiency_data.Fit(arctan_data,"WL S R")

		# printing result 
#		print(f"\n\ndata: fit result for {nume}/{deno}: {fitresult_data.Parameter(0)}*Erf((x-{fitresult_data.Parameter(1)})/{fitresult_data.Parameter(2)})\n\n")
		print(f"\n\ndata: fit result for {nume}/{deno}: {fitresult_data.Parameter(0)}/pi * Arctan((x-{fitresult_data.Parameter(1)})/{fitresult_data.Parameter(2)}) + pi/2\n\n")

		erf_data.SetParameters(fitresult_data.Parameter(0),fitresult_data.Parameter(1),fitresult_data.Parameter(2))


		# getting nume hist for MC
		nume_handler_mc = file_mc.Get(f"/NOSYS/{nume}")
#		nume_handler_mc.Write(f"nume_mc_{nume}")
		
		#rebinning
		nume_handler_mc = nume_handler_mc.Rebin(len(binedges) - 1, "rebinned_nume",binedges)
		
		#efficiency of MC
		efficiency_mc = TEfficiency(nume_handler_mc,deno_handler_mc)
		efficiency_mc.SetTitle(f"efficiency_mc_{nume}")
		efficiency_mc.SetName(f"efficiency_mc_{nume}")
		efficiency_mc.Write(f"efficency_mc_{nume}")
		
		# Erf fit function 
		erf_mc = TF1("f2","0.5*[0] * (TMath::Erf((x-[1])/[2]) + 1)",150,500)
		erf_mc.SetParameters(2.25,500,100)
		erf_mc.SetLineColor(kRed)

		# arctan fit function
		arctan_mc = TF1("tan2","([0]/TMath::Pi()) * (TMath::ATan((x - [1])/[2]) + (TMath::Pi()/2) )",100,500)
		arctan_mc.SetParameters(2.25,500,100)
		arctan_mc.SetLineColor(kRed)

		# fitting MC
#		fitresult_mc = efficiency_mc.Fit(erf_mc,"WL S R")
		fitresult_mc = efficiency_mc.Fit(arctan_mc,"WL S R")
		
		#printing the result
		print(f"\n\nmc: fit result for {nume}/{deno}: {fitresult_mc.Parameter(0)}*Erf((x-{fitresult_mc.Parameter(1)})/{fitresult_mc.Parameter(2)})\n\n")
		erf_mc.SetParameters(fitresult_mc.Parameter(0),fitresult_mc.Parameter(1),fitresult_mc.Parameter(2))

		# styling for data
		efficiency_data.SetMarkerStyle(kFullCircle)
		efficiency_data.SetMarkerSize(1)
		efficiency_data.SetMarkerColor(kBlue)
		efficiency_data.SetLineColor(kBlue)

#		xaxis = efficiency_data.GetPassedHistogram().GetXaxis()
#		xaxis.SetRangeUser(0,1000)
		efficiency_data.Draw("EP SAME")

		# styling for MC
		efficiency_mc.SetMarkerStyle(kFullSquare)
		efficiency_mc.SetMarkerSize(1)
		efficiency_mc.SetMarkerColor(kRed)
		efficiency_mc.SetLineColor(kRed)

		efficiency_mc.Draw("EP SAME")

		# legend
#		gPad.BuildLegend()
		legend = TLegend(0.75, 0.8, 0.9, 0.9)
		legend.AddEntry(efficiency_data, f"efficiency_data", "lp")
		legend.AddEntry(efficiency_mc, f"efficiency_mc", "lp")
		legend.SetTextSize(0.03)
		legend.SetBorderSize(0)
		legend.SetFillColor(0)
		legend.SetFillStyle(0)
		legend.SetTextFont(42)


		legend.Draw()

		gStyle.SetOptStat(0)

		tl = ROOT.TLatex()
		tl.SetTextFont(42)
		tl.SetTextSize(0.05)
		tl.SetLineWidth(2)
		tl.DrawLatexNDC(0.2,0.85,"#splitline{#bf{#it{ATLAS}} Internal}{#sqrt{s} = 13.6 TeV, 25.8 fb^{-1} }")

		t2 = ROOT.TLatex()
		t2.SetTextFont(42)
		t2.SetTextSize(0.025)
		t2.SetLineWidth(2)
		t2.DrawLatexNDC(0.2,0.65,f"Fit result: #frac{{{round(fitresult_mc.Parameter(0),2)}}}{{#pi}} * (Arctan(#frac{{x-{round(fitresult_mc.Parameter(1),2)}}}{{{round(fitresult_mc.Parameter(2),2)}}}) + #frac{{#pi}}{{2}})")  

		t3 = ROOT.TLatex()
		t3.SetTextFont(42)
		t3.SetTextSize(0.025)
		t3.SetLineWidth(2)
		t3.DrawLatexNDC(0.2,0.55,trigger_name)  

		# lower pad
		canvashandler.cd()
		pad2 = TPad("pad2", "pad2", 0, 0, 1, 0.3)
		pad2.SetTopMargin(0.01)
	#	pad2.SetBottomMargin(0.4)
		pad2.Draw()
		pad2.cd()

		# styling lower pad
		efficiency_ratio = nume_handler_data.Clone("")
		efficiency_ratio.SetMarkerStyle(kFullCircle)
		n_bins = efficiency_ratio.GetNbinsX()
		efficiency_ratio.GetYaxis().SetTitle("Data/MC")
		efficiency_ratio.GetXaxis().SetTitle("Leading Jet pT (GeV)")
		efficiency_ratio.GetYaxis().SetLabelSize(0.075)
		efficiency_ratio.GetYaxis().SetTitleSize(0.075)
		efficiency_ratio.GetYaxis().SetTitleOffset(1)
		efficiency_ratio.GetXaxis().SetTitleOffset(1)
		efficiency_ratio.GetXaxis().SetLabelSize(0.075)
		efficiency_ratio.GetXaxis().SetTitleSize(0.075)

		efficiency_ratio.SetMaximum(1.3)
		efficiency_ratio.SetMinimum(0.7)


		#getting ratio and its error of efficiencies
		for i in range(1, n_bins + 1):
    		# Get the efficiency for each bin of eff1 and eff2
			eff1_val = efficiency_data.GetEfficiency(i)
			eff2_val = efficiency_mc.GetEfficiency(i)
			err1_val = 0.5 * (efficiency_data.GetEfficiencyErrorUp(i) + efficiency_data.GetEfficiencyErrorLow(i))
			err2_val = 0.5 * (efficiency_mc.GetEfficiencyErrorUp(i) + efficiency_mc.GetEfficiencyErrorLow(i))

			# Avoid division by zero
			if eff2_val != 0:
			    ratio = eff1_val / eff2_val
			    error = ratio * np.sqrt((err1_val / eff1_val)**2 + (err2_val / eff2_val)**2)
			else:
			    ratio = 0  # or set it to NaN or some other indicator if needed
			    error = 0

			# Set the ratio in the new TEfficiency object
			efficiency_ratio.SetBinContent(i, ratio)
			efficiency_ratio.SetBinError(i, error)

		#fitting ratio with horizontal line
		ratio_fit = TF1("f_ratio","[0]",200,500)
		efficiency_ratio.Fit(ratio_fit,"R")

		efficiency_ratio.Draw("EP R")

#		fit_ratio = TF1("f3",f"{fitresult_data.Parameter(0)}*TMath::Erf((x-{fitresult_data.Parameter(1)})/{fitresult_data.Parameter(2)})/{fitresult_mc.Parameter(0)}*TMath::Erf((x-{fitresult_mc.Parameter(1)})/{fitresult_mc.Parameter(2)})",180,500)#fitresult_mc.Parameter(1),1000)
#		fit_ratio.SetLineColor(kRed)
##		fit_ratio.SetLineWidth(1)
#		fit_ratio.Draw("SAME")

		line_at_one = TF1("line","1",0,500)
		line_at_one.SetLineStyle(2)
		line_at_one.SetLineWidth(1)
		line_at_one.Draw("SAME")

		#fsd

		# saving canvas
		canvashandler.Print(f"efficiency_datavmc_{nume}.png")
		canvashandler.Close()


file_data.Close()
file_mc.Close()
