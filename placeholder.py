import pafy

urlList = ["95951E4YO1Q", "x3HnY6_Ho4E",
           "iWw4xOh1bT4", "kEdOo90Ob34", "Jjfq7sSTslM", "v_kIzjHZ6ao"]

objects = []

totalUrls = len(urlList)

for url in urlList:
    print "Creating object for url: %s" % url
    objects = [pafy.new(url) for x in range(totalUrls)]

for o in objects:
    print "Processing object: %s" % o
    print "\n\n"
    print "Title: %s" % o.title
    print "Description: %s" % o.description
    print "Thumb: %s" % o.bigthumbhd
    print "MP4 Video Link: %s" % o.getbest(preftype="mp4").url
    print "\n\n"

