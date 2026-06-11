"""
AI Foundations: 10.1 LLM Basics and the Math of Transformers

This tutorial explains the fundamental principles behind Large Language Models (LLMs)
and implements the core mathematical mechanism: Scaled Dot-Product Attention.

CORE CONCEPTS:
1. Predicting Text: LLMs predict the 'next token' based on a sequence of preceding tokens.
2. Tokens: The 'atoms' of text. Words or sub-words converted into numerical IDs.
3. Context Window: The maximum number of tokens a model can process at once.
4. Softmax: A function that turns raw scores into probabilities (summing to 1.0).

THE MATH: THE SELF-ATTENTION MECHANISM
The heart of the Transformer is Attention. It allows the model to 'attend' to
specific parts of the input sequence when processing a specific token.

Formula: Attention(Q, K, V) = softmax( (Q @ K.T) / sqrt(d_k) ) @ V

Where:
- Q (Query): What I'm looking for.
- K (Key): What I contain.
- V (Value): What information I offer.
- d_k: The dimension of the keys (used for scaling to prevent gradient explosion).
"""

import numpy as np


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / e_x.sum(axis=-1, keepdims=True)


def scaled_dot_product_attention(Q, K, V):
    """
    Implements the core math of a Transformer's attention head.
    """
    d_k = Q.shape[-1]

    # 1. Calculate Dot Product of Query and Key
    # This represents 'similarity' or 'relevance'
    scores = np.matmul(Q, K.transpose(0, 2, 1))

    # 2. Scale the scores
    scaled_scores = scores / np.sqrt(d_k)

    # 3. Apply Softmax to get Attention Weights (Probabilities)
    weights = softmax(scaled_scores)

    # 4. Multiply by Values
    # The output is a weighted sum of the values
    output = np.matmul(weights, V)

    return output, weights


# EXAMPLE DATA
# Imagine a sequence of 3 tokens, each represented by a vector of size 4.
batch_size = 1
seq_len = 3
d_model = 4

# Mock input embeddings
X = np.random.randn(batch_size, seq_len, d_model)

# In a real transformer, Q, K, V are learned linear projections of X
W_q = np.random.randn(d_model, d_model)
W_k = np.random.randn(d_model, d_model)
W_v = np.random.randn(d_model, d_model)

Q = np.matmul(X, W_q)
K = np.matmul(X, W_k)
V = np.matmul(X, W_v)

output, attention_weights = scaled_dot_product_attention(Q, K, V)

print("--- Transformer Math Tutorial ---")
print(f"Input Shape (X): {X.shape}")
print(f"Attention Weights Shape: {attention_weights.shape}")
print("\nAttention Weights (Sum across rows is 1.0 due to Softmax):")
print(attention_weights[0])
print("\nOutput Shape (Same as input):", output.shape)
print("\nLogic Summary:")
print("1. We calculate how much 'Query' (current token) matches 'Keys' (all tokens).")
print("2. We normalize these matches into probabilities (Weights).")
print("3. We use those weights to pull information from 'Values'.")
print("4. This allows the model to 'focus' on relevant words in a sentence.")
