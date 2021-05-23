import collections
import os
import random

from PyQt5.QtWidgets import QMessageBox, QWidget

rootPath = os.path.abspath(os.path.join(os.getcwd(), "..")) + "\\"
sourcePath = rootPath + "source\\words\\"
AllWords = []  # 全词信息
OnlyTranslates = []
OnlyWords = []
word2translate = {}  # 单词-翻译
translate2word = {}  # 翻译-单词
word2symbol = {}  # 单词-音标
word2character = {}  # 单词-词性
character2word = collections.defaultdict(list)  # 词性-单词

with open(sourcePath + "all.txt", "r", encoding="utf-8") as source:
    for w in source:
        wordline = w.split("\t")
        wordline = list(map(str.strip, wordline))
        AllWords.append(wordline[:-1])
        OnlyWords.append(wordline[0])
        OnlyTranslates.append(wordline[2])
        word2translate[wordline[0]] = wordline[-2]
        translate2word[wordline[-2]] = wordline[0]
        word2symbol[wordline[0]] = wordline[1]
        word2character[wordline[0]] = wordline[2]
        character2word[wordline[2]].append(wordline[0])
OnlyWords = tuple(OnlyWords)


def charConvert(Beforechar):
    # ['adj.', 'adv.', 'v.', 'int.', 'prep.', 'art.', 'conj.', 'n.', 'vi.', 'num.', 'pron.', 'vt.']
    if Beforechar == "默认(不论词性)":
        allwords = []
        for v in character2word.values():
            allwords += v
        return allwords
    elif Beforechar == "形容词/副词":
        return character2word['adj.'] + character2word['adv.']
    elif Beforechar == "名词":
        return character2word['n.']
    elif Beforechar == "动词":
        return character2word['vi.'] + character2word['v.'] + character2word['vt.']
    else:
        return character2word['int.'] + character2word['prep.'] + character2word['art.'] + character2word['conj.'] + \
               character2word['num.'] + character2word['pron.']


def RandomSelect(rules, effect):
    oWord = list(OnlyWords)
    number = random.randint(0, 3)
    words = charConvert(rules)
    trueWord = random.choice(words)
    trueTranslate = word2translate[trueWord]
    print(len(OnlyWords), "\n")
    oWord.remove(trueWord)

    otherWords_word = random.sample(oWord, 3)
    print(otherWords_word)
    if effect == "E2C":
        otherWords = [word2translate[w] for w in otherWords_word]
        otherWords.insert(number, trueTranslate)
        otherWords.insert(0,
                          (str(number + 1), trueWord, word2symbol[trueWord], word2character[trueWord], trueTranslate))
    elif effect == "C2E":
        otherWords = [w for w in otherWords_word]
        otherWords.insert(number, trueWord)
        otherWords.insert(0,
                          (str(number + 1), trueWord, word2symbol[trueWord], word2character[trueWord], trueTranslate))
    return otherWords

# 从文本中获取单词
def getWords(rules):
    if rules == "所有词汇":
        return AllWords
    elif rules == "已掌握词汇":
        MasteredWord_source = sourcePath + "mastered.txt"
        words = []
        if not os.path.exists(MasteredWord_source):
            file = open(MasteredWord_source, "w", encoding="utf-8")
            file.close()
        if not os.path.getsize(MasteredWord_source):
            message = QWidget()
            QMessageBox.information(message, '提示', '掌握词汇表中无单词', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            with open(MasteredWord_source, "r", encoding="utf-8") as file:
                for line in file.readlines():
                    words.append(line.split())
        return words
    elif rules == "未掌握词汇":
        NotMasteredWord_source = sourcePath + "notmastered.txt"
        words = []
        if not os.path.exists(NotMasteredWord_source):
            file = open(NotMasteredWord_source, "w", encoding="utf-8")
            file.close()
        if not os.path.getsize(NotMasteredWord_source):
            message = QWidget()
            QMessageBox.information(message, '提示', '未掌握词汇表中无单词', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            with open(NotMasteredWord_source, "r", encoding="utf-8") as file:
                for line in file.readlines():
                    words.append(line.split())
        return words
