# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

#
# CS 171 2012 HW2 skeleton code for scraping a list of popular movies, the year they came out, and their total revenue from imdb.com
#

import lxml
import lxml.html
import lxml.etree

# get the raw HTML (from newegg for the first 100 laptops that are listed)
neweggsite = lxml.html.parse( "http://www.newegg.com/Store/SubCategory.aspx?SubCategory=32&name=Laptops-Notebooks&Pagesize=100" )
#lxml.html.open_in_browser( neweggsite )

#refers to items
items = neweggsite.xpath( '//*[@class="itemCell featuredProduct"] | //*[@class="itemCell"]' )

# price of laptop
#prices = item.xpath()
price_text = []
for item in items:
    price = item.xpath( '*[@class="itemGraphics"]/*[@class="itemBrand"]/img' )

    # if there is no HTML node at the XPath we requested
    if len( price ) == 0:
        price_text.append( "no price information" )

    # if there is is an HTML node at the XPath we requested, then get it's title attribute
    elif len( price ) == 1:
        price_text.append( price[ 0 ].attrib[ "title" ] )

    else:
        print "should never be here.price"

# average customer ratings
#averageratings = item.xpath()
averageratings_text = []
for item in items:
    averageratings = item.xpath( '*[@class="itemGraphics"]/*[@class="itemBrand"]/img' )

    # if there is no HTML node at the XPath we requested
    if len( averageratings ) == 0:
        averageratings_text.append( "no average rating information" )

    # if there is is an HTML node at the XPath we requested, then get it's title attribute
    elif len( averageratings ) == 1:
        averageratings_text.append( brand[ 0 ].attrib[ "title" ] )

    else:
        print "should never be here.averageratings"

# number of customer ratings
#numberofratings = item.xpath( '//*[@class="itemCell featuredProduct"] | //*[@class="itemCell"]' )
numberofratings_text = []
for item in items:
    numberofratings = item.xpath( '*[@class="itemGraphics"]/*[@class="itemBrand"]/img' )

    # if there is no HTML node at the XPath we requested
    if len( numberofratings ) == 0:
        numberofratings_text.append( "no rating information information" )

    # if there is is an HTML node at the XPath we requested, then get it's title attribute
    elif len( numberofratings ) == 1:
        numberofratings_text.append( numberofratings[ 0 ].attrib[ "title" ] )

    else:
        print "should never be here.numberofratings"

# model name
#models = item.xpath( '//*[@class="itemCell featuredProduct"] | //*[@class="itemCell"]' )
model_text = []
for item in items:
    model = item.xpath( '*[@class="itemGraphics"]/*[@class="itemBrand"]/img' )

    # if there is no HTML node at the XPath we requested
    if len( model ) == 0:
        model_text.append( "no model information" )

    # if there is is an HTML node at the XPath we requested, then get it's title attribute
    elif len( model ) == 1:
        model_text.append( brand[ 0 ].attrib[ "title" ] )

    else:
        print "should never be here. model"

# computer brand
#brands = item.xpath( '//*[@class="itemCell featuredProduct"] | //*[@class="itemCell"]' )
brand_text = []
for item in items:
    brand = item.xpath( '*[@class="itemGraphics"]/*[@class="itemBrand"]/img' )

    # if there is no HTML node at the XPath we requested
    if len( brand ) == 0:
        brand_text.append( "no brand information" )

    # if there is is an HTML node at the XPath we requested, then get it's title attribute
    elif len( brand ) == 1:
        brand_text.append( brand[ 0 ].attrib[ "title" ] )

    else:
        print "should never be here.brand"

# make new lists with text from each node (xpath items)
price_text   = [ price.text   for price   in prices ]
averagerating_text   = [ averagerating.text   for averagerating   in averageratings ]
numberofratings_text   = [ numberofratings.text   for numberofratings   in numberofratingss ]
model_text   = [ model.text   for model  in models ]
brand_text   = [ brand.text   for brand   in brands ]

# make sure the text data is in ascii format instead of unicode (why do we do this?)
price_text   = [ text.encode( 'ascii', 'ignore' ) for text in price_text ]
averagerating_text   = [ text.encode( 'ascii', 'ignore' ) for text in averagerating_text ]
numberofratings_text = [ text.encode( 'ascii', 'ignore' ) for text in numberofratings_text ]
model_text   = [ text.encode( 'ascii', 'ignore' ) for text in model_text ]
brand_text  = [ text.encode( 'ascii', 'ignore' ) for text in brand_text ]

# zip the text lists into a tuple (define:tuple = a list/set of numbers in mathematics and computing)
tuples = zip( price_text, averagerating_text, numberofratings_text, model_text, brand_text )

# write results to a TXT file (created TXT file before running script)
with open( "newegg.txt", "w" ) as txt_file:
    for t in tuples:
        line = "%s \t %s \t %s \n" % t
        print line
        txt_file.write( line )
txt_file.close()

