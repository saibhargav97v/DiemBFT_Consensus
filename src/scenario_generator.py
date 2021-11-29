import random
from more_itertools import set_partitions


def generate_heuristic_partitions(num_partitions, nodes, twins, partition_limit, is_Deterministic, seed):

    random.seed(seed)
    gen_partitions = set()
    f = len(twins)
    n = len(nodes)
    total_nodes = nodes + list(twins.values())
    count = 0
    
    while len(gen_partitions) < partition_limit and count <= 10000:
        count += 1
        groups = set()
        number_of_quorum_partitions = random.randint(1, num_partitions)  #randomly select the number of partitions that will have quorum}
        if is_Deterministic:
            for i in range(number_of_quorum_partitions):    # deterministically select 2f+1 nodes for each partition that will have a quorum}
                quorum_partition = frozenset(random.choice([nodes[(i+j)%n],twins.get(nodes[(i+j)%n],None) or nodes[(i+j)%n]])
            for j in range(2*f+1))  # select a node or its twin for the partition
                groups.add(quorum_partition)

        else:
            while len(groups) < number_of_quorum_partitions:
                possible_group = random.sample(total_nodes, 3*f + 1)    
                # \textcolor{blue}{randomly select 3f+1 items from list of all nodes and twins}
                final_group = set()
                random.shuffle(possible_group)              #textcolor{blue}{shuffle the selected nodes}
                for node in possible_group:
                    if twins.get(node,None) not in final_group:      #textcolor{blue}{build a 2f+1 partition where both a node and its twin will not be present simultaneously}
                        final_group.add(node)
                    if len(final_group) == 2*f+1:
                        break
                groups.add(frozenset(final_group))

        # print(f'groups after quorum {groups}')

        if num_partitions - number_of_quorum_partitions > 0:
            possible_groups = [[frozenset(j) for j in i] for i in set_partitions(total_nodes,num_partitions-number_of_quorum_partitions)]
            #textcolor{blue}{generate all possible partition combinations}
            while len(groups) < num_partitions:     #textcolor{blue}{Add a random combination to the groups, ensure it is not already present in the set.}
                for i in possible_groups[random.randint(0, len(possible_groups)-1)]:
                    groups.add(i)
                    if len(groups) == num_partitions:
                        break
        gen_partitions.add(frozenset(groups))
    
    res = [[list(j) for j in i] for i in gen_partitions]
    return res

partitions = generate_heuristic_partitions(3, [0,1,2,3], {0:4}, 25, False, 42)
print(partitions)

