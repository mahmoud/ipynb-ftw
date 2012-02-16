# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

#
# Conway's thing to pull some stuff from SoundCloud
#

import lxml
import lxml.html
import lxml.etree

# get the raw HTML (from newegg for the first 100 laptops that are listed)
soundcloudsite = lxml.html.parse( "http://soundcloud.com/groups/top-music-players/tracks?page=1" )
lxml.html.open_in_browser( soundcloudsite )

#refers to items on soundcloud page
songs = soundcloudsite.xpath( '//*[@class="player"]' )

#name of song
name_text = []
for song in songs:
    name = song.xpath( '*[@class="medium mode player"]/*[@class="info-header"]/h3[0]/a' )

    if len( song ) == 1:
        name_text.append( name[ 0 ].text )
    elif len( song ) == 0:
        name_text.append("0")

#genre of song
genre_text = []
for song in songs:
    genre = song.xpath( '*[@class="medium mode player"]/*[@class="actionbar"]/a' )

    if len( song ) == 1:
        genre_text.append( genre[ 0 ].text )
    elif len( song ) == 0:
        genre_text.append("0")

#number of plays of song
play_text = []
for song in songs:
    play = song.xpath( '*[@class="medium mode player"]/*[@class="info-header"]/*[@class="meta-data"]/*[@class="stats"]/*[@class="plays first"]' )
    import pdb; pdb.set_trace()
    if len( song ) == 1:
        play_text.append( play[ 0 ].text )
    elif len( song ) == 0:
        play_text.append("0")

#number of hearts of song
fav_text = []
for song in songs:
    fav = song.xpath( '*[@class="medium mode player"]/*[@class="info-header"]/*[@class="meta-data"]/*[@class="stats"]/*[@class="comments"]' )

    if len( song ) == 1:
        fav_text.append( fav[ 0 ].text )
    elif len( song ) == 0:
        fav_text.append("0")

#number of downloads of song
download_text = []
for song in songs:
    download = song.xpath( '/*[@class="medium mode player"]/*[@class="info-header"]/*[@class="meta-data"]/*[@class="stats"]/*[@class="favoritings"]' )

    if len( song ) == 1:
        download_text.append( download[ 0 ].text )
    elif len( song ) == 0:
        download_text.append("0")

#number of comments of song
comment_text = []
for song in songs:
    comment = song.xpath( '*[@class="medium mode player"]/*[@class="info-header"]/*[@class="meta-data"]/*[@class="stats"]/*[@class="downloads"]' )

    if len( song ) == 1:
        comment_text.append( comment[ 0 ].text )
    elif len( song ) == 0:
        comment_text.append("0")



# make sure the text data is in ascii format instead of unicode (why do we do this?)
name_text   = [ text.encode( 'ascii', 'ignore' ) for text in name_text ]
genre_text   = [ text.encode( 'ascii', 'ignore' ) for text in genre_text ]
play_text = [ text.encode( 'ascii', 'ignore' ) for text in play_text ]
fav_text   = [ text.encode( 'ascii', 'ignore' ) for text in fav_text ]
download_text  = [ text.encode( 'ascii', 'ignore' ) for text in download_text ]
comment_text  = [ text.encode( 'ascii', 'ignore' ) for text in comment_text ]

# zip the text lists into a tuple (define:tuple = a list/set of numbers in mathematics and computing)
tuples = zip( name_text, genre_text, play_text, fav_text, download_text, comment_text )

# write results to a TXT file (created TXT file before running script)
with open( "../raw_data.tsv", "w" ) as txt_file:
    for tuple in tuples:
        txt_file.write( "%s \t %s \t %s \t %s \t %s \t %s \n" % tuple )

