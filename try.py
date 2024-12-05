import ROOT

# Create a histogram
h = ROOT.TH1F("h", "Test histogram", 100, -5, 5)
h.FillRandom("gaus", 10000)

# Define new bin edges
xbins = [0, 1, 2, 3, 5, 10]

# Rebin the histogram
h_rebinned = h.Rebin(len(xbins) - 1, "h_rebinned", xbins)

# Draw the histograms
c = ROOT.TCanvas("c", "Canvas", 800, 600)
h.Draw()
h_rebinned.SetLineColor(ROOT.kRed)
h_rebinned.Draw("same")
c.Update()