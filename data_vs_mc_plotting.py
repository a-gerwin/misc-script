import ROOT
from ROOT import TH1F, TFile, TEfficiency, TF1, std, TArrayD, TCanvas, gPad, gStyle, TPad, TLegend, TGaxis
from ROOT import kCircle, kPlus, kStar, kRed, kFullCircle, kFullSquare, kBlue, kGreen
import sys, array, os
import numpy as np

#ROOT.gROOT.LoadMacro("/home/agerwin/atlasstyle/AtlasStyle.C")
#ROOT.SetAtlasStyle()
ROOT.gROOT.SetBatch(True)

def create_datavsmc(hist,file_1,hist2="",file_2="",hist1_label="hist1",hist2_label="hist2",title="",xaxis="",outputname="output.png",logscale=False, do_normalize=False):
	#todo: set better dimension
	canvashandler=TCanvas("canvas",'canvas',800, 800)
	canvashandler.cd()
	# todo: set better ratio, we want around 800x600? maybe?
	pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1)
	pad1.SetBottomMargin(0.02)

	pad1.Draw()
	pad1.cd()
#	if logscale:
#		gPad.SetLogy()

	histo_data1 = file_1.Get(f"{hist}").Clone()
	if do_normalize:
		histo_data1.Scale(1/histo_data1.Integral())
	histo_data1.SetName("Data")
	if xaxis != "":
		histo_data1.GetXaxis().SetTitle(hist)
	histo_data1.SetMarkerStyle(kFullCircle)
	histo_data1.SetMarkerColor(kBlue)
	histo_data1.SetMarkerSize(1)
	histo_data1.SetLineColor(kBlue)
	histo_data1.GetXaxis().SetLabelSize(0)


#	pad1.Draw()
#	pad1.cd()
#	if "_pt_" in hist:
#		gPad.SetLogy()
	if file_2 == "":
		file_2 = file_1
	if hist2 == "":
		hist2 = hist

	histo_2 = file_2.Get(f"{hist2}").Clone()
	if do_normalize:
		histo_2.Scale(1/histo_2.Integral())
	histo_2.SetName("MC")
	histo_2.SetLineColor(kRed)
	histo_2.SetMarkerColor(kRed)
	histo_2.SetMarkerSize(1)

	#setting max and min plot range
	maxrange = max(histo_data1.GetMaximum(),histo_data1.GetMaximum())
	minrange = min(histo_data1.GetMinimum(),histo_data1.GetMinimum())
	print(maxrange," <max min> ",minrange)
	histo_data1.SetMaximum(maxrange*1.5 if maxrange > 0 else maxrange * 0.8)
	histo_data1.SetMinimum(minrange*0.8 if minrange > 0 else minrange * 1.5)

	histo_data1.Draw("EP ][")
	histo_2.Draw("SAME EP ][")

	# legend
	#gPad.BuildLegend()
	legend = TLegend(0.7, 0.8, 0.85, 0.9)
#	if plottype == "data vs mc":
#		legend.AddEntry(histo_data1, f"Data", "lp")
#		legend.AddEntry(histo_2, f"MC", "lp")
#	elif plottype == "compare year":
#		legend.AddEntry(histo_data1, f"2022", "lp")
#		legend.AddEntry(histo_2, f"2023", "lp")
#	else:
	legend.AddEntry(histo_data1, f"{hist1_label}", "lp")
	legend.AddEntry(histo_2, f"{hist2_label}", "lp")
	legend.SetTextSize(0.03)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.Draw()


	# Writing "ATLAS Internal ..." on top left
	tl = ROOT.TLatex()
	tl.SetTextFont(42)
	tl.SetTextSize(0.05)
	tl.SetLineWidth(2)
	tl.DrawLatexNDC(0.15,0.81,"#splitline{#bf{#it{ATLAS}} Internal}{#sqrt{s} = 13.6 TeV}")
	
	t2 = ROOT.TLatex()
	t2.SetTextFont(42)
	t2.SetTextSize(0.03)
	t2.SetLineWidth(2)
	t2.DrawLatexNDC(0.15,0.7,title)

	# 'statbox'
	t2.DrawLatexNDC(0.62,0.75,f"{hist1_label} mean: {round(histo_data1.GetMean(),3)} std: {round(histo_data1.GetStdDev(),3)}")
	t2.DrawLatexNDC(0.62,0.7,f"{hist2_label} mean: {round(histo_2.GetMean(),3)} std: {round(histo_2.GetStdDev(),3)}")

	gStyle.SetOptStat(0)
#
#	canvashandler.Update()

#bottom part, the ratio
	canvashandler.cd()
	pad2 = TPad("pad2", "pad2", 0, 0, 1, 0.3)
#	pad2.SetTopMargin(0)
#	pad2.SetBottomMargin(0.4)
	pad2.Draw()
	pad2.cd()
	pad2.SetTopMargin(0.01)

	numerator1 = histo_data1.Clone()
	numerator1.SetName("")
	numerator1.GetYaxis().SetTitle("ratio")# if plottype!="data vs mc" else "Data/MC")
	numerator1.GetXaxis().SetTitle(xaxis)# if plottype!="data vs mc" else "Data/MC")
	numerator1.SetMaximum(1.2)
	numerator1.SetMinimum(0.75)
	numerator1.GetYaxis().SetLabelSize(0.075)
	numerator1.GetYaxis().SetTitleSize(0.075)
	numerator1.GetYaxis().SetTitleOffset(0.5)
	numerator1.GetXaxis().SetTitleOffset(1)
	numerator1.GetXaxis().SetLabelSize(0.075)
	numerator1.GetXaxis().SetTitleSize(0.075)

	denominator = histo_2.Clone()
	denominator.SetName("")

	numerator1.Divide(denominator)
	numerator1.SetLineColor(1)
	numerator1.Draw("EP PMC ][")

	line_at_one = TF1("line","1",numerator1.GetBinLowEdge(1),numerator1.GetBinLowEdge(numerator1.GetNbinsX())+numerator1.GetBinWidth(numerator1.GetNbinsX()))
	line_at_one.SetLineStyle(2)
	line_at_one.SetLineWidth(1)
	line_at_one.Draw("SAME")

	canvashandler.Print(outputname)


if __name__ == "__main__":
###########
###### Convention:
###### file1: data/year2022, file 2: mc/year2023


	file_data = TFile.Open(sys.argv[1], "READ")
	file_mc = TFile.Open(sys.argv[2], "READ")
	
	histograms = ["Iteration1/h_leadingd0Significance","Iteration1/h_d0Significance","Iteration1/h_d0","Iteration1/IPbiases_1/h_d0_mean_vs_eta","Iteration1/IPbiases_1/h_d0_mean_vs_phi","Iteration1/IPbiases_1/h_d0_mean_vs_pt","Iteration1/IPbiases_1/h_d0_mean_vs_qpt","Iteration1/IPbiases_1/h_d0_sigma_vs_qpt"] #['leading_jet_pt_zee_selection_jetmutiplicitycut_only','subleading_jet_pt_zee_selection_jetmutiplicitycut_only','second_subleading_jet_pt_zee_selection_jetmutiplicitycut_only',
	for hist in histograms:
		normalize = True
		if "vs" in hist:
			normalize = False
		#create_datavsmc(hist,file_data,hist2=hist,file_2=file_mc,hist1_label="data24",hist2_label="mc23e",title="yes bias (reprocessed data)",xaxis="",outputname=f"reprocessed2024yesbiasplots/datavsmc_yesbias_{os.path.basename(hist)}.png",logscale=False,do_normalize=normalize)
		create_datavsmc(hist,file_data,hist2=hist,file_2=file_mc,hist1_label="data23",hist2_label="mc23d",title="yes bias",xaxis="",outputname=f"nov03_datamc2023_yesbias_{os.path.basename(hist)}.png",logscale=False,do_normalize=normalize)
		##create_datavsmc(hist,file_data,hist2=hist,file_2=file_mc,hist1_label="data24",hist2_label="mc23e",title="yes bias",xaxis="",outputname=f"datavsmc_yesbias_{os.path.basename(hist)}.png",logscale=False,do_normalize=True)
	

