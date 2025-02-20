import data
import modules
from torch.optim import AdamW

masked = True
batch_size = 2
seq_len = 4
input_tokens, target_tokens = data.sample(batch_size, seq_len)
xft, tfx = data.get_vocab()

d = 8
vocab_size = len(xft)
num_layers = 6
total_heads = 2
#head_dim = embed_dim / total_heads
model = modules.LanguageModel(d, vocab_size, seq_len, num_layers, total_heads)

print(f"Parameters: {model.parameters()}")

optimizer = AdamW(model.parameters(), lr=5e-5, weight_decay=0.01)

print(f"Optimizer: {optimizer}")
