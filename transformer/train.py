import data
import modules
from torch.optim import AdamW

masked = True
batch_size = 2
seq_len = 4
input_batches, target_batches = data.get_training_sequences(batch_size, seq_len)

'''
'''
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

'''
X = input_batches[1]
Y = target_batches[1]

print(f"Loss: {loss}")
'''
batch_index = 0
total_batches = len(input_batches)
for X, Y in zip(input_batches, target_batches):
	logits, loss = model(X, targets=Y)
	print(f"Batch {batch_index} of {total_batches}. Loss: {loss}")
	loss.backward()
	optimizer.step()
	batch_index += 1

