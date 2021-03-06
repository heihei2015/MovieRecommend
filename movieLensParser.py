from DataService import Mongo
import pymongo
import time
import movieLensRatings
import movieLensLinks
import movieLensMovies
import movieLensTags
import movieLensMoviesPopularity
import movieLensRelevance
import movieLensGenres
import movieLensToIMDB

def parse(mongo):
    print("[movieLensParser] Starting parse MovieLens database...")
    startTime = time.time()

    # Add all user ratings into database.
    # runtime: (172.95s)
    movieLensRatings.parse(mongo)
    mongo.db["user_rate"].create_index([("uid", pymongo.ASCENDING)])
    print("[movieLensParser] Created index for uid in user_rate")

    # Add movie id and imdb id pair into database.
    # runtime: (0.93s)
    movieLensLinks.parse(mongo)
    mongo.db["movie"].create_index([("mid", pymongo.ASCENDING)])
    print("[movieLensParser] Created index for mid in movie")
    mongo.db["movie"].create_index([("title", pymongo.ASCENDING)])
    print("[movieLensParser] Created index for title in movie")

    # Add movie titles into database.
    # runtime: (3.15s)
    movieLensMovies.parse(mongo)

    # not needed anymore, retrieved complete info from IMDB now
    # # Add movie genres into database.
    # # runtime: (4.11s)
    # movieLensGenres.parse(mongo)

    # Add tags into database.
    # runtime: (0.06s)
    movieLensTags.parse(mongo)
    mongo.db["tag"].create_index([("tid", pymongo.ASCENDING)])
    print("[movieLensParser] Created index for tid in tag")
    mongo.db["tag"].create_index([("content", pymongo.ASCENDING)])
    print("[movieLensParser] Created index for content in tag")

    # Add movies popularity into database.
    # runtime: (0.83s)
    movieLensMoviesPopularity.parse(mongo)

    # Add tag relevance into database.
    # runtime: (509.09s)
    movieLensRelevance.parse(mongo)

    # Add more movie info into database.
    # runtime: (roughly one hour)
    movieLensToIMDB.retrieve(mongo)
    
    print("[movieLensParser] Parse done (%0.2fs)." % (time.time() - startTime))


def main():
    mongo = Mongo("movieRecommend")
    parse(mongo)

if __name__ == "__main__":
    main()