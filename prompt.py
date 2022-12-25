import random
from constants import MAX_GPT_WORDS

story_subjects = ['monkeys', 'men', 'mice', 'wolves', 'elves', 'goblins', 'dwarves', 'orcs', 'trolls', 'golems',
'gargoyles', 'dragons', 'gods', 'demons', 'angels', 'ghosts', 'spirits', 'witches', 'warlocks', 'wizards', 
'sorcerers', 'sorceresses', 'necromancers', 'necromanceresses', 'vampires', 'werewolves', 'zombies',
'men', 'mice', 'wolves', 'elves', 'goblins', 'dwarves', 'orcs', 'trolls', 'golems', 'gargoyles', 
'dragons', 'gods', 'demons', 'angels', 'ghosts', 'spirits', 'switches', 'warlocks', 'wizards', 
'sorcerers', 'sorceresses']

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

class StoryPrompt:
    def __init__(self, category, subject=None, setting=None):
        self.category = category
        self.subject = subject
        self.setting = setting
        if self.subject and self.setting:
            self.text = 'Write a ' + category + ' about ' + subject + ' in a ' + setting + ' in under {0} words.'.format(MAX_GPT_WORDS)
        elif self.subject:
            self.text = 'Write a ' + category + ' about ' + subject + ' in under {0} words.'.format(MAX_GPT_WORDS)
        elif self.setting:
            self.text = 'Write a ' + category + ' set in ' + setting + ' in under {0} words.'.format(MAX_GPT_WORDS)
        else:
            self.text = 'Write a ' + category + ' in under {0} words.'.format(MAX_GPT_WORDS)
    
    def generate_image_prompt(self, text, art_style):
        """ Returns the prompt to generate image for given text in art style """
        
        if self.subject and self.setting:
            text_prompt = "{0} in {1}".format(self.subject, self.setting)
        elif self.subject:
            text_prompt = self.subject
        elif self.setting:
            text_prompt = self.setting
        else:
           text_prompt = ""
        
        if art_style:
            return text_prompt + " in style " + art_style + text
        else:
            return text_prompt + text

def random_story_prompt():
    """ Returns the content for story generation """
    
    return StoryPrompt(random.choice(story_types), random.choice(story_settings), random.choice(story_subjects))

def random_art_style():
    """ Returns the art style for the video """
    
    return random.choice(art_style)