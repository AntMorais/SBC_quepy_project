# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Domain specific language for DBpedia quepy.
"""

from quepy.dsl import FixedType, HasKeyword, FixedRelation, FixedDataRelation

# Setup the Keywords for this application
HasKeyword.relation = "rdfs:label"
HasKeyword.language = "en"


# -----------------------------------------------ADDED---------------------------------------------------
class IsFictionalCharacter(FixedType):
    fixedtype = "dbpedia-owl:FictionalCharacter"

class IsAnimal(FixedType):
    fixedtype = "dbpedia-owl:Animal"

    

class IsMusicalWork(FixedType):
    fixedtype = "dbpedia-owl:MusicalWork"


class IsWork(FixedType):
    fixedtype = "dbpedia-owl:Work"


class IsThing(FixedType):
    fixedtype = "dbpedia-owl:Thing"



class IsCompany(FixedType):
    fixedtype = "dbpedia-owl:Company"


class IsSoftware(FixedType):
    fixedtype = "dbpedia-owl:Software"


class IsClass(FixedType):
    fixedtype = "dbpedia-owl:Class"



class IsCity(FixedType):
    fixedtype = "dbpedia-owl:City"


class StarsAs(FixedRelation):
    relation = "dbpedia-owl:portrayer"
    reverse = True

class HasNickname(FixedDataRelation):
    relation = "foaf:nick"
    language = "en"

class HasNationality(FixedRelation):
    relation = "dbpedia-owl:country"




class DeathPlaceOf(FixedRelation):
    relation = "dbpedia-owl:deathPlace"
    reverse = True


class WriterOfSong(FixedRelation):
    relation = "dbpedia-owl:writer"
    reverse = True


class Created(FixedRelation):
    relation = "dbpedia-owl:creator"
    reverse = True



class Founded(FixedRelation):
    relation = "dbpprop:founders"
    reverse = True



class CapitalOf(FixedRelation):
    relation = "dbpedia-owl:capital"
    reverse = True




class HasFoafName(FixedDataRelation):
    relation = "foaf:name"
    language = "en"



class ComposerOf(FixedRelation):
    relation = "dbpedia-owl:musicComposer"
    reverse = True

class MayorOf(FixedRelation):
    relation = "dbpedia:mayor"
    reverse = True

class LeaderOf(FixedRelation):
    relation = "dbpedia-owl:leaderName"
    reverse = True


class GovernorOf(FixedRelation):
    relation = "dbpprop:governor"
    reverse= True


class OwnerOf(FixedRelation):
    relation = "dbpprop:owner"
    reverse= True




# -----------------------------------------------ADDED---------------------------------------------------


class IsPerson(FixedType):
    fixedtype = "foaf:Person"


class IsPlace(FixedType):
    fixedtype = "dbpedia:Place"


class IsCountry(FixedType):
    fixedtype = "dbpedia-owl:Country"


class IsPopulatedPlace(FixedType):
    fixedtype = "dbpedia-owl:PopulatedPlace"


class IsBand(FixedType):
    fixedtype = "dbpedia-owl:Band"


class IsAlbum(FixedType):
    fixedtype = "dbpedia-owl:Album"


class IsTvShow(FixedType):
    fixedtype = "dbpedia-owl:TelevisionShow"


class IsMovie(FixedType):
    fixedtype = "dbpedia-owl:Film"


class HasShowName(FixedDataRelation):
    relation = "dbpprop:showName"
    language = "en"


class HasName(FixedDataRelation):
    relation = "dbpprop:name"
    language = "en"





class DefinitionOf(FixedRelation):
    relation = "rdfs:comment"
    reverse = True


class LabelOf(FixedRelation):
    relation = "rdfs:label"
    reverse = True


class UTCof(FixedRelation):
    relation = "dbpprop:utcOffset"
    reverse = True


class PresidentOf(FixedRelation):
    relation = "dbpprop:leaderTitle"
    reverse = True


class IncumbentOf(FixedRelation):
    relation = "dbpprop:incumbent"
    reverse = True


class CapitalOf(FixedRelation):
    relation = "dbpedia-owl:capital"
    reverse = True


class LanguageOf(FixedRelation):
    relation = "dbpprop:officialLanguages"
    reverse = True


class PopulationOf(FixedRelation):
    relation = "dbpprop:populationCensus"
    reverse = True


class IsMemberOf(FixedRelation):
    relation = "dbpedia-owl:bandMember"
    reverse = True


class ActiveYears(FixedRelation):
    relation = "dbpprop:yearsActive"
    reverse = True


class MusicGenreOf(FixedRelation):
    relation = "dbpedia-owl:genre"
    reverse = True


class ProducedBy(FixedRelation):
    relation = "dbpedia-owl:producer"


class BirthDateOf(FixedRelation):
    relation = "dbpprop:birthDate"
    reverse = True


class BirthPlaceOf(FixedRelation):
    relation = "dbpedia-owl:birthPlace"
    reverse = True


class ReleaseDateOf(FixedRelation):
    relation = "dbpedia-owl:releaseDate"
    reverse = True


class StarsIn(FixedRelation):
    relation = "dbpprop:starring"
    reverse = True



class NumberOfEpisodesIn(FixedRelation):
    relation = "dbpedia-owl:numberOfEpisodes"
    reverse = True


class ShowNameOf(FixedRelation):
    relation = "dbpprop:showName"
    reverse = True


class HasActor(FixedRelation):
    relation = "dbpprop:starring"


class CreatorOf(FixedRelation):
    relation = "dbpprop:creator"
    reverse = True


class NameOf(FixedRelation):
    relation = "foaf:name"
    reverse = True


class DirectedBy(FixedRelation):
    relation = "dbpedia-owl:director"


class DirectorOf(FixedRelation):
    relation = "dbpedia-owl:director"
    reverse = True


class DurationOf(FixedRelation):
    # DBpedia throws an error if the relation it's
    # dbpedia-owl:Work/runtime so we expand the prefix
    # by giving the whole URL.
    relation = "<http://dbpedia.org/ontology/Work/runtime>"
    reverse = True


class HasAuthor(FixedRelation):
    relation = "dbpedia-owl:author"


class AuthorOf(FixedRelation):
    relation = "dbpedia-owl:author"
    reverse = True


class IsBook(FixedType):
    fixedtype = "dbpedia-owl:Book"


class LocationOf(FixedRelation):
    relation = "dbpedia-owl:location"
    reverse = True
