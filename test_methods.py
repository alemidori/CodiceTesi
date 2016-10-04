import lcs
import relations
import graph_relations

#coerente > 10
food_list10 = ['water', 'mellon', 'apple', 'pizza', 'chips', 'meat', 'chicken', 'potato', 'milk', 'chocolate']

#coerente > 50
food_list50 = ['water', 'mellon', 'apple', 'pizza', 'chips', 'meat', 'chicken', 'potato', 'milk', 'chocolate',
               'seafood','nuts', 'rice', 'beans', 'legume', 'tofu', 'yogurt', 'cheese', 'bread', 'pasta',
               'cake', 'noodles', 'beef', 'beer', 'vegetables', 'pie', 'tomato', 'mushroom', 'kebab', 'pork',
                'orange', 'lemon', 'banana', 'butter', 'oil', 'olive', 'grapes', 'plum', 'onion', 'hamburger',
               'bacon', 'steak', 'porridge', 'fish', 'chips', 'lobster', 'chips', 'candy','cream', 'soup']


#coerente > 2
electronics_list2 = ['phone', 'computer']

#non coerente > 5
mix5 = ['chocolate', 'phone', 'politician', 'new jersey', 'show']

#non coerente > 20
mix20 = ['baker', 'mechanician', 'worker', 'clerk', 'politician', 'pilot', 'school', 'university', 'academy', 'exam',
         'teacher', 'student', 'master', 'rejection', 'sadness', 'disappointment', 'anger', 'take',  'table',  'every',
         'time', 'watch', 'tablet', 'camera', 'console', 'exam', 'pizza', 'chips', 'tofu', 'yogurt', 'cheese', 'bread',
         'room', 'one', 'vegas', 'water', 'mellon', 'apple', 'sunshine', 'sun', 'moon', 'heart', 'earth']

#astratta coerente > 9
sentiment_list9 = ['love', 'friendship', 'sadness', 'disappointment', 'anger', 'consolation', 'deception', 'betrayal',
                  'fraternity']

#astratta non coerente > 5
abstract = ['love', 'immeasurable', 'power', 'straight', 'hystory']

#solo termine
solo = ['table']

#family coerente > 10
family = ['sister', 'mother', 'father', 'son', 'daughter', 'uncle', 'aunt', 'brother', 'grandmother', 'grandfather']

#semi coerente > 10 - c'e' solo un elemento estraneo nella lista
food_with_outsider10 = ['mellon', 'apple', 'pizza', 'chips', 'meat', 'chicken','potato', 'milk', 'camera']

#semi coerente > 3
food_with_outsider3 = ['mellon', 'apple', 'exam']


jobs_list = ['baker', 'mechanician', 'worker', 'clerk', 'politician', 'pilot']
school_list = ['school', 'university', 'academy', 'exam', 'teacher', 'student', 'master', 'rejection']

mix = ['water', 'mellon', 'apple', 'school', 'university', 'academy', 'exam', 'pizza', 'chips', 'meat', 'chicken',
       'potato', 'milk', 'chocolate', 'phone', 'computer', 'watch', 'tablet', 'camera', 'console']

example_list = ['developer', 'web', 'software', 'politician', 'diiner', 'chinese', 'new jersey']

a = ['take',  'table',  'every', 'time', 'show', 'room', 'one', 'vegas', 'place', 'bar']

topic_exemple = ['love', 'enjoyed',  'perfect', 'hotel', 'dont' 'one', 'place view']

#print(lcs.process(example_list)) #test lcs
#print(relations.process(mix20)) #test relations

#per liste molto lunghe nel graph_relations e' bene aumentare leggermente il parametro della similarita' per
#ridurre il numero di termini in output e quindi prendere un gruppo minore di nodi del grafo
print(graph_relations.process(mix20, 0.2)) #test graph_relations

