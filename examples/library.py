from plex import Plex
from plex_database.library import Library
from plex_database.matcher import Matcher
from plex_database.models import LibrarySection, LibrarySectionType

from stash import Stash
import logging
import os
import sys
import time

# Build caches
cache_dir = os.path.abspath('cache')
matcher_cache = Stash('apsw:///cache.db?table=matcher', 'lru:///?capacity=500&compact_threshold=1500', 'msgpack:///')


def fetch_movies(library):
    movies = {}

    # Retrieve movie sections
    sections = library.sections(LibrarySectionType.Movie, LibrarySection.id).tuples()

    # Fetch movies with account settings
    elapsed, items = measure(library.movies.mapped, sections, account=1, parse_guid=True)
    print 'Library.movies.mapped() - elapsed: %2dms' % (elapsed * 1000)

    for _, guid, settings in items:
        key = (guid.agent, guid.sid)

        if key not in movies:
            movies[key] = []

        movies[key].append(settings)

    print 'len(movies): %r' % len(movies)
    return movies


def fetch_shows(library):
    shows = {}

    # Fetch show sections
    sections = library.sections(LibrarySectionType.Show, LibrarySection.id).tuples()

    # Fetch episodes (with show/season parents)
    elapsed, (show_items, season_items, episode_items) = measure(library.episodes.mapped, sections, account=1, parse_guid=True)
    print 'Library.episodes.with_parents() - elapsed: %2dms' % (elapsed * 1000)

    # Iterate over items, merge them into `shows and `seasons` dictionaries
    for ids, guid, (season_num, episode_num), settings in episode_items:
        if ids['#'] % 100 == 0:
            sys.stdout.write('.')

        show_key = (guid.agent, guid.sid)

        # Ensure show exists
        if show_key not in shows:
            shows[show_key] = {}

        # Ensure episode exists
        episode_key = (season_num, episode_num)

        if episode_key not in shows[show_key]:
            shows[show_key][episode_key] = []

        # Append episode `settings` into dictionary
        shows[show_key][episode_key].append(settings)

    print 'len(shows): %r' % len(shows)
    return shows


def measure(func, *args, **kwargs):
    started = time.time()

    result = func(*args, **kwargs)

    return time.time() - started, result


def test(func, repeat=10, *args, **kwargs):
    t_elapsed = []

    print 'test(%r, %r)' % (func, repeat)

    for x in range(repeat):
        with Plex.configuration.cache(matcher=matcher_cache):
            # Measure task
            elapsed, items = measure(func, *args, **kwargs)

        print "----------------------- %2dms ----------------------------" % (elapsed * 1000)
        t_elapsed.append(elapsed)

        time.sleep(1)

    # Calculate test statistics
    t_min = min(t_elapsed) * 1000
    t_max = max(t_elapsed) * 1000
    t_avg = (sum(t_elapsed) / len(t_elapsed)) * 1000

    print '] min: %2dms, max: %2dms, avg: %2dms' % (t_min, t_max, t_avg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    repeat = int(raw_input('Repeat [10]: ') or 10)

    raw_input('[start (repeat: %r)]' % repeat)

    # Initialize library/matcher
    matcher = Matcher(matcher_cache, Plex.client)
    library = Library(matcher)

    # Fetch movies
    test(fetch_movies, repeat, library=library)

    print
    print "=========================================================="
    print

    # Fetch shows
    test(fetch_shows, repeat, library=library)

    # Flush caches
    matcher_cache.flush()
