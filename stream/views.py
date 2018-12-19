from django.shortcuts import render

# Create your views here.
def movies(request):
    popular_movies_tmdb = tmdb.Movies('popular')
    popular_movies = popular_movies_tmdb.info()['results']

    upcoming_movies_tmdb = tmdb.Movies('upcoming')
    upcoming_movies = upcoming_movies_tmdb.info()['results']

    return render(request, 'movies.html', {'popular':popular_movies, 'upcoming':upcoming_movies})

def single_movie(request, movie_id):
    movies_tmdb = tmdb.Movies(movie_id)
    movies = movies_tmdb.info()
    date_created = movies['release_date']
    date_created_time_struct = time.strptime(date_created, '%Y-%m-%d')
    date_created_date = datetime.fromtimestamp(mktime(date_created_time_struct)).date()
    year = date_created_date.year
    # Get movie name and use it to pass it as an argument to the youtube api.
    movie_name = movies['original_title']
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(q=movie_name, part='id,snippet', maxResults=1).execute()
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
    return render(request, 'single_movie.html', {'movies':movies, 'year':year, 'videoId':video_id})