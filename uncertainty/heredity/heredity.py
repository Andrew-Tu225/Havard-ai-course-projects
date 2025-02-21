import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_probability = 1
    prob_dict = dict()
    #table of detail for each peron
    table = dict()
    for person in people.keys():
        gene = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = person in have_trait
        table[person] = {"gene":gene, "trait":trait}

    for person in people.keys():
        if people[person]["mother"] == None or people[person]["father"] == None:

            prob_dict[person] = PROBS["gene"][table[person]["gene"]]*PROBS["trait"][table[person]["gene"]][table[person]["trait"]]
        
        else:
            prob = 1
            father_gene = table[people[person]["father"]]["gene"]
            mother_gene = table[people[person]["mother"]]["gene"]

            father_hered_prob = .01 if father_gene==0 else 0.50 if father_gene==1 else 0.99
            mother_hered_prob = .01 if mother_gene==0 else 0.50 if mother_gene==1 else 0.99
            
            #not get gene from both father and mother
            if table[person]["gene"] == 0:
                prob *= (1-father_hered_prob)*(1-mother_hered_prob)
                trait = PROBS["trait"][table[person]["gene"]][table[person]["trait"]]
                prob *=trait
            #either from father and not mother or not father and from mother
            elif table[person]["gene"] == 1:
                prob *= father_hered_prob*(1-mother_hered_prob) + (1-father_hered_prob)*mother_hered_prob
                trait = PROBS["trait"][table[person]["gene"]][table[person]["trait"]]
                prob *=trait
            #from both father and mother
            else:
                prob *= father_hered_prob*mother_hered_prob
                trait = PROBS["trait"][table[person]["gene"]][table[person]["trait"]]
                prob*=trait

            prob_dict[person] = prob

    for person,value in prob_dict.items():
        joint_probability *= value

    return joint_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        gene = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = True if person in have_trait else False
        probabilities[person]["gene"][gene] += p
        probabilities[person]["trait"][trait] += p
    


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        gene_sum = 0
        trait_sum = 0
        for gene in probabilities[person]["gene"].keys():
            gene_sum += probabilities[person]["gene"][gene]

        for trait in probabilities[person]["trait"].keys():
            trait_sum += probabilities[person]["trait"][trait]
        
        alpha_gene = 1/gene_sum
        alpha_trait = 1/trait_sum

        for gene in probabilities[person]["gene"].keys():
            probabilities[person]["gene"][gene] = probabilities[person]["gene"][gene]*alpha_gene

        for trait in probabilities[person]["trait"].keys():
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait]*alpha_trait




if __name__ == "__main__":
    main()
