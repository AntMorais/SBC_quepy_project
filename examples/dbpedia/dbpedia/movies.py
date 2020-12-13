# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Movie related regex.
"""

from refo import Plus, Question, Group
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle, Token
from dsl import *
"""IsMovie, NameOf, IsPerson, \
    DirectedBy, LabelOf, DurationOf, HasActor, HasName, ReleaseDateOf, \
    DirectorOf, StarsIn, DefinitionOf, StarsAs, IsFictionalCharacter,  IsThing, HasNationality, Created,\
        IsCompany, IsSoftware, IsBook, AuthorOf, IsClass, Created, CapitalOf"""

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
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS") | Pos("."))

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

    acted = (Lemma("appear") | Lemma("act") | Lemma("star") | Lemma("play") | Lemma("portray"))
    movie = (Lemma("movie") | Lemma("movies") | Lemma("film"))
    regex = (Lemma("which") + (Lemma("actor") | Lemma("actress"))  + acted + Person() + Question(Pos(".")))

    #The target variable matches \
    # a string that will be passed on to the semantics -> interpret\
    # to make part of the final query. 
    #target = Question(Pos("DT")) + Group(Pos("NN"), "target")

    #Returns the intermediate representation of the Regex
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



"""
class WhoIsMayorOfCapitalOf(QuestionTemplate):
    #Ex: "Who is the mayor of the capital of French Polynesia?
    

    regex = Lemma("what") + Token("is") + Pos("DT") + Lemma("mayor") + Pos("IN") + Pos("DT") + Lemma("capital") + Pos("IN") + \
        Question(Pos("DT")) + Thing() + Question(Pos("."))
    #Returns the intermediate representation of the Regex
    def interpret(self, match):
        capital = CapitalOf(match.thing)
        mayor = IsPerson() + MayorOf(capital)
        mayor_name = NameOf(mayor)
        return mayor_name, "enum"

"""


"""
class WhoCreatedXEncyclopedia(QuestionTemplate):
    
    #Ex: "Who created Wikipedia?
    

    regex = (Lemma("who") + (Lemma("create") | Lemma("develop"))  + Book() +  Question(Pos(".")))

    #The target variable matches \
    # a string that will be passed on to the semantics -> interpret\
    # to make part of the final query. 
    #target = Question(Pos("DT")) + Group(Pos("NN"), "target")

    #Returns the intermediate representation of the Regex
    def interpret(self, match):
        creator = IsPerson() + AuthorOf(match.book) 
        creator_name = NameOf(creator)
        return creator_name, "enum"
        
"""









#-------------------------------------------ADDED CLASSES-------------------------------------------------------------------------






class Actor(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)


class Director(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)




class ListMoviesQuestion(QuestionTemplate):
    """
    Ex: "list movies"
    """

    regex = Lemma("list") + (Lemma("movie") | Lemma("film"))

    def interpret(self, match):
        movie = IsMovie()
        name = NameOf(movie)
        return name, "enum"


class MoviesByDirectorQuestion(QuestionTemplate):
    """
    Ex: "List movies directed by Quentin Tarantino.
        "movies directed by Martin Scorsese"
        "which movies did Mel Gibson directed"
    """

    regex = (Question(Lemma("list")) + (Lemma("movie") | Lemma("film")) +
             Question(Lemma("direct")) + Lemma("by") + Director()) | \
            (Lemma("which") + (Lemma("movie") | Lemma("film")) + Lemma("do") +
             Director() + Lemma("direct") + Question(Pos(".")))

    def interpret(self, match):
        movie = IsMovie() + DirectedBy(match.director)
        movie_name = LabelOf(movie)

        return movie_name, "enum"


class MovieDurationQuestion(QuestionTemplate):
    """
    Ex: "How long is Pulp Fiction"
        "What is the duration of The Thin Red Line?"
    """

    regex = ((Lemmas("how long be") + Movie()) |
            (Lemmas("what be") + Pos("DT") + Lemma("duration") +
             Pos("IN") + Movie())) + \
            Question(Pos("."))

    def interpret(self, match):
        duration = DurationOf(match.movie)
        return duration, ("literal", "{} minutes long")


class ActedOnQuestion(QuestionTemplate):
    """
    Ex: "List movies with Hugh Laurie"
        "Movies with Matt LeBlanc"
        "In what movies did Jennifer Aniston appear?"
        "Which movies did Mel Gibson starred?"
        "Movies starring Winona Ryder"
    """

    acted_on = (Lemma("appear") | Lemma("act") | Lemma("star"))
    movie = (Lemma("movie") | Lemma("movies") | Lemma("film"))
    regex = (Question(Lemma("list")) + movie + Lemma("with") + Actor()) | \
            (Question(Pos("IN")) + (Lemma("what") | Lemma("which")) +
             movie + Lemma("do") + Actor() + acted_on + Question(Pos("."))) | \
            (Question(Pos("IN")) + Lemma("which") + movie + Lemma("do") +
             Actor() + acted_on) | \
            (Question(Lemma("list")) + movie + Lemma("star") + Actor())

    def interpret(self, match):
        movie = IsMovie() + HasActor(match.actor)
        movie_name = NameOf(movie)
        return movie_name, "enum"


class MovieReleaseDateQuestion(QuestionTemplate):
    """
    Ex: "When was The Red Thin Line released?"
        "Release date of The Empire Strikes Back"
    """

    regex = ((Lemmas("when be") + Movie() + Lemma("release")) |
            (Lemma("release") + Question(Lemma("date")) +
             Pos("IN") + Movie())) + \
            Question(Pos("."))

    def interpret(self, match):
        release_date = ReleaseDateOf(match.movie)
        return release_date, "literal"


class DirectorOfQuestion(QuestionTemplate):
    """
    Ex: "Who is the director of Big Fish?"
        "who directed Pocahontas?"
    """

    regex = ((Lemmas("who be") + Pos("DT") + Lemma("director") +
             Pos("IN") + Movie()) |
             (Lemma("who") + Lemma("direct") + Movie())) + \
            Question(Pos("."))

    def interpret(self, match):
        director = IsPerson() + DirectorOf(match.movie)
        director_name = NameOf(director)
        return director_name, "literal"


class ActorsOfQuestion(QuestionTemplate):
    """
    Ex: "who are the actors of Titanic?"
        "who acted in Alien?"
        "who starred in The Predator?"
        "Actors of Fight Club"
    """

    regex = (Lemma("who") + Question(Lemma("be") + Pos("DT")) +
             (Lemma("act") | Lemma("actor") | Lemma("star")) +
             Pos("IN") + Movie() + Question(Pos("."))) | \
            ((Lemma("actors") | Lemma("actor")) + Pos("IN") + Movie())

    def interpret(self, match):
        actor = NameOf(IsPerson() + StarsIn(match.movie))
        return actor, "enum"


class PlotOfQuestion(QuestionTemplate):
    """
    Ex: "what is Shame about?"
        "plot of Titanic"
    """

    regex = ((Lemmas("what be") + Movie() + Lemma("about")) | \
             (Question(Lemmas("what be the")) + Lemma("plot") +
              Pos("IN") + Movie())) + \
            Question(Pos("."))

    def interpret(self, match):
        definition = DefinitionOf(match.movie)
        return definition, "define"
