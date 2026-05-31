
---

##node

- current state
- parent
- action (from parent to get state)
- path cost

---

##approach

- frontier begins with initial state
- repeat:
    len(frontier)==0, return no solution
    remove node from frontier -> (LIFO / FIFO)
    goal test, if true return node
    expand, add node to frontier, ONLY -> if not in frontier and if not in explored

---

##remove from node

- LIFO -> depth first search
- FIFO -> breadth first search