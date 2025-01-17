from ROOT import TH1F, TFile, TEfficiency, TF1, std, TArrayD, TCanvas, gPad, kCircle, kRed, gStyle, TPad
import sys, array
import numpy as np

histograms = ['leading_jet_pt_zee_selection_jetmutiplicitycut_only','subleading_jet_pt_zee_selection_jetmutiplicitycut_only','second_subleading_jet_pt_zee_selection_jetmutiplicitycut_only',
				'leading_jet_eta_zee_selection_jetmutiplicitycut_only','subleadjet_eta_zee_selection_jetmutiplicitycut_only','second_subleadjet_eta_zee_selection_jetmutiplicitycut_only']

file_data1 = sys.argv[1]
file_data2 = sys.argv[2]
file_mc = sys.argv[3]

file_data1 = TFile.Open(file_data1, "READ")
file_data2 = TFile.Open(file_data2, "READ")
file_mc = TFile.Open(file_mc, "READ")


for hist in histograms:
	#todo: set better dimension
	canvashandler=TCanvas("canvas",'canvas',800, 1000)
	canvashandler.cd()
	# todo: set better ratio, we want around 800x600? maybe?
	pad1 = TPad("pad1", "pad1", 0, 0.6, 1, 1)
#	pad1.SetBottomMargin(0)

	pad1.Draw()
	pad1.cd()
	if "_pt_" in hist:
		gPad.SetLogy()

	histo_data1 = file_data1.Get(f"/NOSYS/{hist}")
	histo_data1.SetName("Data with insitu")
	histo_data1.GetXaxis().SetTitle(hist)

	histo_data2 = file_data2.Get(f"/NOSYS/{hist}")
	histo_data2.SetName("Data without insitu")

	histo_mc = file_mc.Get(f"/NOSYS/{hist}")
	histo_mc.SetName("MC")
	histo_mc.SetMarkerStyle(kCircle)
	histo_mc.SetLineColor(kRed)

	histo_data1.Draw("PLC PMC")
	histo_data2.Draw("SAME PLC PMC")
	histo_mc.Draw("SAME")

	gPad.BuildLegend()
	

	gStyle.SetOptStat(0)

	canvashandler.Update()

#bottom part, the ratio
	canvashandler.cd()
	pad2 = TPad("pad2", "pad2", 0, 0, 1, 0.6)
#	pad2.SetTopMargin(0)
#	pad2.SetBottomMargin(0.4)
	pad2.Draw()
	pad2.cd()

	numerator1 = histo_data1.Clone()
	numerator1.SetName("")
	numerator2 = histo_data2.Clone()
	numerator2.SetName("")

	denominator = histo_mc.Clone()
	denominator.SetName("")

	numerator1.Divide(denominator)
	numerator1.Draw("PLC PMC")

	numerator2.Divide(denominator)
	numerator2.Draw("SAME PLC PMC")


	canvashandler.Print(f"merged_{hist}.png")
