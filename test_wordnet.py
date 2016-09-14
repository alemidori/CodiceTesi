import wordnet

#coerente > 10
food_list10 = ['water', 'mellon', 'apple', 'pizza', 'chips', 'meat', 'chicken', 'potato', 'milk', 'chocolate']

#coerente > 50
food_list50 = ['water', 'mellon', 'apple', 'pizza', 'chips', 'meat', 'chicken', 'potato', 'milk', 'chocolate',
               'seafood','nuts', 'rice', 'beans', 'legume', 'tofu', 'yogurt', 'cheese', 'bread', 'pasta',
               'cake', 'noodles', 'beef', 'beer', 'vegetables', 'pie', 'tomato', 'mushroom', 'kebab', 'pork',
                'orange', 'lemon', 'banana', 'butter', 'oil', 'olive', 'grapes', 'plum', 'onion', 'hamburger',
               'bacon', 'steak', 'porridge', 'fish', 'chips', 'lobster', 'chips', 'candy','cream', 'soup']

#coerente > 2
electronics_list2 = ['phone', 'computer', 'apple']

#astratta > 9
sentiment_list9 = ['love', 'friendship', 'sadness', 'disappointment', 'anger', 'consolation', 'deception', 'betrayal',
                  'fraternity']


jobs_list = ['baker', 'mechanician', 'worker', 'clerk', 'politician', 'pilot']
school_list = ['school', 'university', 'academy', 'exam', 'teacher', 'student', 'master', 'rejection']

mix = ['water', 'mellon', 'apple', 'school', 'university', 'academy', 'exam', 'pizza', 'chips', 'meat', 'chicken',
       'potato', 'milk', 'chocolate', 'phone', 'computer', 'watch', 'tablet', 'camera', 'console']

example_list = ['developer', 'web', 'software', 'politician', 'diiner', 'chinese', 'new jersey']

a = ['take',  'table',  'every', 'time', 'show', 'room', 'one', 'vegas', 'place', 'bar']


print(wordnet.process(food_list10))
