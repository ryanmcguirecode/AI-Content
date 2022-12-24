import random
# from moviepy.editor import *

story_subjects = ['monkeys', 'men', 'mice', 'wolves', 'elves', 'goblins', 'dwarves', 'orcs', 'trolls', 'golems',
'gargoyles', 'dragons', 'gods', 'demons', 'angels', 'ghosts', 'spirits', 'witches', 'warlocks', 'wizards', 
'sorcerers', 'sorceresses', 'necromancers', 'necromanceresses', 'vampires', 'werewolves', 'zombies',
'men', 'mice', 'wolves', 'elves', 'goblins', 'dwarves', 'orcs', 'trolls', 'golems', 'gargoyles', 
'dragons', 'gods', 'demons', 'angels', 'ghosts', 'spirits', 'switches', 'warlocks', 'wizards', 
'sorcerers', 'sorceresses', ]

adjectives = ['sleepy', 'weird', 'crazy', 'goofy', 'ghoulish', 'zany', 'serious', 'mysterious', 'fun', 'wild']

story_types = ['story', 'tale', 'fable', 'legend', 'myth', 'epic', 'poem', 'haiku', 'ballad', 'ode', 
'rhyme', 'riddle', 'proverb', 'fairy tale', 'folk tale', 'narrative', 'narrative poem', 'narrative rhyme',
'narrative riddle', 'narrative proverb', 'narrative fairy tale', 'narrative folk tale', 'narrative epic', 'narrative ballad', 
'narrative ode', 'narrative haiku', 'narrative myth', 'narrative legend', 'narrative fable', 'narrative tale', 'narrative story', 
'political story']

story_settings = ['city', 'jungle', 'village', 'mountains', 'clouds', 'swamp', 'forest', 'desert', 
'ocean', 'sea', 'river', 'lake', 'pond', 'cave', 'cavern', 'canyon', 'valley', 'plain', 'meadow', 
'field', 'farm', 'town', 'village', 'city', 'castle', 'palace', 'fortress', 'fort', 'keep', 'dungeon',
'tower', 'temple', 'church', 'cathedral', 'mosque', 'synagogue', 'shrine', 'monastery', 'abbey', 'school',
'university', 'college', 'library', 'museum', 'zoo', 'aquarium', 'amusement park', 'theme park', 'park', 
'garden', 'cemetery', 'graveyard', 'forest', 'jungle', 'swamp', 'mountains', 'clouds', 'desert', 'ocean', 
'sea', 'river', 'lake', 'pond', 'cave', 'cavern', 'canyon', 'valley', 'plain', 'meadow', 'field', 'farm', 
'town', 'village', 'city', 'castle', 'palace', 'fortress', 'fort', 'keep', 'dungeon', 'tower', 'temple', 'church', 
'cathedral', 'mosque', 'synagogue', 'shrine', 'monastery', 'abbey', 'school', 'university', 'college', 'library',
'museum', 'zoo', 'aquarium', 'amusement park', 'theme park', 'park', 'garden', 'cemetery', 'graveyard']

art_style = ['cartoon', 'cyberpunk', 'steampunk', 'black and white', 'color', 'grayscale', 'monochrome', 'sepia', 
'pastel', 'watercolor', 'oil painting', 'acrylic painting', 'charcoal drawing', 'pencil drawing', 'ink drawing', 
'sketch', 'sketchy', 'stylized', 'stylized cartoon', 'stylized cyberpunk', 'stylized steampunk', 'stylized black and white', 
'stylized color', 'stylized grayscale', 'stylized monochrome', 'stylized sepia', 'stylized pastel', 'stylized watercolor', 
'stylized oil painting', 'stylized acrylic painting', 'stylized charcoal drawing', 'stylized pencil drawing', 'stylized ink drawing',
 'stylized sketch', 'stylized sketchy']

class Prompt:
    def __init__(self, story_type, adjective, story_setting, story_subject):
        self.story_type = story_type
        self.adjective = adjective
        self.story_setting = story_setting
        self.story_subject = story_subject
        self.prompt = 'Write a ' + story_type + ' about ' + adjective + ' ' + story_subject + ' in a ' + story_setting + '.'

# Returns the content for story generation
def get_content():
    return Prompt(random.choice(story_types), random.choice(adjectives), random.choice(story_settings), random.choice(story_subjects))

# Returns the art style for the video
def get_art_style():
    return random.choice(art_style)