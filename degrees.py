import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

### UNOPTIMIZED INEFFICIENT CODE VERSION-1.0
def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO 
    person = Node(state=source, parent=None, action=None)

    # Target person id
    goal_state = target

    # frontier teyar krno
    frontier = QueueFrontier()

    # frontier m first node add krno
    frontier.add(person)

    # explored stars go track rakhan bi explored set
    explored = set()


    # loop to find the target person
    while True:
        if frontier.empty():
            return None
        
        # removing a node for inspection or say search
        removed_node = frontier.remove()

        # as we found the star, our goal, time to return how many steps it takes and how he/she is connected to the source star
        # return number + list of movie steps
        if removed_node.state == goal_state:
            steps = []
            while removed_node.parent is not None:
                steps.append((removed_node.action, removed_node.state))
                removed_node = removed_node.parent
            steps.reverse()
            # print(f"so it takes ::: {len(steps)} ::: to reach {target}")
            return steps

        
        # now this is not the target so we will first put him to the explore set then next we will see all other related to him
        explored.add(removed_node)

        # now time to add all connected to him except its parent to the frontier for exploration
        all_actions = neighbors_for_person(removed_node.state)
        all_actions = sorted(all_actions)


        # here action stands for movie and state stands for person
        for action, state in all_actions:
            # checking if this state/person is in frontier or not, or not in explored set. If not then we can add it in frontier
            if state == goal_state:
                goal_node = Node(state=state, parent=removed_node, action=action)
                steps = []
                while goal_node.parent is not None:
                    steps.append((goal_node.action, goal_node.state))
                    goal_node = goal_node.parent
                steps.reverse()
                # print(f"so it takes ::: {len(steps)} ::: to reach {target}")
                return steps
            elif state not in explored and not frontier.contains_state(state):
                child = Node(state=state, parent=removed_node, action=action)
                frontier.add(child)

    # raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
