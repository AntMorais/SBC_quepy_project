
"""
Aditional Questions' regex from QALD
#TODO adicionar imports ao dbpedia.dsl
"""
from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import IsMovie, NameOf, IsPerson, IsFictionalCharacter \
    DirectedBy, LabelOf, DurationOf, HasActor, HasName, ReleaseDateOf, \
    DirectorOf, StarsIn, DefinitionOf

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))



class Movie(Particle):
    regex = Question(Pos("DT")) + nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsMovie() + HasName(name)



class FictionalCharacter(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)



#Question/Regex Handler (subclass of QuestionTemplate)
class ActorPortrayedCharacter(QuestionTemplate):
    """
    Ex: "Which actor played Chewbacca?"
        "Who played Agent Smith in the Matrix?"
    """

    acted_on = (Lemma("appear") | Lemma("act") | Lemma("star") | Lemma("play") | Lemma("portray"))
    movie = (Lemma("movie") | Lemma("movies") | Lemma("film"))
    regex = (Lemma("which") + Lemma("actor") + acted_on + FictionalCharacter())
    regex = (Question(Lemma("list")) + movie + Lemma("with") + Actor()) | \
            (Question(Pos("IN")) + (Lemma("what") | Lemma("which")) +
             movie + Lemma("do") + Actor() + acted_on + Question(Pos("."))) | \
            (Question(Pos("IN")) + Lemma("which") + movie + Lemma("do") +
             Actor() + acted_on) | \
            (Question(Lemma("list")) + movie + Lemma("star") + Actor())


    #Returns the intermediate representation of the Regex
    def interpret(self, match):
        thing = match.target.tokens
        target = HasKeyword(thing)
        definition = IsDefinedIn(target)
        return definition