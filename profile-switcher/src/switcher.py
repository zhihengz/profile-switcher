#!/usr/bin/python
import getopt,sys,os
import xml.dom.minidom

class Profile:
    def __init__ ( self, name ):
        self.name = name
        self.path = None
        self.description = ""
        self.profiles = {}
        
class Subject:
    def __init__( self, name ):
        self.name = name
        self.profiles = {}
        self.alias = None

    def addProfile( self, aProfile ):
        self.profiles[ aProfile.name ] = aProfile

 
confXmlFile="profile-switch.conf"

def print_usage( progname ):
    print "Usage: " + progname + " [OPTIONS]"
    print "[OPTIONS] are:"
    print "--help                       print this help information"
    print "--list <subject>             list available profile(s)"
    print "--switch <subject> <profile> switch <subject> to use <profile>"
    print "--status <subject>           print out current profile status"
    print "--version                    print version"

def print_info( msg ):
    print "INFO:     " + msg

def print_warn( msg ):
    print "WARNING:  " + msg

def print_error( msg ):
    print "ERROR:    " + msg

def print_debug( msg ): 
    if not msg == None:
        print "DEBUG:    " + msg
    else:
        print "DEBUG:    " + "none"

def get_node_text( aNode ):

    if aNode.nodeType == aNode.TEXT_NODE:
        return aNode.nodeValue

    if aNode.nodeType == aNode.ELEMENT_NODE:
        for childNode in aNode.childNodes:
            childNodeText = get_node_text( childNode )
            if not childNodeText == None:
                return childNodeText

    # otherwise return none
    return None    
    
def readProfileConfig( configFile ):
    
    subjects = {}
    try:
        doc = xml.dom.minidom.parse( configFile )
    except IOError:
        print_error( "cannot read " + configFile )
        return subjects

    for node in doc.getElementsByTagName( "subject" ):
        subject = Subject( node.getAttribute( "name" ) )
        # load alias
        for aliasNode in node.getElementsByTagName( "alias" ):
            subject.alias = get_node_text( aliasNode )
        # ignore if no alias found
        if subject.alias == None:
            print_warn( "subject " + subject.name + " has no alias" );
            continue
        # load profiles
        for profileNode in node.getElementsByTagName( "profile" ):
            profile = Profile( profileNode.getAttribute( "name" ) )
            for childNode in profileNode.childNodes:
                if childNode.nodeName == "description":
                    profile.description = get_node_text( childNode )
                elif childNode.nodeName == "path":
                    profile.path = get_node_text( childNode )

            # skip if no path found
            if profile.path == None:
                print_warn( "profile " + profile.name + " has no path" )
                continue

            subject.addProfile( profile )

        subjects[ subject.name ] = subject

    return subjects
    
def print_subject( subject ):

    if subject == None:
        return
    
    msg = "subject: " + subject.name + " profiles: "

    hasPrevious = False
    for n, p in subject.profiles.iteritems( ):
        if hasPrevious:
            msg += "| "
        
        hasPrevious = True
        msg += p.name + " "
    print msg

def find_match_profile( profiles, realpath ):

    for n, p in profiles.iteritems( ):
        if os.path.exists( p.path ) and os.path.abspath( p.path ) == os.path.abspath( realpath ):
            return p.name
    
    return None

def subject_status( subject ):
    
    subjectPathAlias = subject.alias
    
    msg = "subject: " + subject.name + " "
    if os.path.exists( subjectPathAlias ):
        if os.path.islink( subjectPathAlias ):
            realPath = os.path.realpath( subjectPathAlias )
            if os.path.exists( realPath ):
                profileName = find_match_profile( subject.profiles, realPath )
                if profileName == None:
                    msg += "profile not found for " + realPath
                else:
                    msg += "current profile: " + profileName
            else:
                msg += "alias path to broken link " + realPath
        else:
            msg += "alias path " + subjectPathAlias + " is not link"
    else:
        msg += "alias path " + subjectPathAlias + " does not exists"

    print msg

def switch_profile ( subject, profileName ): 

    if subject == None:
        print_error( "subject is none" )

    profile = subject.profiles[ profileName ]

    if profile == None:
        print_error( "no profile " + profileName + 
                     " found on subject " + subject.name )
        return

    realProfilePath = os.path.realpath( profile.path )
    if not os.path.exists( realProfilePath ):
        print_error( "subject: " + subject.name + 
                     " profile: " + profile.name + 
                     " path " + profile.path + " does not exists" )
        return

    try:
        if os.path.islink( subject.alias ):
            os.unlink( subject.alias )
        elif os.pathq.exists( subject.alias ):
            print_error( "subject " + subject.name +
                         " alias " + subject.alias +
                         " is real file, please resolve firstly" );
            return
        
        os.symlink( realProfilePath, subject.alias )
        print "subject " + subject.name + " profile is " + profile.name
    except OSError:
        print_error( "cannot switch profile due to permission" )
def main( ):
    progname="switcher"
    version="1.0.0"
    author="Zhiheng Zhang"
    mainopts = [ "help",
                 "version",
                 "list",
                 "status",
                 "switch="]

    try:
        opts, args = getopt.getopt( sys.argv[1:], "", mainopts )
    except getopt.GetoptError:
        #print usgae        
        print_error ( "non-recognized command line arguments" )
        print_usage( progname )
        sys.exit( 1 );

    for o, a in  opts:
        if o == "--version":
            print progname + " version " + version + " by " + author
            break
        elif o == "--help":
            print_usage( progname )
            break
        elif o == "--list":
            subjects = readProfileConfig( confXmlFile )
            if len( args ) > 0:
                name = args[0]
                print_subject( subjects[ name ] )
            else:
                for n, s in subjects.iteritems( ):
                    print_subject ( s )
            break
        elif o == "--status":
            subjects = readProfileConfig( confXmlFile )
            if len( args ) > 0:
                name = args[0]
                subject_status( subjects[ name ] )
            else:
                for n, s in subjects.iteritems( ):
                    subject_status( s )
            break 
        elif o == "--switch":
            subjectName = a
            if len( args ) < 1:
                print_error( "not enough arguments for switch" )
                print_usage( progname )
                sys.exit( 1 )
                
            profileName = args[0]
            subjects = readProfileConfig( confXmlFile )
            switch_profile( subjects[ subjectName ], profileName )
            break
        else:
            print_usage( progname )

    sys.exit( 0 )


if __name__ == "__main__":
    main( )
