"""
A module to work with a Zettelkasten implemented with zetteldeft
"""
from collections import defaultdict
from pathlib import Path

LINK = "§"

class Zettelkasten:
    """Slip box manager
    """
    def __init__(self, path):
        self.path = Path(path)
        self.build()
        self.find_orphans()

    def build(self):
        files = list(self.path.glob("*.org"))
        self.n_zettels = len(files)
        self.zettels = {}
        self.n_links = 0
        self.links_to = {}
        self.links_from = defaultdict(list)

        for file in files:
            zet = Zettel(file)
            self.zettels[zet.idx] = zet
            self.n_links += len(zet.links_to)
            self.links_to[zet.idx] = zet.links_to
            for link in zet.links_to:
                self.links_from[link].append(zet.idx)

        # add back links
        for link in self.links_from:
            zet = self.zettels[zet.idx]
            zet.links_from = self.links_from[link]


    def find_orphans(self):
        """
        Find zettels that are not linked to other zettels
        """
        orphans = set()
        for item in self.zettels.items():
            idx, zet = item
            if zet.is_orphan():
                orphans.add(idx)
        self.orphans = orphans

    def find_widows(self):
        """
        Find zettels with dead links
        """
        raise NotImplementedError()

    def summary(self):
        """
        Report statistics on Slip box"""
        message = (
            f"Zettelkasten has {self.n_zettels} notes,"
            f" {self.n_links} links,"
            f" and {len(self.orphans)} orphans.")
        print(message)

class Zettel:
    """Individual note in Slip box
    """
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.name = self.file_path.name
        self.idx = self.name.split()[0]
        self.read()
        self.links_from = set() 

    def read(self):
        with self.file_path.open() as tmp:
            self.contents = tmp.readlines()

        self.links_to = set()
        for line in self.contents:
            if LINK in line:
                links = [link for link in line.split() if link.startswith(LINK)]
                for link in links:
                    self.links_to.add(link)

    def is_orphan(self):
        if len(self.links_from) == 0:
            if len(self.links_to) == 0:
                return True
        return False

    def summary(self):
        """
        Report characteristics of the zettel
        """
        raise NotImplementedError()

def main():
    path = "/home/serge/Dropbox/org/notes/zetteldeft"
    zk = Zettelkasten(path)
    return zk

if __name__ == '__main__':
    zk = main()
