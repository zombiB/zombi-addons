#!/usr/bin/python
# *
# *  Copyright (C) 2012-2013 Garrett Brown
# *  Copyright (C) 2010      j48antialias
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  Based on code by j48antialias:
# *  https://anarchintosh-projects.googlecode.com/files/addons_xml_generator.py
 
""" addons.xml generator """

import os
import sys
import time
import re
import xml.etree.ElementTree as ET
try:
    import shutil, zipfile
except Exception as e:
    print('An error occurred importing module!\n%s\n' % e)
 
# Compatibility with 3.0, 3.1 and 3.2 not supporting u"" literals
print(sys.version)
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x
 
class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    def __init__(self):
        # generate files
        self._generate_addons_file()
        self._generate_md5_file()
        # notify user
        print("Finished updating addons xml and md5 files\n")
 
    def _generate_addons_file(self):
        # addon list
        addons = os.listdir(".")
        # final addons text
        addons_xml = u("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n")
        # loop thru and add each addons addon.xml file
        for addon in addons:
            try:
                # skip any file or .svn folder or .git folder
                if (not os.path.isdir(addon) or addon == ".svn" or addon == ".git" or addon == "zips"): continue
                # create path
                _path = os.path.join(addon, "addon.xml")
                # split lines for stripping
                xml_lines = open(_path, "r").read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if (line.find("<?xml") >= 0): continue
                    # add line
                    if sys.version < '3':
                        addon_xml += unicode(line.rstrip() + "\n", "UTF-8")
                    else:
                        addon_xml += line.rstrip() + "\n"
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception as e:
                # missing or poorly formatted addon.xml
                print("Excluding %s for %s" % (_path, e))
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u("\n</addons>\n")
        # save file
        self._save_file(addons_xml.encode("UTF-8"), file="addons.xml")
 
    def _generate_md5_file(self):
        # create a new md5 hash
        try:
            import md5
            m = md5.new(open("addons.xml", "r").read()).hexdigest()
        except ImportError:
            import hashlib
            m = hashlib.md5(open("addons.xml", "r", encoding="UTF-8").read().encode("UTF-8")).hexdigest()
 
        # save file
        try:
            self._save_file(m.encode("UTF-8"), file="addons.xml.md5")
        except Exception as e:
            # oops
            print("An error occurred creating addons.xml.md5 file!\n%s" % e)
 
    def _save_file(self, data, file):
        try:
            # write data to the file (use b for Python 3)
            open(file, "wb").write(data)
        except Exception as e:
            # oops
            print("An error occurred saving %s file!\n%s" % (file, e))
 
 
def zipfolder(foldername, target_dir, zips_dir, addon_dir):
    zipobj = zipfile.ZipFile(zips_dir + foldername, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for f in files:
            fn = os.path.join(base, f)
            zipobj.write(fn, os.path.join(addon_dir, fn[rootlen:]))
    zipobj.close()


                     
if (__name__ == "__main__"):
    # start
    Generator()

    # rezip files and move
    try:
        print('Starting zip file creation...')
        rootdir = sys.path[0]
        zipsdir = rootdir + os.sep + 'zips'   
        filesinrootdir = os.listdir(rootdir)
        
        for x in filesinrootdir:
            if re.search("^(context|plugin|script|service|skin|repository)" , x) and not re.search('.zip', x):
                zipfilename = x + '.zip'
                zipfilenamefirstpart = zipfilename[:-4]
                zipfilenamelastpart = zipfilename[len(zipfilename) - 4:]
                zipsfolder = os.path.normpath(os.path.join('zips', x)) + os.sep
                foldertozip = rootdir + os.sep + x
                filesinfoldertozip = os.listdir(foldertozip)        
                # #check if zips folder exists
                if not os.path.exists(zipsfolder):
                    os.makedirs(zipsfolder)
                    print('Directory doesn\'t exist, creating: ' + zipsfolder)                
                # #get addon version number           
                if "addon.xml" in filesinfoldertozip: 
                    tree = ET.parse(os.path.join(rootdir, x, "addon.xml"))
                    root = tree.getroot()
                    for elem in root.iter('addon'):
                        print('%s %s version: %s' % (x, elem.tag, elem.attrib['version']))
                        version = '-' + elem.attrib['version']                  
                # #check if and move addon, changelog, fanart and icon to zipdir                       
                for y in filesinfoldertozip: 
                    # print('processing file: ' + os.path.join(rootdir,x,y))
                    if re.search("addon|changelog|icon|fanart", y):
                        shutil.copyfile(os.path.join(rootdir, x, y), os.path.join(zipsfolder, y))
                        print('Copying %s to %s' % (y, zipsfolder))                
                # #check for and zip the folders
                print('Zipping %s and moving to %s\n' % (x, zipsfolder))
                try:
                    zipfolder(zipfilenamefirstpart + version + zipfilenamelastpart, foldertozip, zipsfolder, x)
                    print('zipped with zipfolder\n')
                except:
                    if os.path.exists(zipsfolder + x + version + '.zip'):
                        os.remove(zipsfolder + x + version + '.zip')
                        print('trying shutil')
                    try:
                        shutil.move(shutil.make_archive(foldertozip + version, 'zip', rootdir, x), zipsfolder)
                        print('zipped with shutil\n')
                    except Exception as e:
                        print('Cannot create zip file\nshutil %s\n' % e)
    except Exception as e:
        print('Cannot create or move the needed files\n%s' % e)
    print('Done')