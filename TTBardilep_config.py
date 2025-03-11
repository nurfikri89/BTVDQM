from FWCore.ParameterSet.Config import *

nEvents = 10
filename = "root://xrootd-cms.infn.it///store/data/Run2024D/MuonEG/MINIAOD/PromptReco-v1/000/380/306/00000/bef7affe-4d5b-40c3-9e80-7c6aaac7087b.root"

process = Process("TTBardilepTest")

process.maxEvents = untracked.PSet( input = untracked.int32(nEvents))

process.source = Source("PoolSource",
fileNames = untracked.vstring(filename))


process.bestElectrons = EDFilter("EtaPtMinCandViewSelector",
   src = InputTag("slimmedElectrons"),
   ptMin = double( 30 ),
   etaMin = double( -2.5 ),
   etaMax = double( 2.5 )
)

process.bestMuons = EDFilter("EtaPtMinCandViewSelector",
   src = InputTag("slimmedMuons"),
   ptMin = double( 30 ),
   etaMin = double( -2.4 ),
   etaMax = double( 2.4 )
)

process.nElectronFilter = EDFilter("CandViewCountFilter",
                             src = InputTag("bestElectrons"),
                             minNumber = uint32(1)
)

process.nMuonFilter = EDFilter("CandViewCountFilter",
                             src = InputTag("bestMuons"),
                             minNumber = uint32(1)
)

process.diLepCandsPM = EDProducer("CandViewShallowCloneCombiner",
    decay = string("electrons@+ muons@-"),
    cut = string("mass > 1")
)

process.diLepCandsMP = EDProducer("CandViewShallowCloneCombiner",
    decay = string("electrons@- muons@+"),
    cut = string("mass > 1")
)

process.out = OutputModule("PoolOutputModule",
    fileName = untracked.string("test_out.root")
    )

process.printEventNumber = OutputModule("AsciiOutputModule")

process.select = Path(
    process.bestElectrons *
    process.bestMuons *
    process.nElectronFilter *
    process.nMuonFilter *
    process.diLepCandsPM *
    process.diLepCandsMP 
)
     
process.ep = EndPath(
   process.printEventNumber *
   process.out
)





