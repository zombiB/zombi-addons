"""
    Repository, addons.xml and addons.xml.md5 structural generator

        Modifications:

        - by Rodrigo@TVADDONS: Zip plugins/repositories to a "zip" folder
        - BartOtten: Create a repository addon, skip folders without addon.xml, user config file
        - Twilight0@TVADDONS: Ignore .idea subdirectories in addons' directories, changed from md5 module to hashlib
                              copy changelogs, icons and fanarts

    This file is provided "as is", without any warranty whatsoever. Use as own risk
"""

import os
import hashlib
import zipfile
import shutil
import datetime
from xml.dom import minidom
from ConfigParser import SafeConfigParser


# Load the configuration:
config = SafeConfigParser()
config.read('config.ini')
tools_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
output_path = "_" + config.get('locations', 'output_path')
addonid = config.get('addon', 'id')
name = config.get('addon', 'name')
version = config.get('addon', 'version')
author = config.get('addon', 'author')
summary = config.get('addon', 'summary')
description = config.get('addon', 'description')
url = config.get('locations', 'url')


class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from a subdirectory (eg. _tools) of
        the checked-out repo. Only handles single depth folder structure.
    """

    def __init__(self):

        # travel path one up
        os.chdir(os.path.abspath(os.path.join(tools_path, os.pardir)))

        # generate files
        self._pre_run()
        self._generate_repo_files()
        self._generate_addons_file()
        self._generate_md5_file()
        self._generate_zip_files()

    def _pre_run(self):

        # create output  path if it does not exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    def _generate_repo_files(self):

        if os.path.isfile(addonid + os.path.sep + "addon.xml"):
            return

        print "Create repository addon"

        with open(tools_path + os.path.sep + "template.xml", "r") as template:
            template_xml = template.read()

        repo_xml = template_xml.format(
            addonid=addonid,
            name=name,
            version=version,
            author=author,
            summary=summary,
            description=description,
            url=url,
            output_path=output_path)

        # save file
        if not os.path.exists(addonid):
            os.makedirs(addonid)

        self._save_file(repo_xml.encode("utf-8"), file=addonid + os.path.sep + "addon.xml")

    def _generate_zip_files(self):
        global version, addonid
        addons = os.listdir(".")
        # loop thru and add each addons addon.xml file
        for addon in addons:
            # create path
            _path = os.path.join(addon, "addon.xml")
            # skip path if it has no addon.xml
            if not os.path.isfile(_path):
                continue
            try:
                # skip any file or .git folder
                if not (os.path.isdir(addon) or addon == ".idea" or addon == ".git" or addon == ".svn" or addon == output_path or addon == tools_path):
                    continue
                # create path
                _path = os.path.join(addon, "addon.xml")
                # split lines for stripping
                document = minidom.parse(_path)
                for parent in document.getElementsByTagName("addon"):
                    version = parent.getAttribute("version")
                    addonid = parent.getAttribute("id")
                self._generate_zip_file(addon, version, addonid)
            except Exception, e:
                print e

    def _generate_zip_file(self, path, version, addonid):
        print "Generate zip file for " + addonid + " " + version
        filename = path + "-" + version + ".zip"
        try:
            zip = zipfile.ZipFile(filename, 'w')
            for root, dirs, files in os.walk(path + os.path.sep):
                if '.idea' in dirs:
                    dirs.remove('.idea')
                zip.write(os.path.join(root))
                for file in files:
                    zip.write(os.path.join(root, file))

            zip.close()

            if not os.path.exists(output_path + addonid):
                os.makedirs(output_path + addonid)

            if os.path.isfile(output_path + addonid + os.path.sep + filename):
                # pass #uncomment to overwrite existing zip file, then comment or remove the next two lines below
                os.rename(output_path + addonid + os.path.sep + filename,
                    output_path + addonid + os.path.sep + filename + "." + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            shutil.move(filename, output_path + addonid + os.path.sep + filename)
        except Exception, e:
            print e

    def _generate_addons_file(self):
        print "Generating addons.xml file"
        # addon list
        addons = os.listdir(".")
        # final addons text
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n"
        # loop thru and add each addons addon.xml file
        for addon in addons:
            # create path
            _path = os.path.join(addon, "addon.xml")
            # skip path if it has no addon.xml
            if not os.path.isfile(_path):
                continue
            try:
                # split lines for stripping
                xml_lines = open(_path, "r").read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if (line.find("<?xml") >= 0):
                        continue
                    # add line
                    addon_xml += unicode(line.rstrip() + "\n", "utf-8")
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception, e:
                # missing or poorly formatted addon.xml
                print "Excluding %s for %s" % (_path, e,)
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"
        # save file
        self._save_file(addons_xml.encode("utf-8"), file=output_path + "addons.xml")

    def _generate_md5_file(self):
        print "Generating addons.xml.md5 file"
        try:
            # create a new md5 hash
            m = hashlib.md5(open(output_path + "addons.xml").read()).hexdigest()
            # save file
            self._save_file(m, file=output_path + "addons.xml.md5")
        except Exception, e:
            # oops
            print "An error occurred creating addons.xml.md5 file!\n%s" % (e,)

    def _save_file(self, data, file):
        try:
            # write data to the file
            open(file, "w").write(data)
        except Exception, e:
            # oops
            print "An error occurred saving %s file!\n%s" % (file, e,)


class Copier:
    def __init__(self):
        self._copy_additional_files()

    def _copy_additional_files(self):
        os.chdir(os.path.abspath(os.path.join(tools_path, os.pardir)))
        addons = os.listdir(".")
        for addon in addons:
            xml_file = os.path.join(addon, "addon.xml")
            if not os.path.isfile(xml_file):
                continue
            if not (os.path.isdir(addon) or addon == ".idea" or addon == ".git" or addon == ".svn" or addon == output_path or addon == tools_path):
                continue
            document = minidom.parse(xml_file)
            for parent in document.getElementsByTagName("addon"):
                version = parent.getAttribute("version")
                try:
                    if os.path.isfile(output_path + addon + os.path.sep + "changelog-" + version + ".txt"):
                        pass
                    else:
                        shutil.copy(addon + os.path.sep + "changelog.txt", output_path + addon + os.path.sep + "changelog-" + version + ".txt")
                except IOError:
                    pass
                try:
                    if os.path.isfile(output_path + addon + os.path.sep + "icon.png"):
                        pass
                    else:
                        shutil.copy(addon + os.path.sep + "icon.png", output_path + addon + os.path.sep + "icon.png")
                except IOError:
                    pass
                try:
                    if os.path.isfile(output_path + addon + os.path.sep + "fanart.jpg"):
                        pass
                    else:
                        shutil.copy(addon + os.path.sep + "fanart.jpg", output_path + addon + os.path.sep + "fanart.jpg")
                except IOError:
                    pass

if __name__ == "__main__":
    Generator()
    Copier()
    print "Finished updating addons xml & md5 files, zipping addons and copying additional files"
