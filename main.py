import glob
from Tagger import Tagger

if __name__ == '__main__':
	corpora = glob.glob("corpora/meiroku/*.xml")
	for corpus in corpora:
		M6Tagger = Tagger("surface", corpus)
		## コーパスから語・品詞・外来語IOタグ
		M6Tagger.makeWordPosLoanIO()
		word_pos_loanIO = M6Tagger.getWordPosLoanIO()
		## LoanBI
		M6Tagger.makeCharLoanBIESO()
		char_loanBIESO = M6Tagger.getCharLoanBIESO()
		## 2-gramデータ
		M6Tagger.makeCharBigram()
		bigram = M6Tagger.getCharBigram()
		## Orthoデータ
		M6Tagger.makeCharOrtho()
		ortho = M6Tagger.getCharOrtho()
		## 結果をプリント
		M6Tagger.printMergeList()