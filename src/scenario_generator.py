import random
from more_itertools import set_partitions


def generate_heuristic_partitions(num_partitions, nodes, twins, partition_limit, is_Deterministic, seed):

    random.seed(seed)
    gen_partitions = []
    f = len(twins)
    n = len(nodes)
    total_nodes = nodes + twins
    
    while len(gen_partitions) < partition_limit:
        groups = []
        number_of_quorum_partitions = random.randint(1, num_partitions)  #randomly select the number of partitions that will have quorum}

        if is_Deterministic:
            for i in range(number_of_quorum_partitions):    # deterministically select 2f+1 nodes for each partition that will have a quorum}
                for j in range(2*f+1):
                    groups.append(random.choice([nodes[(i+j)%n],twins[(i+j)%f]]))
                    #select a node or its twin for the partition
                # groups.add(quorum_partition)

        else:
            while len(groups) < number_of_quorum_partitions:
                possible_group = random.sample(total_nodes, 3*f + 1)    
                # \textcolor{blue}{randomly select 3f+1 items from list of all nodes and twins}
                final_group = set()
                random.shuffle(possible_group)              #textcolor{blue}{shuffle the selected nodes}
                for node in possible_group:
                    if node.twin() not in final_group:      #textcolor{blue}{build a 2f+1 partition where both a node and its twin will not be present simultaneously}
                        final_group.add(node)
                    if len(final_group) == 2*f+1:
                        break
                groups.append(final_group)

        # print([i for i in groups])

        if num_partitions - number_of_quorum_partitions > 0:
            possible_groups = [i for i in set_partitions(total_nodes,num_partitions-number_of_quorum_partitions)]
            print(possible_groups)   
            #textcolor{blue}{generate all possible partition combinations}
            while len(groups) < num_partitions:     #textcolor{blue}{Add a random combination to the groups, ensure it is not already present in the set.}
                groups.append(possible_groups[random.randint(0, len(possible_groups)-1)])
            gen_partitions.append(groups)
    return gen_partitions

partitions = generate_heuristic_partitions(3, [1,2,3], [4], 20, True, 42)
