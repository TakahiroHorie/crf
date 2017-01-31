## convert into IOtagged data
import re, jaconv
from xml.etree.ElementTree import *

class XMLProcessor:
	def __init__(self, corpus:str):
		self.corpus = corpus

		self.__convData = None

	## TODO: XML処理の機能を分ける
	def convertXML2List(self):
		tree = parse(self.corpus)
		root = tree.getroot()
		elem_sen = root.findall(".//s")
		data = []
		for sent in elem_sen:
			new_sent = []
			for wordeme in sent:
				new_sent.append([wordeme.tag, wordeme.get("orthToken"), wordeme.get("lForm"), wordeme.get("pos")])
			data.append(new_sent)
		self.__convData = data

	def getXML2List(self): return self.__convData




class Tagger:

	def __init__(self, strType:str, corpus:str):
		self.strType = strType ## katakana, surface
		self.corpus = corpus

		self.__wordPosIOData = None
		self.__charBIESOData = None
		self.__bigramData = None
		self.__orthoData = None

	## TODO: XML処理の機能を分ける
	def makeWordPosLoanIO(self):
		tree = parse(self.corpus)
		root = tree.getroot()
		elem_sen = root.findall(".//s")
		data = []
		for sent in elem_sen:
			new_sent = []
			for wordeme in sent:
				if wordeme.tag in ["quotation", "lb", "pb"]: continue
				## spanタグ(外来語)のとき一階下のSUWを見る
				if (wordeme.tag == "span"):
					ea = wordeme.find("SUW")
					pos = ea.get("pos")
					new_sent.append([ea.get("orthToken"), pos, "I-外来語"])
				## 外来語以外
				elif (wordeme.tag == "SUW"):
					eb = wordeme
					if eb != None:
						pos = eb.get("pos")
						## case: katakana
						if self.strType == "katakana":
							if eb.get("lForm") != "": new_sent.append([eb.get("lForm"), pos, "O-外来語"])
							else: new_sent.append([eb.get("orthToken"), pos, "O-外来語"])
						## case: surface
						elif self.strType == "surface":
							new_sent.append([eb.get("orthToken"), pos, "O-外来語"])		
			data.append(new_sent)
		self.__wordPosIOData = data

	def makeCharLoanBIESO(self):
		data = []
		for sent in self.__wordPosIOData:
			new_sent = []
			for i in range(len(sent)):
				word = sent[i]
				for j in range(len(word[0])):
					
					if (word[2] == "I-外来語"):
						if len(word[0]) == 1: loan_tag = "S"
						elif (j == 0): loan_tag = "B"
						elif (j == len(word[0])-1): loan_tag = "E"
						else: loan_tag = "I"
					elif (word[2] == "O-外来語"): loan_tag = "O"

					new_sent.append([word[0][j], loan_tag])
			data.append(new_sent)
		self.__charBIESOData = data

	def makeCharBigram(self):
		data = []
		for sent in self.__wordPosIOData:
			new_sent = []
			for i in range(len(sent)):
				word = sent[i]
				for j in range(len(word[0])):
					if i == 0 and j == 0: char_prev = "BOS"
					elif j == 0: char_prev = sent[i-1][0][-1]
					else: char_prev = word[0][j-1]

					if (i == len(sent)-1) and (j == len(word[0])-1): char_next = "EOS" 
					elif (j == len(word[0])-1): char_next = sent[i+1][0][0]
					else: char_next = word[0][j+1]

					char = word[0][j]
					bigram_1 = char_prev + char
					bigram_2 = char + char_next

					new_sent.append([bigram_1, bigram_2])

			data.append(new_sent)
		self.__bigramData = data

	def makeCharOrtho(self):
		## Hi: ひらがな, Ka: カタカナ, Ch: 漢字, Se: 送り仮名
		## Nu: 数詞, Br: 括弧類, Pu: punctuation, An: その他
		re_Hi = re.compile(r"[ぁ-ん]")
		re_Ka = re.compile(r"[ァ-ヴ]")
		re_Ch = re.compile(r"[一-龠|々|ヿ|〓]")

		orthoData = []
		for sent in self.__wordPosIOData:
			new_sent = []
			for word in sent:
				poss = self.procPos(word[1])
				for char in word[0]:
					ortho = ""
					if "動詞" in poss:
						if re_Ch.search(char)!=None: ortho = "Ch"
						## 動詞のカタカナ部分は別扱い
						elif re_Hi.search(char)!=None: ortho = "Se"
					elif "数詞" in poss: ortho = "Nu"
					elif ("括弧開" in poss) or ("括弧閉" in poss): ortho = "Br"
					elif "読点" in poss: ortho = "Pu"
					else:
						if re_Ch.search(char)!=None: ortho = "Ch"
						elif re_Hi.search(char)!=None: ortho = "Ka"
						elif re_Ka.search(char)!=None: ortho = "Ka"
						else: ortho = "An"
					new_sent.append([ortho])
			orthoData.append(new_sent)
		self.__orthoData = orthoData

	def getWordPosLoanIO(self): return self.__wordPosIOData

	def getCharLoanBIESO(self): return self.__charBIESOData

	def getCharBigram(self): return self.__bigramData

	def getCharOrtho(self): return self.__orthoData

	def printMergeList(self):
		## WORD, POS, IO
		## CHAR, BIESO, BIGRAM(len=2), ORTHO
		for (a, b, c) in zip(self.__charBIESOData, self.__bigramData, self.__orthoData):
			for i in range(len(a)):
				print("{0[0]} {2[0]} {1[0]} {1[1]} {0[1]}".format\
					([jaconv.hira2kata(word) for word in a[i]],\
					 [jaconv.hira2kata(word) for word in b[i]], c[i]))
				# print("{0[0]} {2[0]}".format([jaconv.hira2kata(word) for word in a[i]], b[i], c[i]))
			print("")

	## 品詞情報から細分類を抽出
	def procPos(self, pos:str):
		pos_list = pos.split("-")
		return pos_list



























		