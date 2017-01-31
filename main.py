import glob
from Tagger import Tagger, XMLProcessor

if __name__ == '__main__':
	corpora = glob.glob("corpora/meiroku/*.xml")
	for corpus in corpora:
		# M6Tagger = Tagger("surface", corpus)
		# ## get attributes from corpus
		# M6Tagger.makeWordPosLoanIO()
		# M6Tagger.makeCharLoanBIESO()
		# M6Tagger.makeCharBigram()
		# M6Tagger.makeCharOrtho()

		# M6Tagger.printMergeList()

		M6Proc = XMLProcessor(corpus)
		## get attributes from corpus
		M6Proc.convertXML2List()
		print(M6Proc.getXML2List())