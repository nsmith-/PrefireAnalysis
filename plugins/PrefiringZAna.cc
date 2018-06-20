// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/transform.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"

#include "TTree.h"

#include "Math/LorentzVector.h"
#include "Math/PxPyPzE4D.h"
// == reco::LorentzVector
typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> LorentzVector;

namespace {
  struct EventStruct {
    Long64_t run;
    Long64_t lumi;
    Long64_t event;
    int bunchCrossing;
    int triggerRule;
    
    LorentzVector tag_electron;

    std::vector<LorentzVector> photon_p4;
    std::vector<float> photon_sieie;
    std::vector<float> photon_hoe;
    std::vector<float> photon_iso;

    std::vector<int> L1EG_bx;
    std::vector<LorentzVector> L1EG_p4;
    std::vector<int> L1EG_iso;
  };

  std::vector<const pat::TriggerObjectStandAlone*> getMatchedObjs(const float eta, const float phi, const std::vector<pat::TriggerObjectStandAlone>& trigObjs, const float maxDeltaR=0.1)
  {
    std::vector<const pat::TriggerObjectStandAlone*> matchedObjs;
    const float maxDR2 = maxDeltaR*maxDeltaR;
    for(auto& trigObj : trigObjs){
      const float dR2 = reco::deltaR2(eta,phi,trigObj.eta(),trigObj.phi());
      if(dR2<maxDR2) matchedObjs.push_back(&trigObj);
    }
    return matchedObjs;
  }
}

class PrefiringZAna : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
  public:
    explicit PrefiringZAna(const edm::ParameterSet&);
    ~PrefiringZAna();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    // virtual void beginJob() override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    // virtual void endJob() override;

    edm::EDGetTokenT<int> triggerRuleToken_;
    edm::EDGetTokenT<pat::ElectronCollection> electronToken_;
    // edm::EDGetTokenT<edm::ValueMap<bool>> mediumIdToken_;
    edm::EDGetTokenT<reco::VertexCollection> vertexToken_;
    StringCutObjectSelector<pat::Electron> tagElectronCut_;
    edm::EDGetTokenT<reco::PhotonCollection> photonsToken_;
    edm::EDGetTokenT<BXVector<l1t::EGamma>> l1egToken_;
    edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjectsToken_;
    edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescalesToken_;

    TTree * tree_;
    EventStruct event_;
};

PrefiringZAna::PrefiringZAna(const edm::ParameterSet& iConfig):
  triggerRuleToken_(consumes<int>(iConfig.getParameter<edm::InputTag>("triggerRule"))),
  electronToken_(consumes<pat::ElectronCollection>(iConfig.getParameter<edm::InputTag>("electronSrc"))),
  //  mediumIdToken_(consumes<edm::ValueMap<bool>>(iConfig.getParameter<edm::InputTag>("mediumId"))),
  vertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexSrc"))),
  tagElectronCut_(iConfig.getParameter<std::string>("tagElectronCut")),
  photonsToken_(consumes<reco::PhotonCollection>(iConfig.getParameter<edm::InputTag>("photonSrc"))),
  l1egToken_(consumes<BXVector<l1t::EGamma>>(iConfig.getParameter<edm::InputTag>("l1egSrc"))),
  triggerObjectsToken_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("triggerObjects"))),
  triggerPrescalesToken_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("triggerPrescales")))
{
  usesResource("TFileService");
  edm::Service<TFileService> fs;

  tree_ = fs->make<TTree>("tree","Event Summary");
  tree_->Branch("run", &event_.run);
  tree_->Branch("lumi", &event_.lumi);
  tree_->Branch("event", &event_.event);
  tree_->Branch("bunchCrossing", &event_.bunchCrossing);
  tree_->Branch("triggerRule", &event_.triggerRule);
  tree_->Branch("tag_electron", &event_.tag_electron);
  tree_->Branch("photon_p4", &event_.photon_p4);
  tree_->Branch("photon_sieie", &event_.photon_sieie);
  tree_->Branch("photon_hoe", &event_.photon_hoe);
  tree_->Branch("photon_iso", &event_.photon_iso);
  tree_->Branch("L1EG_bx", &event_.L1EG_bx);
  tree_->Branch("L1EG_p4", &event_.L1EG_p4);
  tree_->Branch("L1EG_iso", &event_.L1EG_iso);
}


PrefiringZAna::~PrefiringZAna()
{
}

void
PrefiringZAna::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  event_.run = iEvent.run();
  event_.lumi = iEvent.luminosityBlock();
  event_.event = iEvent.id().event();
  event_.bunchCrossing = iEvent.bunchCrossing();

  Handle<int> triggerRuleHandle;
  iEvent.getByToken(triggerRuleToken_, triggerRuleHandle);
  event_.triggerRule = *triggerRuleHandle;

  Handle<pat::ElectronCollection> electronHandle;
  iEvent.getByToken(electronToken_, electronHandle);
  // const auto inputId = electronHandle.id();

  // Handle<ValueMap<bool>> mediumIdHandle;
  // iEvent.getByToken(mediumIdToken_, mediumIdHandle);

  Handle<reco::VertexCollection> vertexHandle;
  iEvent.getByToken(vertexToken_, vertexHandle);
  const auto& pv = vertexHandle->at(0);

  Handle<reco::PhotonCollection> photonsHandle;
  iEvent.getByToken(photonsToken_, photonsHandle);

  Handle<BXVector<l1t::EGamma>> l1egHandle;
  iEvent.getByToken(l1egToken_, l1egHandle);

  Handle<pat::TriggerObjectStandAloneCollection> triggerObjectsHandle;
  iEvent.getByToken(triggerObjectsToken_, triggerObjectsHandle);

  Handle<pat::PackedTriggerPrescales> triggerPrescalesHandle;
  iEvent.getByToken(triggerPrescalesToken_, triggerPrescalesHandle);
  const edm::TriggerResults& triggerResults = triggerPrescalesHandle->triggerResults();


  pat::Electron * tagEl = nullptr;
  for(size_t iEl=0; iEl<electronHandle->size(); ++iEl) {
    // Writeable so cut string can access new data
    pat::Electron el(electronHandle->at(iEl));

    // el.addUserInt("MediumId", mediumIdHandle->get(inputId, iEl));
    el.addUserFloat("dxy", el.gsfTrack()->dxy(pv.position()));
    el.addUserFloat("dz", el.gsfTrack()->dz(pv.position()));

    std::vector<const pat::TriggerObjectStandAlone*> matchedTrigObjs = getMatchedObjs(el.superCluster()->eta(), el.superCluster()->phi(), *triggerObjectsHandle, 0.3);
    int pass2016trigger{0};
    int pass2017trigger{0};
    for (const auto trigObjConst : matchedTrigObjs) {
      pat::TriggerObjectStandAlone trigObj(*trigObjConst);
      trigObj.unpackNamesAndLabels(iEvent, triggerResults);

      // HLT_Ele25_eta2p1_WPTight_Gsf_v OR HLT_Ele27_WPTight_Gsf_v
      if ( trigObj.hasFilterLabel("hltEle25erWPTightGsfTrackIsoFilter") || trigObj.hasFilterLabel("hltEle27WPTightGsfTrackIsoFilter") ) {
        pass2016trigger = 1;
      }
      // HLT_Ele32_WPTight_Gsf with special recipe
      if ( trigObj.hasFilterLabel("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter") && trigObj.hasFilterLabel("hltEGL1SingleEGOrFilter") ) {
        pass2017trigger = 1;
      }
    }
    el.addUserInt("pass2016trigger", pass2016trigger);
    el.addUserInt("pass2017trigger", pass2017trigger);

    // take highest pt electron for now
    if ( tagEl == nullptr and tagElectronCut_(el) ) {
      tagEl = &el;
    }
  }
  if ( tagEl == nullptr ) return;

  event_.tag_electron = tagEl->p4();


  event_.photon_p4.clear();
  event_.photon_sieie.clear();
  event_.photon_hoe.clear();
  event_.photon_iso.clear();
  for(const auto& pf : *photonsHandle) {
    if ( pf.energy() < 10. ) {
      continue;
    }
    event_.photon_p4.push_back(pf.p4());
    event_.photon_sieie.push_back(pf.sigmaIetaIeta());
    event_.photon_hoe.push_back(pf.hadronicOverEm());
    event_.photon_iso.push_back(pf.neutralHadronIso()+pf.photonIso());
  }


  event_.L1EG_bx.clear();
  event_.L1EG_p4.clear();
  event_.L1EG_iso.clear();

  auto readBx = [&] (const BXVector<l1t::EGamma>& egVect, int bx) {
    for (auto itL1=l1egHandle->begin(bx); itL1!=l1egHandle->end(bx); ++itL1) {
      event_.L1EG_bx.push_back(bx);
      event_.L1EG_p4.push_back(itL1->p4());
      event_.L1EG_iso.push_back(itL1->hwIso());
    }
  };

  readBx(*l1egHandle, -2);
  readBx(*l1egHandle, -1);
  readBx(*l1egHandle,  0);
  readBx(*l1egHandle,  1);
  readBx(*l1egHandle,  2);

  tree_->Fill();
}


void
PrefiringZAna::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


DEFINE_FWK_MODULE(PrefiringZAna);
