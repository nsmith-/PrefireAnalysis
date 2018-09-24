#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
import math
import array
from PassFailSimulFitter import PassFailSimulFitter

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


def header(text, bottom=False):
    l = ROOT.TLatex()
    ROOT.SetOwnership(l, False)
    l.SetNDC()
    l.SetTextSize(0.7*ROOT.gPad.GetTopMargin())
    l.SetTextFont(42)
    l.SetTextAlign(31)
    if bottom:
        l.SetY(0.02)
        l.SetX(1-0.05)
    else:
        l.SetY(1-0.9*ROOT.gPad.GetTopMargin())
        l.SetX(1-ROOT.gPad.GetRightMargin())
    l.SetTitle(text)
    l.Draw()


for n,h in hists.iteritems():
    c = ROOT.TCanvas(n, n)
    h.Draw("colz" if "2D" in h.ClassName() else "")
    c.Print("%s/%s.pdf" % (outDir, n))
    c.Print("%s/%s.root" % (outDir, n))


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



pdfDefL1 = [
    "a0[1]",
    "a1[1,0,50]",
    "a2[1,0,50]",
    "a3[1,0,50]",
    "RooBernstein::backgroundPass(mass, {a0,a1,a2,a3})",
    "b0[1]",
    "b1[1,0,50]",
    "b2[1,0,50]",
    "b3[1,0,50]",
    "RooBernstein::backgroundFail(mass, {b0,b1,b2,b3})",
    "efficiency[0.9,0,1]",
    "numSignalAll[1., 100000.]",
    "numBackgroundPass[0., 100000.]",
    "numBackgroundFail[0., 100000.]",
    "expr::numSignalPass('efficiency*numSignalAll', efficiency, numSignalAll)",
    "expr::numSignalFail('(1-efficiency)*numSignalAll', efficiency, numSignalAll)",
    "RooVoigtian::signalPass(mass, zMassP[91,30,140], 2.5, sigResP[10,4,30])",
    "RooVoigtian::signalFail(mass, zMassF[91,30,140], 2.5, sigResF[10,4,30])",
    "SUM::pdfPass(numSignalPass*signalPass, numBackgroundPass*backgroundPass)",
    "SUM::pdfFail(numSignalFail*signalFail, numBackgroundFail*backgroundFail)",
    "SIMUL::simPdf(decision, Passed=pdfPass, Failed=pdfFail)",
]
pdfDef = [
    "a0[1]",
    "a1[1,0,50]",
    "a2[1,0,50]",
    "a3[1,0,50]",
    "a4[1,0,50]",
    "RooBernstein::backgroundPass(mass, {a0,a1,a2,a3,a4})",
    "b0[1]",
    "b1[1,0,50]",
    "b2[1,0,50]",
    "b3[1,0,50]",
    "b4[1,0,50]",
    "RooBernstein::backgroundFail(mass, {b0,b1,b2,b3,b4})",
    "efficiency[0.9,0,1]",
    "numSignalAll[1., 100000.]",
    "numBackgroundPass[0., 100000.]",
    "numBackgroundFail[0., 100000.]",
    "expr::numSignalPass('efficiency*numSignalAll', efficiency, numSignalAll)",
    "expr::numSignalFail('(1-efficiency)*numSignalAll', efficiency, numSignalAll)",
    "RooVoigtian::signalPass(mass, zMassP[91,81,101], 2.5, sigResP[5,1.4,10])",
    "RooVoigtian::signalFail(mass, zMassF[91,81,101], 2.5, sigResF[5,1.4,10])",
    "SUM::pdfPass(numSignalPass*signalPass, numBackgroundPass*backgroundPass)",
    "SUM::pdfFail(numSignalFail*signalFail, numBackgroundFail*backgroundFail)",
    "SIMUL::simPdf(decision, Passed=pdfPass, Failed=pdfFail)",
]
fitVariable = ROOT.RooRealVar('mass', 'TP Pair Mass', 30, 150, 'GeV')
fitVariable.setBins(24)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)


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
for name, pair in effs.iteritems():
    h2d_bxm1 = hists[pair[0]]
    h2d_bx0 = hists[pair[1]]
    for iY in range(1, h2d_bx0.GetNbinsY()+1):
        nPass = "%s_Pass_bin%d" % (name, iY)
        nFail = "%s_Fail_bin%d" % (name, iY)
        nEff = "eff_%s_bin%d" % (name, iY)
        hpass = h2d_bxm1.ProjectionX(nPass, iY, iY)
        hfail = h2d_bx0.ProjectionX(nFail, iY, iY)
        if hpass.Integral()==0 or hfail.Integral()==0:
            continue
        fitter = PassFailSimulFitter(nEff, fitVariable)
        fitter.setPdf(pdfDef if 'Pho' in name else pdfDefL1)
        fitter.setData("data", hpass, hfail)
        res = fitter.fit("simPdf", "data")
        fits[nEff] = res
        c = fitter.drawFitCanvas(res)
        c.cd()
        ptstr = "%d#leqp_{T}^{L1}<%d" % (h2d_bx0.GetYaxis().GetBinLowEdge(iY), h2d_bx0.GetYaxis().GetBinUpEdge(iY))
        header("%s, %s, %s" % (hdr, etastr(name), ptstr), bottom=True)
        c.Print("%s/fits/%s.pdf" % (outDir, nEff))

    nbins = h2d_bx0.GetNbinsY()
    x = array.array('d', [0.]*nbins) 
    xw = array.array('d', [0.]*nbins) 
    y = array.array('d', [0.]*nbins) 
    eyp = array.array('d', [0.]*nbins) 
    eym = array.array('d', [0.]*nbins) 
    for iY in range(1, h2d_bx0.GetNbinsY()+1):
        x[iY-1] = h2d_bx0.GetYaxis().GetBinCenter(iY)
        xw[iY-1] = h2d_bx0.GetYaxis().GetBinWidth(iY)*0.5
        nEff = "eff_%s_bin%d" % (name, iY)
        if nEff in fits:
            res = fits[nEff]
            effValue = res.floatParsFinal().find('efficiency')
            y[iY-1] = effValue.getVal()
            eym[iY-1] = -1.*effValue.getErrorLo()
            eyp[iY-1] = effValue.getErrorHi()
        else:
            y[iY-1] = 0.
            eym[iY-1] = 0.
            eyp[iY-1] = 1.

    geff = ROOT.TGraphAsymmErrors(nbins, x, y, xw, xw, eym, eyp)
    geff.SetNameTitle(name, name)
    c = ROOT.TCanvas(name)
    geff.Draw("ape")
    c.Print("%s/%s.pdf" % (outDir, name))

