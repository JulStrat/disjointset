class  UnionFind:

    def  __init__(self,  n,  pathop=None):
        self._parent  =  [i for i in range(n)]
        self._root  =  set(self._parent)

        if  pathop  ==  'compression':
            self.find  =  self._compression
        elif  pathop  ==  'splitting':
            self.find  =  self._splitting
        elif  pathop  ==  'halving':
            self.find  =  self._halving

    def  _compression(self,  x):
        r  =  x
        while  r  !=  self._parent[r]:
            r  =  self._parent[r]
        while  x  !=  r:
            p  =  self._parent[x]
            self._parent[x]  =  r
            x  =  p
        return x

    def  _splitting(self,  x):
        while  x  !=  self._parent[x]:
            p  =  self._parent[x]
            self._parent[x]  =  self._parent[p]
            x  =  p
        return x

    def  _halving(self,  x):
        while  x  !=  self._parent[x]:
            p  =  self._parent[x]
            self._parent[x]  =  self._parent[p]
            x  =  self._parent[x]
        return x

    def  find(self,  x):
        while  x  !=  self._parent[x]:
            x  =  self._parent[x]
        return x

    def  root_set(self):
        return self._root.copy()

    def  connected(self,  x,  y):
        return (self.find(x)  ==  self.find(y))

    def  union(self,  x,  y):
        rx,  ry  =  self.find(x),  self.find(y)
        if  rx  ==  ry:
            return False
        if  self._parent[rx]  <  self._parent[ry]:
            rx,  ry  =  ry,  rx
        self._parent[ry]  =  rx
        self._root.remove(ry)
        return True

    def  size(self):
        return len(self._root)

    def  __len__(self):
        return len(self._parent)

class  UnionFindWeighted(UnionFind):

    def  __init__(self,  s,  pathop=None):
        UnionFind.__init__(self,  s,  pathop)
        self._weight  =  [1]*(len(self._parent))

    def  union(self,  x,  y):
        rx,  ry  =  self.find(x),  self.find(y)
        if  rx  ==  ry:
            return False
        if  self._weight[rx]  <  self._weight[ry]:
            rx,  ry  =  ry,  rx
        self._parent[ry]  =  rx
        self._weight[rx]  +=  self._weight[ry]
        self._root.remove(ry)
        return True

    def weight(self, x):
        return self._weight[self.find(x)]

class  UnionFindRanked(UnionFind):

    def  __init__(self,  s,  pathop=None):
        UnionFind.__init__(self,  s,  pathop)
        self._rank  =  [0]*(len(self._parent))
        
    def  union(self,  x,  y):
        rx,  ry  =  self.find(x),  self.find(y)
        if  rx  ==  ry:
            return False
        if  self._rank[rx]  ==  self._rank[ry]:
            self._rank[rx]  +=  1
        elif  self._rank[rx]  <  self._rank[ry]:
            rx,  ry  =  ry,  rx
        self._parent[ry]  =  rx
        self._root.remove(ry)
        return True

    def rank(self, x):
        return self._rank[self.find(x)]

class  UnionFindCrossed(UnionFind):     

    def union(self, x, y):
        while self._parent[x] != self._parent[y]:
            if self._parent[x] < self._parent[y]:
                x, y = y, x
            if y == self._parent[y]:
                self._parent[y] = self._parent[x]
                self._root.remove(y)
                return True
            t = self._parent[y]
            self._parent[y] = self._parent[x]
            y = t
        return False

if __name__ == 'builtins':
    import  networkx  as  nx
    from  random  import  shuffle
    grph  =  nx.erdos_renyi_graph(400,  0.1,  seed=None,  directed=False)
    edg  =  list(grph.edges())
    print("edges  -  ",  len(edg))
    cut_value,  partition  =  nx.stoer_wagner(grph)
    print("stoer_wagner  -  ",  cut_value)
    gmin_cut  =  float('inf')
    for  __  in  range(400):
        shuffle(edg)
        #ds  =  UnionFindCrossed(400,  pathop='compression')
        ds  =  UnionFindCrossed(400)
        i  =  0
        while  ds.size()  >  2  and  i  <  len(edg):
            ds.union(edg[i][0],  edg[i][1])
            i  +=  1
        #print(ds.size(),  i)    
        min_cut  =  0
        while  i  <  len(edg):
            if  not  ds.connected(edg[i][0],  edg[i][1]):
                min_cut  +=  1
            if  min_cut  >=  gmin_cut:
                break
            i  +=  1        
        if  min_cut  <  gmin_cut:
            gmin_cut  =  min_cut
    print("karger  -  ",  gmin_cut)
