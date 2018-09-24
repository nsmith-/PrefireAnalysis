import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing()
options.register(
    "is2016",
    True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "2016 vs 2017+ label name for trigger objects (selectedPatTrigger vs. slimmedPatTrigger)"
)
options.parseArguments()

process = cms.Process("TEST")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring([
        #'/store/data/Run2017F/JetHT/MINIAOD/31Mar2018-v1/30000/54B9283C-C637-E811-A002-B496910A0554.root',
        '/store/data/Run2016H/JetHT/MINIAOD/03Feb2017_ver3-v1/100000/C8E4E1EC-97EA-E611-BC0D-001E67792738.root',
    ]),
    secondaryFileNames = cms.untracked.vstring([
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70006/E2AD6AFB-BDDF-E711-A932-0025905A6104.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70006/5260FD8C-BDDF-E711-BA7D-0CC47A7C34EE.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70006/FAFE3491-BDDF-E711-A5FC-0025905A6134.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70002/D4287C60-D5DF-E711-B716-A0369FD8FDB0.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70002/24B20F66-D6DF-E711-871A-008CFA1C6564.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50000/46F6F25F-CBDE-E711-8525-02163E014624.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50000/E62A295A-CBDE-E711-9F6B-02163E0118C5.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50001/06999498-79DF-E711-9E0D-02163E01364E.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50002/08E8F29F-AEDF-E711-B155-02163E01348C.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50002/BE7A8FBE-B4DF-E711-824F-02163E01A46F.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50002/E44994FE-BBDF-E711-818E-02163E0136F5.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70003/8E2E748B-1FE0-E711-9608-008CFAFC53C6.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70003/A2DA6C02-2CE0-E711-A436-A0369FC5D5A4.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70003/B2B65D7E-05E0-E711-A5A0-02163E012509.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70003/D4080733-06E0-E711-8E1D-02163E0129F1.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70004/CE523E1C-8DE0-E711-A6AC-008CFA197D38.root',
        #'/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70004/DC645294-27E0-E711-8C0C-3417EBE64567.root',
        '/store/data/Run2016H/JetHT/AOD/PromptReco-v3/000/284/038/00000/E45D54F1-779F-E611-A271-02163E011CBF.root',
        '/store/data/Run2016H/JetHT/AOD/PromptReco-v3/000/284/039/00000/DE1B6E0E-759F-E611-865D-02163E014719.root',
        '/store/data/Run2016H/JetHT/AOD/PromptReco-v3/000/284/042/00000/E2E0BED8-6D9F-E611-825B-FA163E88EBC7.root',
        '/store/data/Run2016H/JetHT/AOD/PromptReco-v3/000/284/043/00000/0433CA2C-9F9F-E611-AE55-02163E012007.root',
        '/store/data/Run2016H/JetHT/AOD/PromptReco-v3/000/284/043/00000/4EDD51A4-CE9F-E611-9E9D-02163E014310.root',
        '/store/data/Run2016H/JetHT/AOD/PromptReco-v3/000/284/043/00000/566A0223-C49F-E611-BF3B-02163E01230B.root',
        '/store/data/Run2016H/JetHT/AOD/PromptReco-v3/000/284/043/00000/88BE1171-C79F-E611-95CF-02163E01352A.root',
    ]),
)

process.prefireVetoFilter = cms.EDFilter("TriggerRulePrefireVetoFilter",
    l1AcceptRecordLabel = cms.InputTag("scalersRawToDigi"),
)

process.ntuple = cms.EDAnalyzer("PrefiringJetAna",
    triggerRule = cms.InputTag("prefireVetoFilter:ruleIndex"),
    jetSrc = cms.InputTag("slimmedJets"),
    metSrc = cms.InputTag("slimmedMETs"),
    tagJetCut = cms.string("pt > 30 && userInt('looseJetId')"),
    l1egSrc = cms.InputTag("caloStage2Digis:EGamma"),
    l1jetSrc = cms.InputTag("caloStage2Digis:Jet"),
    l1GtSrc = cms.InputTag("gtStage2Digis"),
    triggerObjects = cms.InputTag("selectedPatTrigger" if options.is2016 else "slimmedPatTrigger"),
    triggerPrescales = cms.InputTag("patTrigger"),
)

process.bxm1_pass = cms.EDAnalyzer("L1EGCheck",
    l1egSrc = cms.InputTag("caloStage2Digis:EGamma"),
    bx = cms.int32(-1),
)

process.bxm1_fail = cms.EDAnalyzer("L1EGCheck",
    l1egSrc = cms.InputTag("caloStage2Digis:EGamma"),
    bx = cms.int32(-1),
)

process.skimPath = cms.Path(process.prefireVetoFilter+process.bxm1_pass+process.ntuple)

# process.failntuple = process.ntuple.clone()
# process.checkPath = cms.Path(~process.prefireVetoFilter+process.bxm1_fail+process.failntuple)
process.checkPath = cms.Path(~process.prefireVetoFilter+process.bxm1_fail)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("ntuple.root"),
    closeFileFast = cms.untracked.bool(True)
)

