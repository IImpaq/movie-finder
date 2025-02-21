from recommender import MovieRecommender
from inputTypes import GetMovieRecommendationsInput, GetMovieDescriptionInput
from subtitles import initializeOpensubtitles, downloadAndSaveSubtitle, checkSubtitleFile, summarizeSubtitles, extractKeyThemes

recommender = MovieRecommender("../data/movies_dataset_preprocessed.csv")

def proceedAvailableGenres():
    genres = []

    for i in range(len(recommender.dataset)):
        temp = recommender.dataset["genres"][i].split("-")
        for genre in temp:
            if genre not in genres:
                genres.append(genre)

    return genres


def proceedAvailableLanguages():
    language_counts = {}

    for i in range(len(recommender.dataset)):
        lang = recommender.dataset["original_language"][i]
        language_counts[lang] = language_counts.get(lang, 0) + 1

    sorted_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
    languages = [language for language, _ in sorted_languages]

    return languages

def proceedMovieRecommendation(input: GetMovieRecommendationsInput):
    print(f"Generating recommendation for: {input}")

    recommendations = recommender.get_movies(input)
    # Cleaning entires from recommendations which are only used for evaluation
    result = []
    for recommendation in recommendations:
        result.append({
          "title": recommendation["title"],
          "genre": recommendation["genre"],
          "rating": recommendation["rating"],
          "year": recommendation["year"],
          "poster": recommendation["poster"],
          "confidence": recommendation["confidence"]
        })

    print(f"Generated recommendations: {recommendations}")
    return result


def proceedMovieDescription(input: GetMovieDescriptionInput):
    print(input)

    movie_name = f"{input.year} - {input.title}"
    language = "en"                                             # TODO: Summarys in different languages?

    # Due to the API limit subtitles will be downloaded
    cleaned_subtitles = checkSubtitleFile(movie_name)

    if cleaned_subtitles == None:
        ost = initializeOpensubtitles()                         # TODO: Exception handling when API limit is reached
        cleaned_subtitles = downloadAndSaveSubtitle(ost, movie_name, language)

    summarized_description = summarizeSubtitles(cleaned_subtitles)

    key_themes = extractKeyThemes(cleaned_subtitles, 3)

    print("Summary: " + summarized_description)
    description = {
        "genre": key_themes,
        "summary": summarized_description
        }

    return description
