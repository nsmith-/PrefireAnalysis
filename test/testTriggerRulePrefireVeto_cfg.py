import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process("TEST")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring([
        '/store/data/Run2017F/JetHT/MINIAOD/31Mar2018-v1/30000/54B9283C-C637-E811-A002-B496910A0554.root',
    ]),
    secondaryFileNames = cms.untracked.vstring([
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70006/E2AD6AFB-BDDF-E711-A932-0025905A6104.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50000/46F6F25F-CBDE-E711-8525-02163E014624.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50000/E62A295A-CBDE-E711-9F6B-02163E0118C5.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50001/06999498-79DF-E711-9E0D-02163E01364E.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50002/08E8F29F-AEDF-E711-B155-02163E01348C.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50002/BE7A8FBE-B4DF-E711-824F-02163E01A46F.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/50002/E44994FE-BBDF-E711-818E-02163E0136F5.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70002/24B20F66-D6DF-E711-871A-008CFA1C6564.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70002/D4287C60-D5DF-E711-B716-A0369FD8FDB0.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70003/8E2E748B-1FE0-E711-9608-008CFAFC53C6.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70003/A2DA6C02-2CE0-E711-A436-A0369FC5D5A4.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70003/B2B65D7E-05E0-E711-A5A0-02163E012509.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70003/D4080733-06E0-E711-8E1D-02163E0129F1.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70004/CE523E1C-8DE0-E711-A6AC-008CFA197D38.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70004/DC645294-27E0-E711-8C0C-3417EBE64567.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70006/5260FD8C-BDDF-E711-BA7D-0CC47A7C34EE.root',
        '/store/data/Run2017F/JetHT/AOD/17Nov2017-v1/70006/FAFE3491-BDDF-E711-A5FC-0025905A6134.root',
    ]),
)

process.prefireVetoFilter = cms.EDFilter("TriggerRulePrefireVetoFilter",
    l1AcceptRecordLabel = cms.InputTag("scalersRawToDigi"),
)
process.skimPath = cms.Path(process.prefireVetoFilter)

process.skimOutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dropMetaData = cms.untracked.string('NONE'),
    fastCloning = cms.untracked.bool(True),
    fileName = cms.untracked.string("output.root"),
    overrideInputFileSplitLevels = cms.untracked.bool(False),
    outputCommands = cms.untracked.vstring(
        'keep *_*_*_PAT',
        # 'drop *',
        # 'keep *_*_*_HLT',
        # 'keep *_*Stage2Digis*_*_*',
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring(
            'skimPath',
        )
    ),
)
process.output_step = cms.EndPath(process.skimOutput)

process.schedule = cms.Schedule(
    process.skimPath,
    process.output_step,
)
