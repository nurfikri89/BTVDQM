import FWCore.ParameterSet.Config as cms

nEvents = 30000
# nEvents = -1

filename = "root://xrootd-cms.infn.it//store/data/Run2024I/MuonEG/MINIAOD/PromptReco-v2/000/386/694/00000/1324bb20-fc5c-4095-b27e-54a62156e229.root"
# filename = "file:./1324bb20-fc5c-4095-b27e-54a62156e229.root"

process = cms.Process("SelectElMuPlusJets")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(nEvents))

process.source = cms.Source("PoolSource",
fileNames = cms.untracked.vstring(filename))


#
# Define Loose and Signal Muons. Count them and filter events
#
process.looseMuonsBTVDQM = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("slimmedMuons"),
    cut = cms.string("(pt > 20) && (abs(eta)<2.4) && (passed('CutBasedIdLoose'))"),
    filter = cms.bool(False)
)
process.signalMuonsBTVDQM = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("looseMuonsBTVDQM"),
    cut = cms.string("(pt > 30) && passed('CutBasedIdMediumPrompt')"),
    filter = cms.bool(False)
)
process.nLooseMuonsCountBTVDQM = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1),
    src = cms.InputTag("looseMuonsBTVDQM")
)
process.nSignalMuonsCountBTVDQM = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1),
    src = cms.InputTag("signalMuonsBTVDQM")
)


#
# Define Loose and Signal Electrons. Count them and filter events
#
process.looseElectronsBTVDQM = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("slimmedElectrons"),
    cut = cms.string(
        "(pt > 20) "
        "&& ((abs(superCluster().eta())<2.4) && (abs(superCluster().eta())<1.4442) || (abs(superCluster().eta())>1.5660)) "
        "&& (electronID('cutBasedElectronID-RunIIIWinter22-V1-loose')) "
    ),
    filter = cms.bool(False)
)
process.signalElectronsBTVDQM = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("looseElectronsBTVDQM"),
    cut = cms.string("(pt > 30) && electronID('cutBasedElectronID-RunIIIWinter22-V1-tight')"),
    filter = cms.bool(False)
)
process.nLooseElectronsCountBTVDQM = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1),
    src = cms.InputTag("looseElectronsBTVDQM")
)
process.nSignalElectronsCountBTVDQM = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1),
    src = cms.InputTag("signalElectronsBTVDQM")
)


process.diLepElMuCandsBTVDQM = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("signalMuonsBTVDQM@+ signalElectronsBTVDQM@-"),
    # cut = cms.string("(mass > 20) && (charge=0)")
    cut = cms.string("")
)
process.diLepElMuCandsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("diLepElMuCandsBTVDQM"),
    minNumber = cms.uint32(1),
)


#
# merge signal muons and signal electrons
# Use it for overlap removal of signal jets
#
process.signalLeptonsBTVDQM = cms.EDProducer("CandViewMerger",
  src = cms.VInputTag("signalMuonsBTVDQM", "signalElectronsBTVDQM")
)
# process.selectedJetsBTVDQM = cms.EDFilter("PATJetRefSelector",
process.selectedJetsBTVDQM = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("slimmedJetsPuppi"),
    cut = cms.string(
        "(pt > 30) && (abs(eta) < 2.5)"
    ),
    filter = cms.bool(False)
)
process.signalJetsBTVDQM = cms.EDFilter("DeltaROverlapExclusionSelector",
   src = cms.InputTag('selectedJetsBTVDQM'),
   overlap = cms.InputTag('signalLeptonsBTVDQM'),
   maxDeltaR = cms.double(0.4),
   filter = cms.bool(False),
)
process.nSignalJetsBTVDQM = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(2),
    maxNumber = cms.uint32(9999),
    src = cms.InputTag("signalJetsBTVDQM")
)


process.twoHighestPtSignalJetsBTVDQM = cms.EDFilter('LargestPtCandViewSelector',
    src = cms.InputTag('signalJetsBTVDQM'),
    maxNumber = cms.uint32(2),
    filter = cms.bool(False),
)

#
# This will dump a new MiniAOD, with the same content as input MiniAOD plus with the new collections added
#
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("test_out.root"),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('selectPath')
    ),
)


#
# Quick histogramming
#
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("histo.root")
)
process.histsSignalMuonsBTVDQM = cms.EDAnalyzer("CandViewHistoAnalyzer",
    src = cms.InputTag("signalMuonsBTVDQM"),
    histograms = cms.VPSet(
        cms.PSet(
           min = cms.untracked.double(0.0),
           max = cms.untracked.double(300.0),
           nbins = cms.untracked.int32(30),
           description = cms.untracked.string('muon transverse momentum [GeV]'),
           name = cms.untracked.string('muonPt'),
           plotquantity = cms.untracked.string('pt'),
        ),
        cms.PSet(
           min = cms.untracked.double(-2.0),
           max = cms.untracked.double(2.0),
           nbins = cms.untracked.int32(40),
           description = cms.untracked.string('muon pseudo rapidity'),
           name = cms.untracked.string('muonEta'),
           plotquantity = cms.untracked.string('eta'),
        ),
    )
)
process.histsSignalElectronsBTVDQM = cms.EDAnalyzer("CandViewHistoAnalyzer",
    src = cms.InputTag("signalElectronsBTVDQM"),
    histograms = cms.VPSet(
        cms.PSet(
           min = cms.untracked.double(0.0),
           max = cms.untracked.double(300.0),
           nbins = cms.untracked.int32(30),
           description = cms.untracked.string('elec transverse momentum [GeV]'),
           name = cms.untracked.string('elecPt'),
           plotquantity = cms.untracked.string('pt'),
        ),
        cms.PSet(
           min = cms.untracked.double(-2.0),
           max = cms.untracked.double(2.0),
           nbins = cms.untracked.int32(40),
           description = cms.untracked.string('elec pseudo rapidity'),
           name = cms.untracked.string('elecEta'),
           plotquantity = cms.untracked.string('eta'),
        ),
    )
)

process.histsDiLepElMuCandsBTVDQM = cms.EDAnalyzer("CandViewHistoAnalyzer",
    src = cms.InputTag("diLepElMuCandsBTVDQM"),
    histograms = cms.VPSet(
        cms.PSet(
           min = cms.untracked.double(0.0),
           max = cms.untracked.double(200.0),
           nbins = cms.untracked.int32(20),
           description = cms.untracked.string('mass Dilep'),
           name = cms.untracked.string('mass'),
           plotquantity = cms.untracked.string('mass'),
        ),
    )
)


process.histsTwoHighestPtSignalJetsBTVDQM = cms.EDAnalyzer("CandViewHistoAnalyzer",
    src = cms.InputTag("twoHighestPtSignalJetsBTVDQM"),
    histograms = cms.VPSet(
        cms.PSet(
           min = cms.untracked.double(0.0),
           max = cms.untracked.double(300.0),
           nbins = cms.untracked.int32(30),
           description = cms.untracked.string('jet %d transverse momentum [GeV]'),
           name = cms.untracked.string('jet_%d_pt'),
           plotquantity = cms.untracked.string('pt'),
           itemsToPlot = cms.untracked.int32(3),
        ),
        cms.PSet(
           min = cms.untracked.double(-2.5),
           max = cms.untracked.double(2.5),
           nbins = cms.untracked.int32(50),
           description = cms.untracked.string('jet %d pseudo rapidity'),
           name = cms.untracked.string('jet_%d_eta'),
           plotquantity = cms.untracked.string('eta'),
           itemsToPlot = cms.untracked.int32(3),
        ),
    )
)
#
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideHistogramUtilities
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideEDMNtuples
#

process.printEventNumber = cms.OutputModule("AsciiOutputModule")

process.selectPath = cms.Path(
    process.looseMuonsBTVDQM
    +process.signalMuonsBTVDQM
    +process.looseElectronsBTVDQM
    +process.signalElectronsBTVDQM
    +process.nLooseMuonsCountBTVDQM
    +process.nLooseElectronsCountBTVDQM
    +process.nSignalMuonsCountBTVDQM
    +process.nSignalElectronsCountBTVDQM
    +process.signalLeptonsBTVDQM
    +process.diLepElMuCandsBTVDQM
    +process.diLepElMuCandsFilter
    +process.selectedJetsBTVDQM
    +process.signalJetsBTVDQM
    +process.nSignalJetsBTVDQM
    +process.twoHighestPtSignalJetsBTVDQM
    +process.histsSignalMuonsBTVDQM
    +process.histsSignalElectronsBTVDQM
    +process.histsDiLepElMuCandsBTVDQM
    +process.histsTwoHighestPtSignalJetsBTVDQM
)

process.ep = cms.EndPath(
   process.printEventNumber *
   process.out
)