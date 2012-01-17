# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <markdowncell>

# <a href="http://www.amazon.com/Book-Abstract-Algebra-Second-Mathematics/dp/0486474178">A Book of Abstract Algebra, second edition</a> Practice Problems

# <markdowncell>

# Chapter 9: Isomorphism
# =========
# 
# Two groups are isomorphic if an isomorphism can be shown from one to the other, in either direction.
# 
# A function $f: G \rightarrow H$ is an isomorphism between the groups G and H if it is bijective and linear.
# 
# Bijective and Linear means: 
# 
# * $f(a) = f(b) \Leftrightarrow a = b$ &nbsp; (injective)
# * $\forall h \in H, \exists g \in G \ s.t. \ f(g) = h$ &nbsp; (surjective)
# * $f(ab) = f(a) \circ f(b)$ &nbsp; (linear)

# <markdowncell>

# 9-A: Isomorphism is an Equivalence Relation among Groups
# --------------------------------------------------------
# For all isomorphisms:
# 
# 1.  Every group is isomorphic to itself
# 2.  If $G_1 \simeq G_2$, then $G_2 \simeq G_1$ (isomorphism is commutative)
# 3.  If $G_1 \simeq G_2$, and $G_2 \simeq G_3$, then $G_1 \simeq G_3$ (isomorphism is transitive)
# 
# 1) Let G be any group. If $\varepsilon: G \rightarrow G$ is the identity function, $\varepsilon(x) = x$, show that $\varepsilon$ is an isomorphism.
# 
# * the identity function is trivially bijective
# * $\varepsilon(ab) = ab = \varepsilon(a)\varepsilon(b)$
# 
# The conditions of an isomorphism are satisfied by $\varepsilon$.
# 
# 2) Let $G_1$ and $G_2$ be groups, and $f: G_1 \rightarrow G_2$ be an isomorphism.  Show that $f^{-1}: G_2 \rightarrow G_1$ is an isomorphism.

# <codecell>


