import httplib, urllib2
import base64
import xml.etree.ElementTree as ET

def getUrl(address, url):
    conn = httplib.HTTPConnection(address)
    conn.request("GET", url)
    res = conn.getresponse()
    if res.status != 200:
        print "Connection failed, error code " + str(res.status)
        print address + url
        return
    buf = res.read()
    conn.close()
    return buf


class pumilioCon:
    """ A class for making and using a connection to a 
        pumilio ecological recoding database"""
   
    address = ""
    url = ""
    username = ""
    password = ""
    login = ""
    XML = ""
   
    def __init__(self, address="127.0.0.1", url="/", username="admin", password="pass"):
        self.address = address
        self.url = url
        self.username = username
        self.password = password
        self.login = username + ";" + password
    
    def getXML(self):
        xmlUrl = self.url + "xml.php"
        if self.login != "":
            xmlUrl += "?login=" + self.login
        self.XML = ET.fromstring(getUrl(self.address, xmlUrl))
        
    def checkVersion(self):
        if self.XML == "":
            self.getXML()
        root = self.XML
        ver = root.find("pumilio_version").text
        print "Pumilio Version: " + ver
        return ver

    def projectTitle(self):
        if self.XML == "":
            self.getXML()
        root = self.XML
        title = root.find("pumilio_title").text
        desc = root.find("pumilio_description").text
        print "Pumilio Server Title: " + title
        print desc
        return title, desc

    #retuns an xml.etree.ElementTree.Element object    
    def getCollections(self):
        if self.XML == "":
            self.getXML()
        root = self.XML
        collections = root.find("Collections")
        print "Collections:"
        for c in collections:
            print c.find("CollectionName").text + ", ID: " + c.find("ColID").text
        return collections

    #retuns an xml.etree.ElementTree.Element object    
    def getSites(self):
        if self.XML == "":
            self.getXML()
        root = self.XML
        sites = root.find("Sites")
        print "Sites:"
        for s in sites:
            print s.find("SiteName").text + ", ID: " + s.find("SiteID").text
        return sites

    #retuns an xml.etree.ElementTree.Element object    
    def getSounds(self, siteID="", colID="", urlType="all"):
        #if useColID is true, we will search by collection ID instead of site ID
        u = "xml.php?type=" + urlType + "&SiteID=" + siteID + "&ColID=" + colID
        searchXML = getUrl(self.address, self.url + u)
        result = ET.fromstring(searchXML)
        sounds = result.find("Sounds")
        total = 0 
        for s in sounds:
            total += 1
        print "Queried with Site ID " + siteID + " and Collection ID " + colID
        print str(total) + " sounds found"
        return sounds
    
    #this works a bit different than the pumilioR library for R that this script is based on
    #just provide soundID and site ID and/or collectio ID
    def getFile(self, soundID, siteID="", colID=""):
        sounds = self.getSounds(siteID, colID)
        filePath = ""
        for s in sounds:
            if s.find("SoundID").text == soundID:
                filePath = s.find("FilePath").text
                fileName = s.find("OriginalFilename").text
                break
        request = urllib2.Request(filePath)
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        result = urllib2.urlopen(request)
        
        #this gets a 403 regardless, but my credentials don't work on the Purdue server
        # so I can't see how it's supposed to work properly
        
        #print "Downloaded file ID " + soundID + ": " + fileName
        

con = pumilioCon("1159sequoia06.fnr.purdue.edu", "/borneo2014/", "soundscape", "HEMAlab2479")
con.checkVersion()
con.projectTitle()
con.getCollections()
con.getSites()
con.getFile("102", "103")
