from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    merges = int(request.form['merges'])
    bangla_text = request.form['input_text']
    tokens = []
    for i in range(merges):
        token = byte_pair_encode_bangla(bangla_text, i)
        for x in token:
            if x not in tokens:
                tokens.append(x)
    return f'You entered: {tokens}'

def get_stats(vocab):
    pairs = {}
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pair = (symbols[i], symbols[i + 1])
            if pair in pairs:
                pairs[pair] += freq
            else:
                pairs[pair] = freq
    return pairs

def merge_vocab(pair, v_in):
    v_out = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    for word in v_in:
        w_out = word.replace(bigram, replacement)
        v_out[w_out] = v_in[word]
    return v_out
    
def byte_pair_encode_bangla(text, num_merges):
    vocab = {}
    for word in text.split():
        word = ' '.join(word) + ' </w>'  
        if word in vocab:
            vocab[word] += 1
        else:
            vocab[word] = 1
    
    for i in range(num_merges):
        pairs = get_stats(vocab)
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)
    
    bpe_tokens = set()
    for word in vocab.keys():
        bpe_tokens.update(word.split())
    
    return bpe_tokens


if __name__ == "__main__":
    app.run()