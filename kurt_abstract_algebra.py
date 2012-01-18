# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <markdowncell>

# <a href="http://www.amazon.com/Book-Abstract-Algebra-Second-Mathematics/dp/0486474178">A Book of Abstract Algebra, second edition</a> Practice Problems

# <markdowncell>

# Chapter 9: Isomorphism
# =========
# 
# $G \simeq H$ means G is isomorphic to H.
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
# 1) Let G be any group. If $\varepsilon: G \rightarrow G$ is the identity function,
# $\varepsilon(x) = x$, show that $\varepsilon$ is an isomorphism.
# 
# * the identity function is trivially bijective
# * $\varepsilon(ab) = ab = \varepsilon(a)\varepsilon(b)$
# 
# The conditions of an isomorphism are satisfied by $\varepsilon$.  
# $G \simeq G$.
# 
# 2) Let $G_1$ and $G_2$ be groups, and $f: G_1 \rightarrow G_2$ be an isomorphism.
# Show that $f^{-1}: G_2 \rightarrow G_1$ is an isomorphism.
# 
# * Since $f$ is bijective, $f^{-1}$ is also bijective.
# * Let $c,d \in G_2$,.  
# Since $f$ is surjective, $\exists a,b \in G_1$ such that $c=f(a)$ and $d=f(b)$.    
# Since $f$ is an isomorphism, $f(ab) = f(a)f(b) = cd$.  
# $f^{-1}$ of both sides, $f^{-1}(f(ab)) = ab = f^{-1}(cd)$.  
# By definition of $f^{-1}$, $f^{-1}(c)=a$ and $f^{-1}(d)=b$.  
# Substituting for $a$ and $b$ gets $f^{-1}(c)f^{-1}(d) = f^{-1}(cd)$.  
# 
# $f^{-1}$ is both linear and bijective, $\Rightarrow$ $f^{-1}$ is an isomorphism.  
# $G_1 \simeq G_2 \Leftrightarrow G_2 \simeq G_1$
# 
# 
# 3) Let $G_1$, $G_2$, and $G_3$ be groups, 
# and let $f: G_1 \rightarrow G_2$ and $g: G_2 \rightarrow G_3$ be ismorphisms.  
# Prove that $g \circ f: G_1 \rightarrow G_3$ is an isomorphism.
# 
# * Since $f$ and $g$ are bijective, $g \circ f$ is bijective.
# * Since $f$ is linear, $f(ab) = f(a)f(b)$  
# Take $g$ of both sides, $g(f(ab)) = g(f(a)f(b))$  
# Since g is linear, $g(f(a)f(b)) = g(f(a))g(f(b))$  
# $g(f(ab)) = g(f(a)f(b)) = g(f(a))g(f(b))$  
# $(g \circ f)(ab) = (g \circ f)(a)(g \circ f)(b)$  
# In other words, the composition of two linear transformations is a linear transformation
# 
# $g \circ f$ is both linear and bijective, $\Rightarrow$ $g \circ f$ is an isomorphism.  
# $G_1 \simeq G_2$ and $G_2 \simeq G_3$ $\Rightarrow$ $G_1 \simeq G_3$

# <markdowncell>

# 9-B: Elements which Correspond under an Isomorphism
# -------------
# 
# An isomorphism $f$ from $G_1$ to $G_2$ is a one-to-one correspondence between $G_1$ and $G_2$ satisfying $f(ab)=f(a)f(b)$  
# $f$ matches every element of $G_1$ with a corresponding element of $G_2$  
# It is important to note that:
# 
# 1.  $f$ matches the neutral/identity element of $G_1$ with the neutral element of $G_2$
# 2.  If $f$ matches an element $x$ in $G_1$ with $y$ in $G_2$ , then, neccesarily, $f$ matches $x^{-1}$ with $y^{-1}$  
# That is, if $x \leftrightarrow y$ then $x^{-1} \leftrightarrow y^{-1}$
# 3. $f$ matches a generator of $G_1$ with a generator of $G_2$
# 
# 
# 1) if $e_1$ denotes the neutral element of $G_1$ and $e_2$ denotes the neutral element of $G_2$, prove that $f(e_1)=e_2$
# 
# Let $b = f(a)$.  
# Since $f$ is linear, $f(a) = f(e_1a) = f(e_1)f(a)$.  
# Substitute $f(a) = b$ $\Rightarrow$ $b = f(e_1)b$.  
# Right-multiply both sides by $b^{-1}$, $e_2 = f(e_1)$.
# 
# For any isomorphism $f: G_1 \rightarrow G_2$, the neutral element of $G_1$ is mapped to the neutral element of $G_2$
# 
# 2) Prove that for each $a$ in $G_1$, $f(a^{-1}) = [f(a)]^{-1}$
# 
# Let $b = f(a)$.  
# From part (1), $f(e_1) = e_2$.  
# Since $f$ is linear, $e_2 = f(e_1) = f(aa^{-1}) = f(a^{-1})f(a) = f(a^{-1})b$.  
# Remove the middle steps: $e_2 = f(a^{-1})b$  
# Right multiply by $b^{-1}$ : $b^{-1} = f(a^{-1})$  
# Substitute $b = f(a)$ : $[f(a)]^{-1} = f(a^{-1})$  
# 
# 3) If $G_1$ is a cyclic group with generator $a$, prove that $G_2$ is also a cyclic group, with generator $f(a)$.
# 
# $G_1$ is a cyclic group with generator $a$, $\Rightarrow$ $\forall g_1 \in G_1, a^{n} = g_1$ for some $n$.  
# $f$ : $G_1 \rightarrow G_2$ is an isomorphism $\Rightarrow$ $\forall g_2 \in G_2, f(g_1) = g_2$ for some $g_1 \in G_1$.  
# $\forall g_2 \in G_2, f(a^{n}) = g_2$ for some $n$.  
# Since $f$ is linear, $f(a^{n}) = [f(a)]^{n}$.  
# $\forall g_2 \in G_2, [f(a)]^{n} = g_2$ for some $n$.  
# $f(a)$ is a generator of $G_2$.  

# <markdowncell>

# 9-C: Isomorphism of some Finite Groups
# -----------
# In each of the following, $G$ and $H$ are finite groups.  Determine whether or not $G \simeq H$.  Prove your answer in either case.  
# To find an isomorphism from $G$ to $H$ will require a little ingenuity.  
# For example, if $G$ and $H$ are cyclic groups, it is clear that we must match a generator $a$ for $G$ with a generator $b$ of $H$;  
# that is, $f(a) = b$.  Then $f(aa) = bb$, $f(aaa) = bbb$, and so on.
# If $G$ and $H$ are not cyclic, we have other ways: for example,  
# if $G$ has an element which is its own inverse, it must be matched with an element $H$ having the same property.  
# Often, the specifics of a problem will suggest an isomorphism, if we keep our eyes open.  
# 
# To prove that a specific one-to-one correspondence $f: G \rightarrow H$ is an isomorphism,  
# we may check that it transforms the table of $G$ onto the table of $H$.
# 
# 1) $G$ is the checkerboard game group of Chapter 3  
# (four elements, move diagonal, move left/right, move up/down, hold still; multiplying two moves means applying them one after the other: for example L/R*U/D=Diagonal)  
# $H$ is the group of the complex numbers  {$i, -i, 1, -1$} under multiplication.
# 
# 2) $G$ is the same as in part 1.  $H = \mathbb{Z}_4$
# 
# 3) $G$ is the group $P_2$ of subsets of a two-element set.  $H$ is as in part 1.
# 
# 4) $G$ is $S_3$.  $H$ is the group of matrices described on page 28 of this text.  
# [skip if isomorphic -- requires grinding through a 5x5 table]
# 
# 5) $G$ is the coin group game of Chapter 3, Exercise E.  $H$ is $D_4$, the group of symmetries of the square.
# 
# 6) $G$ is the group of symmetries of the rectangle.  $H$ is as in part 1.
# 
# Up/Down = Reflect across x-axis
# Left/Right = Reflect across y-axis
# Diagonal = Rotate 180 degrees

