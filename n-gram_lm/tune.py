import pandas as pd
import numpy as np
import data
import math
from scipy.optimize import minimize

#vocab = data.get_vocab()
unigram = data.get_unigram() # (index) : log prob
bigram = data.get_bigram() # (index, index) : log prob
trigram = data.get_trigram() # (index, index, index) : log prob
xft, tfx = data.get_lookups() # index from token, token from index
observed_set = data.get_dev_set()

def get_index(t_i):
  if t_i in xft:
    return xft[t_i]
  else:
    # TODO: Decide on how to handle upper / lowercase versions
    # I think it should fall back to lowercase if it can't find the uppercase
    # (?) store probabilities for both cases, and compute combined when needed
    #print(f"Not in vocab: {t_i}")
    return -1

# Loss Function:
def negative_log_likelihood(lambdas, fallback = -1000): # equiv to 1e-1000 raw prob
  print(f"Fallback: {fallback}")
  l1, l2, l3 = lambdas
  print(f"l1: {lambdas[0]}, l2: {lambdas[1]}, l3: {lambdas[2]}")
  total_likelihood = 0

  for sentence in observed_set:
    sentence_likelihood = 0
    # t_i for token string representation, x_i for vocab index representation
    for i, t_i in enumerate(sentence):
      x_i = get_index(t_i)
      if x_i == -1:
        #print(f"Word {t_i} not in vocab")
        unigram_prob = fallback # log prob
        bigram_prob = fallback #
        trigram_prob = fallback #
      else:
        unigram_prob = unigram.get(x_i, fallback) # log prob
        # Note: <s> and </s> are removed from unigram prob
        # fallback value is needed even though these tokens exist in vocab
        print(f"unigram: {unigram.get(x_i, fallback)}, fallback: {fallback}")
        if i == 1: # First word in the sentence after <s>
          bigram_prob = bigram.get((xft['<s>'], x_i), fallback)
          trigram_prob = fallback
        else:
          x_i_min_1 = get_index(sentence[i-1])
          bigram_prob = bigram.get((x_i_min_1, x_i), fallback) # log prob
          x_i_min_2 = sentence[i-2]
          trigram_prob = trigram.get((x_i_min_2, x_i_min_1, x_i), fallback)
      print(f"Uni: {unigram_prob}, Bi: {bigram_prob}, Tri: {trigram_prob}")
      raw_prob = l1 * (10**unigram_prob) + l2 * (10**bigram_prob) + l3 * (10**trigram_prob)
      #print(f"l1: {l1}, l2: {l2}, l3: {l3}")
      #print(f"Raw: {raw_prob}, fallback: {1e-10}, max: {max(raw_prob, 1e-10)}")
      log_prob = math.log10(max(raw_prob, 1e-10))
      sentence_likelihood += log_prob
    total_likelihood += sentence_likelihood
  print(total_likelihood/len(observed_set))
  return -(total_likelihood/len(observed_set))


# Optimization
initial_lambdas = [1/3, 1/3, 1/3]
constraints = [{'type': 'eq', 'fun': lambda x: sum(x) - 1}]  # l1 + l2 + l3 = 1
bounds = [(0, 1), (0, 1), (0, 1)]  # Each lambda must be between 0 and 1

# Minimize the negative log-likelihood
result = minimize(negative_log_likelihood, initial_lambdas, args=(-100,), 
                  constraints=constraints, bounds=bounds)

print(f"Success? : {result.success}")
print(f"Message : {result.message}")

# Optimal weights
optimal_lambdas = result.x
print("Optimal lambdas:", optimal_lambdas)

# [9.49650121e-01 9.37157253e-18 5.03498791e-02]
#l1: 0.19294876040543507, l2: 0.8070512544957388, l3: 0.0

#testval = negative_log_likelihood(initial_lambdas)
#print(testval)