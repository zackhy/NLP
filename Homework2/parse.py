import sys
from nltk.tag import mapping
from providedcode.dependencygraph import DependencyGraph
from providedcode.transitionparser import TransitionParser

if __name__ == '__main__':
    data = sys.stdin.read()
    infile = sys.argv[1]
    sentence_list = data.split('\n')
    depgraphs = []
    for sent in sentence_list:
        depgraph = DependencyGraph.from_sentence(sent)

        for node in depgraph.nodes:
            tag = depgraph.nodes[node]['tag']
            ctag = mapping.map_tag('wsj', 'universal', tag)
            depgraph.nodes[node]['ctag'] = ctag

        depgraphs.append(depgraph)

    tp = TransitionParser.load(infile)
    parsed = tp.parse(depgraphs)

    for p in parsed:
        print p.to_conll(10).encode('utf-8')




