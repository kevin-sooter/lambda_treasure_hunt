## Project week proposal:

Create a large world, LambdaMUD style that can be traversed using REST move commands
  ~2000 rooms

Server enforces that players can only move once every 10 seconds, otherwise will incur a penalty


{"room_id": 1, "exits": {n": {"room_id": 2}, "w": {"room_id": 3}}


Phase 1: Exploration

  Students will automate exploration to traverse the world and build a map. Recommend to save in JSON via local storage?

Phase 2: Map building
  Generate a graphical representation of the world map. PMs will award prizes to the best maps in their group

Phase 3: Treasure hunting
  Students will receive clues in the form of algorithm puzzles. The answer to the puzzles will be an integer representing the room_id where their treasure is located, which they should be able to navigate to based on their map. Once in the correct room, they will have to "dig" some number of times to retrieve the treasure. (dig is a REST call that can only be called once every 10 seconds)

```
int_list = [93, 68, 70, 72, 70, 89, 44, 59, 78, 5, 74, 78, 91, 99, 9, 1, 91, 8, 15, 73, 41, 51, 2, 96, 32, 40, 5, 3, 22, 16, 17, 61, 77, 17, 6, 27, 89, 37, 65, 99, 63, 34, 83, 21, 38, 34, 55, 39, 88, 90, 25, 37, 95, 79, 27, 25, 43, 64, 63, 78, 54, 7, 36, 53, 16, 56, 66, 10, 40, 63, 51, 55, 11, 45, 69, 9, 78, 43, 66, 44, 67, 52, 37, 66, 93, 29, 47, 50, 7, 15, 44, 2, 88, 97, 41, 14, 70, 22, 19, 48]

# IMPLEMENT
def longest_subsequence(l):
    """
    Return the length of the longest subsequence
    of the given list such that all elements of
    the subsequence are sorted in increasing order.
    """
    pass

print( f"Your treasure is in room: {longest_subsequence(int_list)" )
```

curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "password":"testpassword"}' localhost:8000/api/login/

curl -X GET -H 'Authorization: Token 547ab6e88f192b85f52157827b957eaf62645732' localhost:8000/api/adv/init/


curl -X POST -H 'Authorization: Token 547ab6e88f192b85f52157827b957eaf62645732' -H "Content-Type: application/json" -d '{"direction":"n"}' localhost:8000/api/adv/move/

curl -X POST -H 'Authorization: Token 547ab6e88f192b85f52157827b957eaf62645732' -H "Content-Type: application/json" -d '{"direction":"s"}' localhost:8000/api/adv/move/

curl -X POST -H 'Authorization: Token 547ab6e88f192b85f52157827b957eaf62645732' -H "Content-Type: application/json" -d '{"direction":"n", "next_room_id":1}' localhost:8000/api/adv/move/



curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "password":"testpassword"}' https://lambda-treasure-hunt.herokuapp.com/api/login/

curl -X POST -H 'Authorization: Token 547ab6e88f192b85f52157827b957eaf62645732' -H "Content-Type: application/json" -d '{"name":"treasure"}' localhost:8000/api/adv/take/

curl -X POST -H 'Authorization: Token 547ab6e88f192b85f52157827b957eaf62645732' -H "Content-Type: application/json" -d '{"name":"treasure"}' localhost:8000/api/adv/drop/

curl -X POST -H 'Authorization: Token 547ab6e88f192b85f52157827b957eaf62645732' -H "Content-Type: application/json" localhost:8000/api/adv/status/

curl -X POST -H 'Authorization: Token 547ab6e88f192b85f52157827b957eaf62645732' -H "Content-Type: application/json" -d '{"name":"treasure"}' localhost:8000/api/adv/sell/


curl -X POST -H 'Authorization: Token 547ab6e88f192b85f52157827b957eaf62645732' -H "Content-Type: application/json" -d '{"name":"treasure", "confirm":"yes"}' localhost:8000/api/adv/sell/
