#AODV-lite (on-demand) per simulazione multi-hop: BFS, cache con TTL e ricostruzione del path.
from collections import deque, defaultdict
import time

class AODV:
    def __init__(self, neighbors: dict[str, list[str]] | dict[str, set[str]], ttl_seconds: int = 300):
        self.N = {k: set(v) for k, v in neighbors.items()}
        self.routing_table: dict[str, dict[str, tuple[str, int, float]]] = defaultdict(dict)
        self.ttl_seconds = ttl_seconds

    #Controlla se la rotta node→dest esiste ed è ancora valida (TTL)
    def _valid(self, node: str, dest: str) -> bool:
        entry = self.routing_table.get(node, {}).get(dest)
        if not entry:
            return False
        return time.time() < entry[2]

    #Rimuove voci scadute dalla routing_table (TTL superato)
    def clear_expired(self):
        now = time.time()
        for n, dests in list(self.routing_table.items()):
            for d, (_, _, exp) in list(dests.items()):
                if now >= exp:
                    del dests[d]
            if not dests:
                del self.routing_table[n]
                
    #Cerca un un percorso src→dest con BFS, se trovato lo installa nella tabella
    def discover(self, src: str, dest: str) -> list[str] | None:
        self.clear_expired()
        q = deque([src])
        parent = {src: None}
        while q:
            u = q.popleft()
            if u == dest:
                return self._install_path(src, dest, parent)
            for v in self.N.get(u, set()):
                if v not in parent:
                    parent[v] = u
                    q.append(v)
        return None

    #Ricostruisce il cammino dalla BFS e aggiorna la routing table con next_hop/hop_count
    def _install_path(self, src: str, dest: str, parent: dict[str, str | None]) -> list[str]:
        path = []
        cur = dest
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        expiry = time.time() + self.ttl_seconds
        L = len(path)
        for i in range(L - 1):
            u = path[i]
            nh = path[i + 1]
            hop_count = L - i - 1
            self.routing_table[u][dest] = (nh, hop_count, expiry)
        return path
        
    #Restituisce un percorso già in tabella (se valido), seguendo i next_hop
    def get_path(self, src: str, dest: str) -> list[str] | None:
        if not self._valid(src, dest):
            return None
        path = [src]
        cur = src
        guard = 0
        while cur != dest and guard < 100:
            nh = self.routing_table.get(cur, {}).get(dest, (None, None, None))[0]
            if nh is None:
                return None
            path.append(nh)
            cur = nh
            guard += 1
        return path if path[-1] == dest else None
