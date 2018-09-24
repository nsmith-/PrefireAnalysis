#define ZAnalysis_cxx
// The class definition in ZAnalysis.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.


// The following methods are defined in this file:
//   Begin():      called every time a loop on the tree starts,
//              a convenient place to create your histograms.
//   SlaveBegin():  called after Begin(), when on PROOF called only on the
//              slave servers.
//   Process():    called for each event, in this function you decide what
//              to read and fill your histograms.
//   SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//              called only on the slave servers.
//   Terminate():   called at the end of the loop on the tree,
//              a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// root> T->Process("ZAnalysis.C")
// root> T->Process("ZAnalysis.C","some options")
// root> T->Process("ZAnalysis.C+")
//


#include "ZAnalysis.h"

void ZAnalysis::Begin(TTree * /*tree*/)
{
  // The Begin() function is called at the start of the query.
  // When running with PROOF Begin() is only called on the client.
  // The tree argument is deprecated (on PROOF 0 is passed).

  TString option = GetOption();

  const double l1egPtBinning[] = {5, 10, 20, 30, 40, 50, 100};
  const int nPtBins = sizeof(l1egPtBinning)/sizeof(double)-1;
  const double massBinning[] = {30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150};
  const int nMassBins = sizeof(massBinning)/sizeof(double)-1;

  hEleL1EGmassL1Pt_bxm1_ = newOutput<TH2D>("EleL1EGmassL1Pt_bxm1", "L1EG in BX -1;Electron-L1EG Mass [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hEleL1EGmassL1Pt_bx0_ = newOutput<TH2D>("EleL1EGmassL1Pt_bx0", "L1EG in BX 0;Electron-L1EG Mass [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hEleL1EGmassL1Pt_bx1_ = newOutput<TH2D>("EleL1EGmassL1Pt_bx1", "L1EG in BX 1;Electron-L1EG Mass [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);

  hEleL1EGEta2p0massL1Pt_bxm1_ = newOutput<TH2D>("EleL1EGEta2p0massL1Pt_bxm1", "L1EG in BX -1;Electron-L1EG Mass [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hEleL1EGEta2p0massL1Pt_bx0_ =  newOutput<TH2D>("EleL1EGEta2p0massL1Pt_bx0", "L1EG in BX 0;Electron-L1EG Mass [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hEleL1EGEta2p0massL1Pt_bx1_ =  newOutput<TH2D>("EleL1EGEta2p0massL1Pt_bx1", "L1EG in BX 1;Electron-L1EG Mass [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);

  hEleL1EGEta2p5massL1Pt_bxm1_ = newOutput<TH2D>("EleL1EGEta2p5massL1Pt_bxm1", "L1EG in BX -1;Electron-L1EG Mass [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hEleL1EGEta2p5massL1Pt_bx0_ =  newOutput<TH2D>("EleL1EGEta2p5massL1Pt_bx0", "L1EG in BX 0;Electron-L1EG Mass [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hEleL1EGEta2p5massL1Pt_bx1_ =  newOutput<TH2D>("EleL1EGEta2p5massL1Pt_bx1", "L1EG in BX 1;Electron-L1EG Mass [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);

  hElePhomass_PhoEta_ = newOutput<TH2D>("ElePhomass_PhoEta", "e#gamma Mass;m_{e#gamma} [GeV];|#eta^{#gamma}|;Counts", 24, 30, 150, 30, 0, 3);
  hPhoIso_eta_mCut_ = newOutput<TH2D>("PhoIso_eta_mCut", "Isolation;PF #Sigma h^{0}+#gamma [GeV];|#eta^{#gamma}|;Counts", 30, 0, 60, 30, 0, 3);
  hPhoSieie_eta_mCut_ = newOutput<TH2D>("PhoSieie_eta_mCut", "SigmaIEtaIEta;#sigma_{i#etai#eta};|#eta^{#gamma}|;Counts", 30, 0, 0.05, 30, 0, 3);
  hPhoHoE_eta_mCut_ = newOutput<TH2D>("PhoHoE_eta_mCut", "Hadronic over EM;Hadronic over EM;|#eta^{#gamma}|;Counts", 20, 0, 0.5, 30, 0, 3);
  hElePhoCutmass_PhoEta_ = newOutput<TH2D>("ElePhoCutmass_PhoEta", "Cleaned e#gamma Mass;m_{e#gamma} [GeV];|#eta^{#gamma}|;Counts", 24, 30, 150, 30, 0, 3);

  hPhoL1EGDeltaR_bxm1_ = newOutput<TH1D>("PhoL1EGDeltaR_bxm1", "L1EG in BX -1;#DeltaR(electron,L1EG);Counts", 20, 0, 1);
  hPhoL1EGDeltaR_bx0_ = newOutput<TH1D>("PhoL1EGDeltaR_bx0", "L1EG in BX 0;#DeltaR(electron,L1EG);Counts", 20, 0, 1);
  hPhoL1EGDeltaR_bx1_ = newOutput<TH1D>("PhoL1EGDeltaR_bx1", "L1EG in BX 1;#DeltaR(electron,L1EG);Counts", 20, 0, 1);
  hPhoL1EGDeltaRsecond_ = newOutput<TH1D>("PhoL1EGDeltaRsecond", "Second L1EG;#DeltaR(electron,L1EG);Counts", 20, 0, 1);
  hPhoL1EGnearestBx_ = newOutput<TH2D>("PhoL1EGnearestBx", "EG matches;Closest L1EG bx;Second closest L1EG bx", 3, -1.5, 1.5, 3, -1.5, 1.5);

  hElePhomassL1Pt_bxm1_ = newOutput<TH2D>("ElePhomassL1Pt_bxm1", "L1EG in BX -1;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hElePhomassL1Pt_bx0_ = newOutput<TH2D>("ElePhomassL1Pt_bx0", "L1EG in BX 0;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hElePhomassL1Pt_bx1_ = newOutput<TH2D>("ElePhomassL1Pt_bx1", "L1EG in BX 1;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);

  hElePhoEta1p0massL1Pt_bxm1_ = newOutput<TH2D>("ElePhoEta1p0massL1Pt_bxm1", "L1EG in BX -1;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hElePhoEta1p0massL1Pt_bx0_ =  newOutput<TH2D>("ElePhoEta1p0massL1Pt_bx0", "L1EG in BX 0;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hElePhoEta1p0massL1Pt_bx1_ =  newOutput<TH2D>("ElePhoEta1p0massL1Pt_bx1", "L1EG in BX 1;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);

  hElePhoEta2p0massL1Pt_bxm1_ = newOutput<TH2D>("ElePhoEta2p0massL1Pt_bxm1", "L1EG in BX -1;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hElePhoEta2p0massL1Pt_bx0_ = newOutput<TH2D>("ElePhoEta2p0massL1Pt_bx0", "L1EG in BX 0;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hElePhoEta2p0massL1Pt_bx1_ = newOutput<TH2D>("ElePhoEta2p0massL1Pt_bx1", "L1EG in BX 1;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);

  hElePhoEta2p5massL1Pt_bxm1_ = newOutput<TH2D>("ElePhoEta2p5massL1Pt_bxm1", "L1EG in BX -1;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hElePhoEta2p5massL1Pt_bx0_ = newOutput<TH2D>("ElePhoEta2p5massL1Pt_bx0", "L1EG in BX 0;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
  hElePhoEta2p5massL1Pt_bx1_ = newOutput<TH2D>("ElePhoEta2p5massL1Pt_bx1", "L1EG in BX 1;m_{e#gamma} [GeV];L1EG p_{T} [GeV];Counts", nMassBins, massBinning, nPtBins, l1egPtBinning);
}

void ZAnalysis::SlaveBegin(TTree * /*tree*/)
{
  // The SlaveBegin() function is called after the Begin() function.
  // When running with PROOF SlaveBegin() is called on each slave server.
  // The tree argument is deprecated (on PROOF 0 is passed).

  TString option = GetOption();

}

Bool_t ZAnalysis::Process(Long64_t entry)
{
  using namespace ROOT::Math::VectorUtil;
  auto bit = [] (int i) { return 1<<i; };
  fReader.SetEntry(entry);

  for(size_t iEG=0; iEG<L1EG_p4.GetSize(); ++iEG) {
    auto eg = L1EG_p4[iEG];
    auto bx = L1EG_bx[iEG];
    bool iso = L1EG_iso[iEG] & 1;
    if ( not iso or DeltaR(eg, *tag_electron) < 0.3 ) continue;

    double mass = (eg+*tag_electron).M();
    if ( bx == -1 ) hEleL1EGmassL1Pt_bxm1_->Fill(mass, eg.Pt());
    if ( bx == 0 ) hEleL1EGmassL1Pt_bx0_->Fill(mass, eg.Pt());
    if ( bx == 1 ) hEleL1EGmassL1Pt_bx1_->Fill(mass, eg.Pt());
    
    if ( std::abs(eg.Eta()) > 2.5 ) {
      if ( bx == -1 ) hEleL1EGEta2p5massL1Pt_bxm1_->Fill(mass, eg.Pt());
      if ( bx == 0 )  hEleL1EGEta2p5massL1Pt_bx0_->Fill(mass, eg.Pt());
      if ( bx == 1 )  hEleL1EGEta2p5massL1Pt_bx1_->Fill(mass, eg.Pt());
    }
    else if ( std::abs(eg.Eta()) > 2.0 ) {
      if ( bx == -1 ) hEleL1EGEta2p0massL1Pt_bxm1_->Fill(mass, eg.Pt());
      if ( bx == 0 )  hEleL1EGEta2p0massL1Pt_bx0_->Fill(mass, eg.Pt());
      if ( bx == 1 )  hEleL1EGEta2p0massL1Pt_bx1_->Fill(mass, eg.Pt());
    }
  }

  for(size_t iPho=0; iPho<photon_p4.GetSize(); ++iPho) {
    auto pho = photon_p4[iPho];
    if ( DeltaR(pho, *tag_electron) < 0.3 ) continue;
    double mass = (pho+*tag_electron).M();
    double absEta = std::abs(pho.Eta());
    hElePhomass_PhoEta_->Fill(mass, absEta);
    if ( mass > 80 ) {
      hPhoIso_eta_mCut_->Fill(photon_iso[iPho], absEta);
      hPhoSieie_eta_mCut_->Fill(photon_sieie[iPho], absEta);
      hPhoHoE_eta_mCut_->Fill(photon_hoe[iPho], absEta);
    }
    
    float sieieThresh = (absEta > 1.479) ? 0.0276 : 0.0103;
    if ( pho.Pt() < 15 or photon_iso[iPho] > 15. or photon_sieie[iPho] > sieieThresh or photon_hoe[iPho] > 0.1 ) continue;

    hElePhoCutmass_PhoEta_->Fill(mass, absEta);

    double minDeltaR{999.};
    int L1match{-1};
    int prevL1match{-1};
    for(size_t iEG=0; iEG<L1EG_p4.GetSize(); ++iEG) {
      double dR = DeltaR(L1EG_p4[iEG], pho);
      if ( dR < minDeltaR and (L1EG_iso[iEG] & 1) ) {
        minDeltaR = dR;
        prevL1match = L1match;
        L1match = iEG;
      }
    }
    if ( L1match == -1 ) continue;

    if ( std::abs(pho.Eta()) >= 2.5 ) {
      if ( L1EG_bx[L1match] == -1 ) hPhoL1EGDeltaR_bxm1_->Fill(minDeltaR);
      if ( L1EG_bx[L1match] == 0 ) hPhoL1EGDeltaR_bx0_->Fill(minDeltaR);
      if ( L1EG_bx[L1match] == 1 ) hPhoL1EGDeltaR_bx1_->Fill(minDeltaR);

      if ( prevL1match >= 0 ) {
        hPhoL1EGDeltaRsecond_->Fill(DeltaR(L1EG_p4[prevL1match], pho));
        hPhoL1EGnearestBx_->Fill(L1EG_bx[L1match], L1EG_bx[prevL1match]);
      }
    }

    if ( minDeltaR < 0.2 ) {
      if ( L1EG_bx[L1match] == -1 ) hElePhomassL1Pt_bxm1_->Fill(mass, L1EG_p4[L1match].Pt());
      if ( L1EG_bx[L1match] == 0 )  hElePhomassL1Pt_bx0_->Fill(mass, L1EG_p4[L1match].Pt());
      if ( L1EG_bx[L1match] == 1 )  hElePhomassL1Pt_bx1_->Fill(mass, L1EG_p4[L1match].Pt());

      if ( std::abs(pho.Eta()) >= 2.5 ) {
        if ( L1EG_bx[L1match] == -1 ) hElePhoEta2p5massL1Pt_bxm1_->Fill(mass, L1EG_p4[L1match].Pt());
        if ( L1EG_bx[L1match] == 0 )  hElePhoEta2p5massL1Pt_bx0_->Fill(mass, L1EG_p4[L1match].Pt());
        if ( L1EG_bx[L1match] == 1 )  hElePhoEta2p5massL1Pt_bx1_->Fill(mass, L1EG_p4[L1match].Pt());
      }
      else if ( std::abs(pho.Eta()) >= 2.0 ) {
        if ( L1EG_bx[L1match] == -1 ) hElePhoEta2p0massL1Pt_bxm1_->Fill(mass, L1EG_p4[L1match].Pt());
        if ( L1EG_bx[L1match] == 0 )  hElePhoEta2p0massL1Pt_bx0_->Fill(mass, L1EG_p4[L1match].Pt());
        if ( L1EG_bx[L1match] == 1 )  hElePhoEta2p0massL1Pt_bx1_->Fill(mass, L1EG_p4[L1match].Pt());
      }
      else if ( std::abs(pho.Eta()) >= 1.0 ) {
        if ( L1EG_bx[L1match] == -1 ) hElePhoEta1p0massL1Pt_bxm1_->Fill(mass, L1EG_p4[L1match].Pt());
        if ( L1EG_bx[L1match] == 0 )  hElePhoEta1p0massL1Pt_bx0_->Fill(mass, L1EG_p4[L1match].Pt());
        if ( L1EG_bx[L1match] == 1 )  hElePhoEta1p0massL1Pt_bx1_->Fill(mass, L1EG_p4[L1match].Pt());
      }
    }
  }

  return kTRUE;
}

void ZAnalysis::SlaveTerminate()
{
  // The SlaveTerminate() function is called after all entries or objects
  // have been processed. When running with PROOF SlaveTerminate() is called
  // on each slave server.

}

void ZAnalysis::Terminate()
{
  // The Terminate() function is the last function to be called during
  // a query. It always runs on the client, it can be used to present
  // the results graphically or save the results to file.

}
