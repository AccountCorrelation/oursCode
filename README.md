# Implementation details:
1. "Corpus" Generation
```
ACCM uses a function RandomWalk(·) to generate account sequences, which works as follows: it starts at a vertex 
(account) ai and proceeds along an uniformly randomly selected edge to visit its neighboring account 
at each step, until the maximum length L is reached. 
```
2. Representation Learning
```
We apply SG model to the network to learn node representations while capturing latent structural relationships 
among nodes. 
```
3. Transformation Matrix (W) Learning
```
After learning social representations of accounts into a low-dimensional space for each network, we need to 
transform these learned embeddings across two (or more) networks to a common space for comparison. In this 
work, we train a linear regression model to learn the transformation matrix towards this goal.
```
4. Alignment and Correlation
```
Finally, the account correlation can be performed through the k-nearest neighbor searching. More formally, 
for any account in a network G (∀a ∈ V ), we project its learned representation vector v to the embedding 
space of the network G′ using the optimal W∗. A. a new vector is obtained v′a = W∗ · va. In the representation 
space of network G′, we then calculate the cosine similarity between vector v′(a) and each embedding vector 
vi in V ′, and return the top-k similar results as the predicted correlated accounts in G′ of account a in G.
```

# True/False positive rate for synthetic datasets
1. Buzznet dataset
![Buzznet](./True-False-Positive-Rate/buzznet.pdf)
