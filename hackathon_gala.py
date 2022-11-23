class Network:

    def __init__(self, network):
        self.network = network
        self.row = len(network)

    def bredth_first_search(self, source, target, parent):

        visited = [False] * self.row
        queue = [source]
        visited[source] = True

        while queue:
            node = queue.pop()
            for idx, val in enumerate(self.network[node]):
                if visited[idx] is False and val > 0:
                    queue.append(idx)
                    visited[idx] = True
                    parent[idx] = node

        return visited[target]

    def ford_fulkerson(self, start, destination):

        parent = [-1] * self.row
        max_flow = 0

        while self.bredth_first_search(start, destination, parent):

            path_flow = float("Inf")
            node = destination
            while node != start:
                path_flow = min(path_flow, self.network[parent[node]][node])
                node = parent[node]

            # Adding the path flows to the maximum flow
            max_flow += path_flow

            # Updating the edge capacities
            node = destination
            while node != start:
                parent_node = parent[node]
                self.network[parent_node][node] -= path_flow
                self.network[node][parent_node] += path_flow
                node = parent[node]

        return max_flow


def createNetwork(N, M, Teams, Tables):
    
    total_nodes = N + M + 2
    total_teams = len(Teams)
    total_tables = len(Tables)
    network = [[0] * total_nodes for _ in range(total_nodes)]

    # Creating the edges from the source node
    network[0][1:total_teams + 1] = Teams

    # Creating the edges from the teams to the tables
    team_to_table_edge = [1]*total_tables
    for team_idx in range(1, total_teams + 1):
        network[team_idx][total_teams + 1:total_nodes - 1] = team_to_table_edge

    # Creating the edges from the tables to the target node
    counter = 0
    for table_idx in range(total_teams + 1, total_nodes - 1):
        network[table_idx][-1] = Tables[counter]
        counter += 1

    return network


if __name__ == "__main__":    
    parameter_list = []
    for _ in range(4):
        line = input().split()
        parameter_list.append(list(map(int, line)))

    N, M, teams, tables = parameter_list[0][0], parameter_list[1][0], parameter_list[2], parameter_list[3]
    
    network = createNetwork(N, M, teams, tables)
    graph = Network(network)

    start = 0
    destination = N+M+1

    print(graph.ford_fulkerson(start, destination))
