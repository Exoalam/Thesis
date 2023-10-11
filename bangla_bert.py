from bnlp import SentencepieceTokenizer

bsp = SentencepieceTokenizer()


input_text = "আমি ভাত খাই। সে বাজারে যায়।"
tokens = bsp.tokenize(input_text)
print(tokens)
text2id = bsp.text2id(input_text)
print(text2id)
id2text = bsp.id2text(text2id)
print(id2text)