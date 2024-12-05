from ROOT import TH1F, TFile, TEfficiency, TF1, std, TArrayD, TCanvas, gPad, kCircle, kRed, gStyle
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
	histo_data1 = file_data1.Get(f"/NOSYS/{hist}")
	histo_data1.SetName("Data with insitu")
	histo_data1.GetXaxis().SetTitle(hist)

	histo_data2 = file_data2.Get(f"/NOSYS/{hist}")
	histo_data2.SetName("Data without insitu")

	histo_mc = file_mc.Get(f"/NOSYS/{hist}")
	histo_mc.SetName("MC")
	histo_mc.SetMarkerStyle(kCircle)
	histo_mc.SetLineColor(kRed)

	canvashandler=TCanvas("canvas")
	canvashandler.cd()



	histo_data1.Draw("PLC PMC")
	histo_data2.Draw("SAME PLC PMC")
	histo_mc.Draw("SAME")

	gPad.BuildLegend()

	if "_pt_" in hist:
		canvashandler.SetLogy()
	

	gStyle.SetOptStat(0)

	canvashandler.SetTitle(hist)
	canvashandler.Update()

	canvashandler.Print(f"merged_{hist}.png")