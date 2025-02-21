import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transition_model = dict()
    random_factor = 1 - damping_factor

    for key in corpus.keys():
        transition_model[key] = 0

    if corpus[page] == None:
        for key in transition_model.keys():
            transition_model[key] += 1/len(list(corpus.keys()))
        return transition_model
    else:
        for key in transition_model.keys():
            transition_model[key] += random_factor/len(list(corpus.keys()))
        if len(corpus[page]) != 0:
            damping_prob = damping_factor/len(corpus[page])
        else:
            damping_prob = damping_factor/len(corpus.keys())
        for value in list(corpus[page]):
            if value not in transition_model.keys():
                transition_model[value] = 0
            transition_model[value] += damping_prob

        return transition_model
            


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict = dict()
    i = 0
    page = random.choice(list(corpus.keys()))
    pagerank_dict[page] =1
    while i<n:
        weights = [transition_model(corpus, page, damping_factor)[key] for key in transition_model(corpus, page, damping_factor).keys()]
        link = random.choices(list(corpus.keys()), weights=weights,k=1)[0]
        if link not in pagerank_dict.keys():
            pagerank_dict[link] = 1
        else:
            pagerank_dict[link] += 1
        page = link
        i+= 1
    for key in pagerank_dict.keys():
        pagerank_dict[key] = pagerank_dict[key]/n
    return pagerank_dict

def has_converge(rank, new_rank, tolerance):
    for key in rank.keys():
        if abs(rank[key] - new_rank[key])>tolerance:
            return False
    return True

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict = dict()
    for key in corpus.keys():
        pagerank_dict[key] = 1/len(list(corpus.keys()))
    
    while True:
        new_rank = dict()
        for child in corpus.keys():
            new_rank[child] = (1-damping_factor)/len(list(corpus.keys()))
            parent_sum_prob = 0

            empty = True
            for parent in corpus.keys():
                if child in corpus[parent]:
                    parent_sum_prob += pagerank_dict[parent] / len(list(corpus[parent]))
                    empty = False

            if empty:
                for parent in corpus.keys():
                    parent_sum_prob += pagerank_dict[parent] / len(list(corpus.keys()))
            new_rank[child] += damping_factor*parent_sum_prob
        
        if has_converge(pagerank_dict, new_rank, 0.001):
            break

        pagerank_dict = new_rank
    
    return pagerank_dict
    


if __name__ == "__main__":
    main()
