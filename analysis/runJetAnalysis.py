#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os

def mkdirp(d):
    if not os.path.exists(d):
        os.makedirs(d)


ROOT.gStyle.SetOptDate(0)
ROOT.gStyle.SetHistLineWidth(2)
ROOT.gStyle.SetPalette(ROOT.kBird)
ROOT.gStyle.SetNumberContours(100)
ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetCanvasDefW(int(600*(1.1)))
ROOT.gStyle.SetPaintTextFormat(".2f")

# era = "JetHT_2016H"
era = sys.argv[1]
hdr = era.replace("_", " ")
outDir = "JetAnalysis/%s" % era

f = ROOT.TFile.Open("prefiringJet_%s.root" % era)
if not f:
    exit(0)
t = f.Get("ntuple/tree")
mkdirp(outDir)

print t.GetEntries()

ROOT.gROOT.ProcessLineSync(".L JetAnalysis.C+")

sel = ROOT.JetAnalysis()
inputs = ROOT.TList()
sel.SetInputList(inputs)

if False:
    frw = ROOT.TFile.Open("reweight.root")
    hrw = frw.Get("reweight")
    inputs.Add(hrw)

t.Process(sel)
hists = dict((h.GetName(), h) for h in sel.GetOutputList())


def header(text):
    l = ROOT.TLatex()
    ROOT.SetOwnership(l, False)
    l.SetNDC()
    l.SetTextSize(0.7*ROOT.gPad.GetTopMargin())
    l.SetTextFont(42)
    l.SetY(1-0.9*ROOT.gPad.GetTopMargin())
    l.SetTextAlign(31)
    l.SetX(1-ROOT.gPad.GetRightMargin())
    l.SetTitle(text)
    l.Draw()


bx = [(-2, 'bxm2'), (-1, 'bxm1'), (0, 'bx0'), (1, 'bx1'), (2, 'bx2')]


for ibx, bxn in bx:
    c = ROOT.TCanvas()
    c.SetLogy(True)
    eff = ROOT.TEfficiency(hists['num_'+bxn], hists['denom'])
    eff.SetName("prefireEfficiencyMap")
    eff.Draw("colztext")
    c.Paint()
    eff.GetPaintedHistogram().GetZaxis().SetTitle("L1IsoEG30 in BX %d Efficiency (#DeltaR<0.4)" % ibx)
    eff.GetPaintedHistogram().GetZaxis().SetRangeUser(0, 1)
    header(hdr)
    c.Print(outDir+"/Jet_L1IsoEG30eff_%s_looseJet_%s.pdf" % (bxn, era))
    c.Print(outDir+"/Jet_L1IsoEG30eff_%s_looseJet_%s.root" % (bxn, era))
    fout = ROOT.TFile(outDir+"/Map_Jet_L1IsoEG30eff_%s_looseJet_%s.root" % (bxn, era), "recreate")
    eff.Write()
    fout = None
    ROOT.SetOwnership(eff, False)
    ROOT.SetOwnership(c, False)

for ibx, bxn in bx:
    c = ROOT.TCanvas()
    c.SetLogy(True)
    eff = ROOT.TEfficiency(hists['numFinOR_'+bxn], hists['denomFinOR'])
    eff.SetName("prefireEfficiencyMap")
    eff.Draw("colztext")
    c.Paint()
    eff.GetPaintedHistogram().GetZaxis().SetTitle("L1 FinOR in BX %d Efficiency" % ibx)
    eff.GetPaintedHistogram().GetZaxis().SetRangeUser(0, 1)
    header(hdr)
    c.Print(outDir+"/Jet_L1FinOReff_%s_looseJet_%s.pdf" % (bxn, era))
    c.Print(outDir+"/Jet_L1FinOReff_%s_looseJet_%s.root" % (bxn, era))
    fout = ROOT.TFile(outDir+"/Map_Jet_L1FinOReff_%s_looseJet_%s.root" % (bxn, era), "recreate")
    eff.Write()
    fout = None
    ROOT.SetOwnership(eff, False)
    ROOT.SetOwnership(c, False)

for ibx, bxn in bx:
    c2 = ROOT.TCanvas()
    eff2 = ROOT.TEfficiency(hists['numL1A_'+bxn], hists['denomL1A'])
    eff2.GetTotalHistogram().GetYaxis().SetTitle("FinOR in BX %d Efficiency" % ibx)
    eff2.Draw("ap")
    header(hdr)
    l = ROOT.TLegend(0.2, 0.8, 0.5, 0.9)
    l.AddEntry(eff2, "Single jet 2.5 #leq |#eta^{jet}| < 3", "pe")
    l.Draw()
    c2.Paint()
    eff2.GetPaintedGraph().GetYaxis().SetRangeUser(0, 1)
    c2.Print(outDir+"/FinOReff_%s_looseJetEta2p5to3p0_%s.pdf" % (bxn, era))
    c2.Print(outDir+"/FinOReff_%s_looseJetEta2p5to3p0_%s.root" % (bxn, era))
    ROOT.SetOwnership(eff2, False)
    ROOT.SetOwnership(c2, False)
    ROOT.SetOwnership(l, False)


c2 = ROOT.TCanvas()
mg = ROOT.TMultiGraph("mgeffthr", ";Jet p_{T}^{EM} [GeV];BX -1 Trigger Efficiency")
efflow = ROOT.TEfficiency(hists['numJetEGthr_eglow'], hists['denomJetEGthr']).CreateGraph()
efflow.SetMarkerColor(ROOT.kRed)
mg.Add(efflow, "p")
effmed = ROOT.TEfficiency(hists['numJetEGthr_egmed'], hists['denomJetEGthr']).CreateGraph()
effmed.SetMarkerColor(ROOT.kBlue)
mg.Add(effmed, "p")
effhigh = ROOT.TEfficiency(hists['numJetEGthr_eghigh'], hists['denomJetEGthr']).CreateGraph()
effhigh.SetMarkerColor(ROOT.kGreen)
mg.Add(effhigh, "p")
finorm1 = ROOT.TEfficiency(hists['numL1A_bxm1'], hists['denomL1A']).CreateGraph()
finorm1.SetMarkerColor(ROOT.kBlack)
mg.Add(finorm1, "p")
mg.Draw("a")
mg.GetYaxis().SetRangeUser(0, 1)
header(hdr)
l = ROOT.TLegend(0.45, 0.15, 0.9, 0.45)
l.AddEntry(efflow, "L1IsoEG20", "pe")
l.AddEntry(effmed, "L1IsoEG30", "pe")
l.AddEntry(effhigh, "L1IsoEG40", "pe")
l.AddEntry(finorm1, "FinOR", "pe")
l.SetHeader("2.5 #leq |#eta^{jet}| < 3")
l.SetFillColorAlpha(ROOT.kWhite, 0.)
l.Draw()
c2.Print(outDir+"/L1EGthrEff_looseJetEta2p5to3p0_%s.pdf" % (era, ))
c2.Print(outDir+"/L1EGthrEff_looseJetEta2p5to3p0_%s.root" % (era, ))
ROOT.SetOwnership(c2, False)
ROOT.SetOwnership(l, False)

c3 = ROOT.TCanvas()
egmap = hists['jet30EGEtaPhi']
egmap.Draw("colz")
header(hdr)
c3.Paint()
c3.GetFrame().SetFillStyle(1001)
c3.GetFrame().SetFillColor(ROOT.kBlack)
c3.Print(outDir+"/Jet30_L1EGbxm1Position_%s.pdf" % (era, ))
c3.Print(outDir+"/Jet30_L1EGbxm1Position_%s.root" % (era, ))

c4 = ROOT.TCanvas()
hists['jetEGdeltaR_bxm1'].SetLineColor(ROOT.kRed)
hists['jetEGdeltaR_bxm1'].SetMarkerColor(ROOT.kRed)
hists['jetEGdeltaR_bxm1'].Draw("histex0")
hists['jetEGdeltaR_bx0'].Draw("histex0same")
hists['jetEGdeltaR_bx1'].SetLineColor(ROOT.kBlue)
hists['jetEGdeltaR_bx1'].SetMarkerColor(ROOT.kBlue)
hists['jetEGdeltaR_bx1'].Draw("histex0same")
l4 = c4.BuildLegend(0.45, 0.4, 0.8, 0.75)
l4.SetHeader("p_{T}^{j} > 30 GeV, 2.5 #leq |#eta^{j}| < 3")
header(hdr)
c4.Print(outDir+"/JetL1EGDeltaR.pdf")
c4.Print(outDir+"/JetL1EGDeltaR.root")
