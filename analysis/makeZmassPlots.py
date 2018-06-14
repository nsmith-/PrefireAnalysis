#!/usr/bin/env python
import ROOT

ROOT.gStyle.SetOptDate(0)
ROOT.gStyle.SetHistLineWidth(2)

f = ROOT.TFile.Open("prefiringZ_Run2017F.root")
t = f.Get("ntuple/tree")

print t.GetEntries()

hm1 = ROOT.TH1D("bxm1", "L1IsoEG in BX -1", 20, 20, 120)
hm1.SetLineColor(ROOT.kRed)
hm1.SetMarkerColor(ROOT.kRed)
h0 = ROOT.TH1D("bx0", "L1IsoEG in BX 0", 20, 20, 120)
h0.SetLineColor(ROOT.kBlack)
h0.SetMarkerColor(ROOT.kBlack)
hp1 = ROOT.TH1D("bxp1", "L1IsoEG in BX +1", 20, 20, 120)
hp1.SetLineColor(ROOT.kBlue)
hp1.SetMarkerColor(ROOT.kBlue)

hl1m1_pt = ROOT.TH1D("bxm1_pt", "L1EG in BX -1, 60<m_{e,L1EG}<100;p_{T}^{L1} [GeV];Counts / 10 GeV", 25, 0, 250)
hl1m1_eta = ROOT.TH1D("bxm1_eta", "L1EG in BX -1, 60<m_{e,L1EG}<100;|#eta^{L1}|;Counts / 0.1", 6, 2.4, 3)

def l1egCut(l1eg, tag, iso):
    dR = ROOT.Math.VectorUtil.DeltaR(l1eg, tag)
    return l1eg.Pt() > 15 and abs(l1eg.Eta()) > 2.4 and abs(l1eg.Eta()) < 3.0 and dR > 0.2 and iso > 2.

for i in xrange(t.GetEntries()):
    t.GetEntry(i)
    for iEG in xrange(t.L1EG_p4.size()):
        l1eg = t.L1EG_p4[iEG]
        bx = t.L1EG_bx[iEG]
        if l1egCut(l1eg, t.tag_electron, t.L1EG_iso[iEG]):
            if bx == 0:
                h0.Fill((t.tag_electron+l1eg).M())
            elif bx == -1:
                hm1.Fill((t.tag_electron+l1eg).M())
                if abs((t.tag_electron+l1eg).M()-80)<20:
                    hl1m1_pt.Fill(l1eg.Pt())
                    hl1m1_eta.Fill(abs(l1eg.Eta()))
            elif bx == 1:
                hp1.Fill((t.tag_electron+l1eg).M())

c = ROOT.TCanvas()
stack = ROOT.THStack("stack", ";Electron-L1EG Mass [GeV];Counts / 5 GeV")
stack.Add(hm1, "e0")
stack.Add(h0, "e0")
stack.Add(hp1, "e0")
stack.Draw("nostack")
l = c.BuildLegend(0.1, 0.7, 0.5, 0.9)
l.SetHeader("p_{T}^{L1} > 15, 2.4 < |#eta^{L1}| < 3.0, hwIso=3")
