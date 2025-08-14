import os
import hashlib

class Generator:
    """
    Generates a new addons.xml file from each addon's addon.xml file
    and a new addons.xml.md5 hash file. Must be run from the root of
    the checked-out repo. Only handles a single-depth folder structure.
    """
    def __init__(self):
        # Generate files
        self._generate_addons_file()
        self._generate_md5_file()
        # Notify user
        print("Finished updating addons.xml and md5 files")

    def _generate_addons_file(self):
        # Addon list
        addons = os.listdir(".")
        # Final addons text
        addons_xml = u'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n'
        # Loop through and add each addon's addon.xml file
        for addon in addons:
            try:
                # Skip any file or .svn folder
                if not os.path.isdir(addon) or addon == ".svn":
                    continue
                # Create path
                _path = os.path.join(addon, "addon.xml")
                # Read and split lines
                with open(_path, "r", encoding="utf-8") as f:
                    xml_lines = f.read().splitlines()
                # New addon
                addon_xml = ""
                # Loop through and clean each line
                for line in xml_lines:
                    # Skip encoding format line
                    if line.startswith('<?xml'):
                        continue
                    # Add line
                    addon_xml += line.rstrip() + "\n"
                # Add to final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception as e:
                # Handle missing or poorly formatted addon.xml
                print(f"Excluding {_path} for {e}")
        # Clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"
        # Save file
        self._save_file(addons_xml, "addons.xml")

    def _generate_md5_file(self):
        try:
            # Create a new md5 hash
            with open("addons.xml", "rb") as f:
                m = hashlib.md5(f.read()).hexdigest()
            # Save file
            self._save_file(m, "addons.xml.md5")
        except Exception as e:
            # Handle errors
            print(f"An error occurred creating addons.xml.md5 file!\n{e}")

    def _save_file(self, data, file):
        try:
            # Write data to the file
            with open(file, "w", encoding="utf-8") as f:
                f.write(data)
        except Exception as e:
            # Handle errors
            print(f"An error occurred saving {file} file!\n{e}")

if __name__ == "__main__":
    # Start
    Generator()
