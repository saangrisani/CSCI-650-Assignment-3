# Sean Angrisani

## Question 1

The given languages are:

- L₁ = {ε, aa, bc, a}
- L₂ = {bcb, c, aa}
- L₃ = {a, aa, abc}

### (a) (L₂ ∩ L₁)L₃

I first find the strings shared by L₂ and L₁. The only common string is aa, so:

L₂ ∩ L₁ = {aa}.

I then concatenate aa with each string in L₃:

- aa · a = aaa
- aa · aa = aaaa
- aa · abc = aaabc

Therefore, **(L₂ ∩ L₁)L₃ = {aaa, aaaa, aaabc}.**

### (b) L₂(L₁ − L₃)

I first remove from L₁ every string that also appears in L₃. Both a and aa are removed, leaving:

L₁ − L₃ = {ε, bc}.

I then concatenate each string in L₂ with both remaining strings. Concatenating with ε leaves a string unchanged:

- bcb · ε = bcb
- bcb · bc = bcbbc
- c · ε = c
- c · bc = cbc
- aa · ε = aa
- aa · bc = aabc

Therefore, **L₂(L₁ − L₃) = {bcb, bcbbc, c, cbc, aa, aabc}.**

## Question 6

My favorite problem is the Traveling Salesman Problem. Its decision version is NP-complete: given a collection of locations, travel costs, and a bound B, does a tour exist that visits every location once, returns to the start, and costs at most B? Finding the shortest such tour is the NP-hard optimization version.

I like this problem because I can connect it to my girlfriend's uncle's work with a DJI drone. He uses a predefined flight to capture images of an area, then uploads them to create a map and locate features such as individual rocks. If the required capture locations are fixed, choosing an efficient order to visit them and return to the launch point is a TSP-style routing problem. The mapping and coordinate calculations are separate, but the flight-planning connection makes the problem feel practical to me.

## Question 7

The topic I found most interesting in the second part of the semester was NP-completeness, especially polynomial-time reductions. I liked seeing how problems that initially look unrelated can share the same underlying difficulty. TSP stood out because I could connect it to planning an efficient drone flight, rather than thinking about it only as an abstract graph problem. I also found it interesting that checking a proposed route against a distance bound can be straightforward even when finding the best route is much harder.

My least favorite topic was filling out CYK tables by hand. I understand how the table determines whether a string belongs to a context-free language, but checking every split and production became repetitive. I preferred the reductions and optimization problems because I found their applications more engaging.
