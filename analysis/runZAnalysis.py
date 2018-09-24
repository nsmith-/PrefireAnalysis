#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
import math
import array

def mkdirp(d):
    if not os.path.exists(d):
        os.makedirs(d)


ROOT.gStyle.SetOptDate(0)
ROOT.gStyle.SetHistLineWidth(2)
ROOT.gStyle.SetPalette(ROOT.kBird)
ROOT.gStyle.SetNumberContours(100)
ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetCanvasDefW(int(600*(1.1)))

# era = "2016H"
era = sys.argv[1]
hdr = "SingleElectron Run%s" % era
f = ROOT.TFile.Open("prefiringZ_Run%s.root" % era)
t = f.Get("ntuple/tree")

outDir = "ZAnalysis/%s" % era
mkdirp(outDir)
mkdirp(outDir+"/fits")

print t.GetEntries()

ROOT.gROOT.ProcessLineSync(".L ZAnalysis.C+")

sel = ROOT.ZAnalysis()
inputs = ROOT.TList()
sel.SetInputList(inputs)


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


for n,h in hists.iteritems():
    c = ROOT.TCanvas(n, n)
    h.Draw("colz" if "2D" in h.ClassName() else "")
    c.Print("%s/%s.pdf" % (outDir, n))


c4 = ROOT.TCanvas()
hists['PhoL1EGDeltaR_bxm1'].SetLineColor(ROOT.kRed)
hists['PhoL1EGDeltaR_bxm1'].SetMarkerColor(ROOT.kRed)
hists['PhoL1EGDeltaR_bxm1'].Draw("histex0")
hists['PhoL1EGDeltaR_bx0'].Draw("histex0same")
hists['PhoL1EGDeltaR_bx1'].SetLineColor(ROOT.kBlue)
hists['PhoL1EGDeltaR_bx1'].SetMarkerColor(ROOT.kBlue)
hists['PhoL1EGDeltaR_bx1'].Draw("histex0same")
hists['PhoL1EGDeltaRsecond'].SetLineColor(ROOT.kGreen)
hists['PhoL1EGDeltaRsecond'].SetMarkerColor(ROOT.kGreen)
hists['PhoL1EGDeltaRsecond'].Draw("histex0same")
l4 = c4.BuildLegend(0.45, 0.4, 0.8, 0.75)
l4.SetHeader("p_{T}^{#gamma} > 15 GeV, 2.5 #leq |#eta^{j}| < 3")
header(hdr)
c4.Print(outDir+"/PhoL1EGDeltaR.pdf")



# 3rd order Bernstein bkg
fcn = ROOT.TF1("zFit", "[0]*5.*TMath::Voigt(x-[1], [2], 2.5)+[3]*(1-(x/120-.25))^3+[4]*3*(x/120-.25)*(1-(x/120-.25))^2+[5]*3*(x/120-.25)^2*(1-(x/120-.25))+[6]*(x/120-.25)^3", 30, 150)
fcn.SetParNames("N_{peak}", "m_{Z}", "#sigma_{res}", "B_{0}", "B_{1}", "B_{2}", "B_{3}")
fcn.SetLineWidth(2)
def resetFcn(h):
    peak = h.Integral(h.FindBin(80), h.FindBin(100))
    tot = h.Integral()
    fcn.SetParameter(0, peak)
    fcn.SetParLimits(0, 0, tot)
    fcn.SetParameter(1, 91)
    fcn.SetParLimits(1, 60, 120)
    fcn.SetParameter(2, 5)
    fcn.SetParLimits(2, 1, 10)
    fcn.SetParameter(3, (tot-peak))
    fcn.SetParLimits(3, 0, tot)
    fcn.SetParameter(4, 0.)
    fcn.SetParLimits(4, 0, tot)
    fcn.SetParameter(5, 0.)
    fcn.SetParLimits(5, 0, tot)
    fcn.SetParameter(6, 0.)
    fcn.SetParLimits(6, 0, tot)


effs = {
    'PhoL1EGMatchPrefireEffEtaIncl': ('ElePhomassL1Pt_bxm1', 'ElePhomassL1Pt_bx0'),
    'PhoL1EGMatchPrefireEffEta1p0': ('ElePhoEta1p0massL1Pt_bxm1', 'ElePhoEta1p0massL1Pt_bx0'),
    'PhoL1EGMatchPrefireEffEta2p0': ('ElePhoEta2p0massL1Pt_bxm1', 'ElePhoEta2p0massL1Pt_bx0'),
    'PhoL1EGMatchPrefireEffEta2p5': ('ElePhoEta2p5massL1Pt_bxm1', 'ElePhoEta2p5massL1Pt_bx0'),
    'L1EGPrefireEffEtaIncl': ('EleL1EGmassL1Pt_bxm1', 'EleL1EGmassL1Pt_bx0'),
    'L1EGPrefireEffEta2p0': ('EleL1EGEta2p0massL1Pt_bxm1', 'EleL1EGEta2p0massL1Pt_bx0'),
    'L1EGPrefireEffEta2p5': ('EleL1EGEta2p5massL1Pt_bxm1', 'EleL1EGEta2p5massL1Pt_bx0'),
}

def etastr(plotname):
    if '2p5' in plotname:
        return "2.5#leq|#eta^{L1}|<3"
    elif '2p0' in plotname:
        return "2.0#leq|#eta^{L1}|<2.5"
    elif '1p0' in plotname:
        return "1.0#leq|#eta^{L1}|<2.0"
    return "0#leq|#eta^{L1}|<3"

fits = {}
def fitProjections(h2d):
    for iY in range(1, h2d.GetNbinsY()+1):
        n = h2d.GetName()+"_bin%d" % iY
        hproj = h2d.ProjectionX(n, iY, iY)
        resetFcn(hproj)
        c = ROOT.TCanvas(n, n)
        hproj.SetStats(True)
        hproj.Draw("ex0")
        hproj.GetYaxis().SetTitle("Counts / 5 GeV")
        fitRes = hproj.Fit(fcn, "ILS")
        c.Update()
        statsbox = hproj.FindObject("stats")
        statsbox.SetY1NDC(0.4)
        statsbox.SetY2NDC(0.8)
        fits[n] = fitRes.Get().Clone()
        #fcn.Draw("same")
        ptstr = "%d#leqp_{T}^{L1}<%d" % (h2d.GetYaxis().GetBinLowEdge(iY), h2d.GetYaxis().GetBinUpEdge(iY))
        header("%s, %s, %s, BX %s" % (hdr, etastr(n), ptstr, "-1" if 'bxm1' in n else "0"))
        c.Print("%s/fits/%s.pdf" % (outDir, n))

for name, pair in effs.iteritems():
    h2d_bxm1 = hists[pair[0]]
    h2d_bx0 = hists[pair[1]]
    fitProjections(h2d_bxm1)
    fitProjections(h2d_bx0)
    nbins = h2d_bx0.GetNbinsY()
    x = array.array('d', [0.]*nbins) 
    xw = array.array('d', [0.]*nbins) 
    y = array.array('d', [0.]*nbins) 
    eyp = array.array('d', [0.]*nbins) 
    eym = array.array('d', [0.]*nbins) 
    for iY in range(1, h2d_bx0.GetNbinsY()+1):
        x[iY-1] = h2d_bx0.GetYaxis().GetBinCenter(iY)
        xw[iY-1] = h2d_bx0.GetYaxis().GetBinWidth(iY)*0.5
        npass = fits[pair[0]+"_bin%d"%iY].Value(0)
        epass = fits[pair[0]+"_bin%d"%iY].Error(0)
        nfail = fits[pair[1]+"_bin%d"%iY].Value(0)
        efail = fits[pair[1]+"_bin%d"%iY].Error(0)
        y[iY-1] = npass / (npass + nfail)
        err = math.hypot( epass*nfail/(npass+nfail)**2, efail*npass/(npass+nfail)**2 )
        eyp[iY-1] = err
        eym[iY-1] = err
        # eyp[iY-1] = ROOT.TEfficiency.ClopperPearson(nall, npass, 0.68, True) - y[iY-1]
        # eym[iY-1] = y[iY-1] - ROOT.TEfficiency.ClopperPearson(nall, npass, 0.68, False)
    geff = ROOT.TGraphAsymmErrors(nbins, x, y, xw, xw, eym, eyp)
    geff.SetNameTitle(name, name)
    c = ROOT.TCanvas(name)
    geff.Draw("ape")
    c.Print("%s/%s.pdf" % (outDir, name))

