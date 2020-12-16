
"""
Aditional Questions' regex from QALD
"""

from refo import Plus, Question, Group
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle, Token
from dsl import *
nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS") | Pos("CC"))



class Movie(Particle):
    regex = Question(Pos("DT")) + nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsMovie() + HasFoafName(name)






#-------------------------------------------ADDED PARTICLES-------------------------------------------------------------------------


class FictionalCharacter(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsFictionalCharacter() + HasKeyword(name)



class Nationality(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return HasKeyword(name)


class Thing(Particle):
    regex =  nouns

    def interpret(self, match):
        return HasKeyword(match.words.tokens.title())




class Company(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens
        return IsCompany() + HasKeyword(name)




class Classe(Particle):
    regex = Question(Pos("JJ")) + (Pos("NN") | Pos("NNP") | Pos("NNS")) |\
            Pos("VBN")

    def interpret(self, match):
        return IsClass() + HasKeyword(match.words.tokens)




class MusicalWork(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsMusicalWork() + HasKeyword(name)




class PopulatedPlace(Particle):
    regex = Plus( Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsPopulatedPlace() + HasKeyword(name)



#-------------------------------------PARTICLES FROM OTHER FILES-------------------------------------------------------------------

class Person(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS") )
    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)



class Book(Particle):
    regex = Plus(nouns)

    def interpret(self, match):
        name = match.words.tokens
        return IsBook() + HasKeyword(name)





#-------------------------------------------ADDED CLASSES-------------------------------------------------------------------------

#Question/Regex Handler (subclass of QuestionTemplate)

class ActorPortrayedCharacter(QuestionTemplate):
    """
    Ex: "Which actor played Chewbacca?"
        "Who played Agent Smith in the Matrix?"
    """

    acted = (Lemma("appear") | Lemma("act") | Lemma("star") | \
            Lemma("play") | Lemma("portray"))
    regex = (Lemma("which") + (Lemma("actor") | Lemma("actress")) \
            + acted + Person() + Question(Pos(".")))

    def interpret(self, match):
        actor = IsPerson() + StarsAs(match.person)
        actor_name = NameOf(actor)
        return actor_name, "enum"
        
        


class WhoCreatedX(QuestionTemplate):
    
    #Ex: "Who created Batman?"
    #thing = Group(Plus(Pos("IN") | Pos("NP") | Pos("NNP") | Pos("NNPS") | Lemma("-")),"thing")
    regex = (Lemma("who") + Lemma("create")  + Thing() +  Question(Pos(".")))
    #Returns the intermediate representation of the Regex
    def interpret(self, match):
        creator = IsPerson() + Created(match.thing)
        creator_name = NameOf(creator)
        return creator_name, "enum"


class WhoFoundedCompany(QuestionTemplate):
    
    #Ex: "Who founded Intel?"
    
    regex = (Lemma("who") + Lemma("found")  + Company() +  Question(Pos(".")))
    #Returns the intermediate representation of the Regex
    def interpret(self, match):
        creator = IsPerson() + Founded(match.company)
        creator_name = NameOf(creator)
        return creator_name, "enum"

        



class WhoIsGovernorOf(QuestionTemplate):
    """
    Ex: "Who is the governor of Wyoming?
    """
    regex = (Lemma("who") + Lemma("be")  + Pos("DT") + Lemma("governor") + Pos("IN") + PopulatedPlace() +  Question(Pos(".")))
    #Returns the intermediate representation of the Regex
    def interpret(self, match):
        creator_name = GovernorOf(match.populatedplace)
        return creator_name, "enum"


class WhoIsOwnerOf(QuestionTemplate):
    """
    Ex: "Who is the owner of Facebook?
    """
    regex = (Lemma("who") + Lemma("be")  + Pos("DT") + Lemma("owner") + Pos("IN") + Thing() +  Question(Pos(".")))
    #Returns the intermediate representation of the Regex
    def interpret(self, match):
        owner_name = OwnerOf(match.thing)
        return owner_name, "enum"



class WhoWroteTheSong(QuestionTemplate):
    """
    Ex: "who wrote the song Hotel California?"

    """
    regex = (Lemmas("who write") + Pos("DT") + Lemma("song") + MusicalWork() + Question(Pos(".")))

    def interpret(self, match):
        author = NameOf(IsPerson() + WriterOfSong(match.musicalwork))
        return author, "enum"



class WhereDidXDie(QuestionTemplate):
    """
    Ex: "Where did John Lennon die?"

    """

    regex = ((Lemma("where") | (Pos("IN") + Lemma("which") + Lemma("city")))+  Lemma("do") + Person() + Lemma("die") + Question(Pos(".")))
    
    def interpret(self, match):
        death_place =  DeathPlaceOf(match.person)
        death_place_name = LabelOf(death_place)
        return death_place_name, "enum"




class WhoIsCalled(QuestionTemplate):
    #Ex: "Who was called Frank The Tank?"
    #	 "Who was called Rodzilla?"
    nickname = Group(nouns, "nickname")
    regex = (Lemma("who") + Lemma("be") + Lemma("call") + nickname + Question(Pos(".")))

    def interpret(self, match):
        person = IsPerson() + HasNickname(match.nickname.tokens)        
        name = NameOf(person)
        return name, "enum"




class WhoComposedMusicFor(QuestionTemplate):
    """
    Ex: "Who composed the music for Harold and Maude?"
    """

    regex = (Lemma("who") + Lemma("compose") + Pos("DT") + Lemma("music") + Pos("IN") + Movie() + Question(Pos(".")))
    
    def interpret(self, match):
        composer = IsPerson() + ComposerOf(match.movie)
        composer_name = NameOf(composer)
        return composer_name, "enum"




class WhoIsMayorOf(QuestionTemplate):
    
    #Ex: "Who is the mayor of Tel Aviv?
    
    regex = (  Lemma("who") + Lemma("be")  + Pos("DT") + Lemma("mayor") + Pos("IN") + PopulatedPlace() +  Question(Pos(".")))
    #Returns the intermediate representation of the Regex
    def interpret(self, match):
        creator = IsPerson() + LeaderOf(match.populatedplace)
        creator_name = NameOf(creator)
        return creator_name, "enum"