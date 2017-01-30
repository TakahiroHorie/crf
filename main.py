import glob
from Tagger import Tagger

if __name__ == '__main__':
	corpora = glob.glob("corpora/meiroku/*.xml")
	for corpus in corpora:
		M6Tagger = Tagger("surface", corpus)
		## コーパスから語・品詞・外来語IOタグ
		M6Tagger.makeWordPosLoanIO()
		## LoanBI
		M6Tagger.makeCharLoanBIESO()
		## 2-gramデータ
		M6Tagger.makeCharBigram()
		## Orthoデータ
		M6Tagger.makeCharOrtho()
		## 結果をプリント
		# M6Tagger.printMergeList()
		print(M6Tagger.getCharBigram())