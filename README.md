Solving suduku with improving backtracking tree search

I created 3 verions, each with added search features, to compare the effectiveness of each feature.

Version 1: Simple backtracking search

Version 2: Added forward Checking (maintining arc consistency)

Version 3: Added ordering and filtering

Define
<img src="https://latex.codecogs.com/svg.latex?\Large&space;X_{i,j}" title="l1.1" /> where <img src="https://latex.codecogs.com/svg.latex?\Large&space;i,j\in∈\{1,2,3,4,5,6,7,8,9\}" title="l1.2" />

The Domain of each <img src="https://latex.codecogs.com/svg.latex?\Large&space;X_{i,j}" title="l2.1" /> is <img src="https://latex.codecogs.com/svg.latex?\Large&space;\{1,2,3,4,5,6,7,8,9\}" title="l2.2" />

Constraints:
<img src="https://latex.codecogs.com/svg.latex?\Large&space;(\forall∀i,j,k|j=k\lor∨X_{i,j}\neq≠X_{i,k})" title="l3" />

<img src="https://latex.codecogs.com/svg.latex?\Large&space;(\forall∀i,j,k|i=k\lor∨X_{i,j}\neq≠X_{k,j})" title="l4" />

<img src="https://latex.codecogs.com/svg.latex?\Large&space;(\forall∀n\in∈\{0,1,2\},i,j|(i=⌊\frac{i-1}{3}⌋3+n\land∧j=\lfloor⌊\frac{j-1}{3}\rfloor⌋3+n)\lor∨X_{i,j}\neq≠X_{\lfloor⌊\frac{i-1}{3}\rfloor⌋3+n,\lfloor⌊\frac{j-1}{3}\rfloor⌋3+n})" title="l4" />


![versionComparison](/graphic.png)

