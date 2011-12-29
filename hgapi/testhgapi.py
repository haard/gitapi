from __future__ import with_statement
import unittest, doctest
import os, shutil, os.path
import hgapi 

class TestHgAPI(unittest.TestCase):
    """Tests for hgapi.py
    Uses and wipes subfolder named 'test'
    Tests are dependant on each other; named test_<number>_name for sorting
    """
    repo = hgapi.Repo("./test", user="testuser")
    
    @classmethod
    def setUpClass(cls):
        #Patch Python 3
        if hasattr(cls, "assertEqual"):
            setattr(cls, "assertEquals", cls.assertEqual)
            setattr(cls, "assertNotEquals", cls.assertNotEqual)
        if os.path.exists("./test"):
            shutil.rmtree("./test")
        os.mkdir("./test")
        assert os.path.exists("./test")

    @classmethod
    def tearDownClass(self):
        shutil.rmtree("test")

    def test_000_Init(self):
        self.repo.hg_init()
        self.assertTrue(os.path.exists("test/.hg"))

    def test_010_Identity(self):
        rev = self.repo.hg_rev()
        hgid = self.repo.hg_id()
        self.assertEquals(-1, rev)
        self.assertEquals("000000000000", hgid)

    def test_020_Add(self):
        with open("test/file.txt", "w") as out:
            out.write("stuff")
        self.repo.hg_add("file.txt")
        
    def test_030_Commit(self):
        #Commit and check that we're on a real revision
        self.repo.hg_commit("adding", user="test")
        rev  = self.repo.hg_rev()
        hgid = self.repo.hg_id()
        self.assertEquals(rev, 0)
        self.assertNotEquals(hgid, "000000000000")

        #write some more to file
        with open("test/file.txt", "w+") as out:
            out.write("more stuff")

        #Commit and check that changes have been made
        self.repo.hg_commit("modifying", user="test")
        rev2  = self.repo.hg_rev()
        hgid2 = self.repo.hg_id()
        self.assertNotEquals(rev, rev2)
        self.assertNotEquals(hgid, hgid2)

    def test_040_Log(self):
        rev = self.repo[0]
        self.assertEquals(rev.desc, "adding")
        self.assertEquals(rev.author, "test")
        self.assertEquals(rev.branch, "default")
        self.assertEquals(rev.parents, [-1])

    def test_050_Update(self):
        node = self.repo.hg_id()
        self.repo.hg_update(1)
        self.assertEquals(self.repo.hg_rev(), 1)
        self.repo.hg_update("tip")
        self.assertEquals(self.repo.hg_id(), node)


    def test_060_Heads(self):
        node = self.repo.hg_node()

        self.repo.hg_update(0)
        with open("test/file.txt", "w+") as out:
            out.write("even more stuff")

        #creates new head
        self.repo.hg_commit("modifying", user="test")

        heads = self.repo.hg_heads()
        self.assertEquals(len(heads), 2)
        self.assertTrue(node in heads)
        self.assertTrue(self.repo.hg_node() in heads)

        #Close head again
        self.repo.hg_commit("Closing branch", close_branch=True)
        self.repo.hg_update(node)

        #Check that there's only one head remaining
        heads = self.repo.hg_heads()
        self.assertEquals(len(heads), 1)
        self.assertTrue(node in heads)

    def test_070_Config(self):
        with open("test/.hg/hgrc", "w") as hgrc:
            hgrc.write("[test]\n" +
                       "stuff.otherstuff = tsosvalue\n" +
                       "stuff.debug = True\n" +
                       "stuff.verbose = false\n" +
                       "stuff.list = one two three\n" +
                       "[ui]\n" +
                       "username = testsson")
        #re-read config
        self.repo.read_config()     
        self.assertEquals(self.repo.config('test', 'stuff.otherstuff'),
                          "tsosvalue")
        self.assertEquals(self.repo.config('ui', 'username'),
                          "testsson")


    def test_071_ConfigBool(self):
        self.assertTrue(self.repo.configbool('test', 'stuff.debug'))
        self.assertFalse(self.repo.configbool('test', 'stuff.verbose'))
        
    def test_072_ConfigList(self):
        self.assertTrue(self.repo.configlist('test', 'stuff.list'),
                        ["one", "two", "three"])

    def test_080_LogBreakage(self):
        """Some log messages/users could possibly break 
        the revision parsing"""
        #write some more to file
        with open("test/file.txt", "w+") as out:
            out.write("stuff and, more stuff")

        #Commit and check that changes have been made
        self.repo.hg_commit("}", user="},desc=\"test")
        self.assertEquals(self.repo["tip"].desc, "}")
        self.assertEquals(self.repo["tip"].author, "},desc=\"test")
  

    def test_090_ModifiedStatus(self):
        #write some more to file
        with open("test/file.txt", "a") as out:
            out.write("stuff stuff stuff")
        status = self.repo.hg_status()
        self.assertEquals(status, 
                          {'A': [], 'M': ['file.txt'], '!': [], 
                           '?': [], 'R': []})
        
    def test_100_CleanStatus(self):
        #commit file created in 090
        self.repo.hg_commit("Comitting changes", user="test")
        #Assert status is empty
        self.assertEquals(self.repo.hg_status(), 
                          {'A': [], 'M': [], '!': [], '?': [], 'R': []})

    def test_110_UntrackedStatus(self):
        #Create a new file
        with open("test/file2.txt", "w") as out:
            out.write("stuff stuff stuff")
        status = self.repo.hg_status()
        self.assertEquals(status, 
                          {'A': [], 'M': [], '!': [], 
                           '?': ['file2.txt'], 'R': []})

    def test_120_AddedStatus(self):
        #Add file created in 110
        self.repo.hg_add("file2.txt")
        status = self.repo.hg_status()
        self.assertEquals(status, 
                          {'A': ['file2.txt'], 'M': [], '!': [], 
                           '?': [], 'R': []})

    def test_130_MissingStatus(self):
        #Commit file created in 120
        self.repo.hg_commit("Added file")
        import os
        os.unlink("test/file2.txt")
        status = self.repo.hg_status()
        self.assertEquals(status, 
                          {'A': [], 'M': [], '!': ['file2.txt'], 
                           '?': [], 'R': []})

    def test_140_RemovedStatus(self):
        #Remove file from repo
        self.repo.hg_remove("file2.txt")
        status = self.repo.hg_status()
        self.assertEquals(status, 
                          {'A': [], 'M': [], '!': [], 
                           '?': [], 'R': ['file2.txt']})

    def test_140_EmptyStatus(self):
        self.repo.hg_revert(all=True)
        status = self.repo.hg_status(empty=True)
        self.assertEquals(status, {})

    def test_150_ForkAndMerge(self):
        #Store this version
        node = self.repo.hg_node()

        self.repo.hg_update(4, clean=True)
        with open("test/file3.txt", "w") as out:
            out.write("this is more stuff")

        #creates new head
        self.repo.hg_add("file3.txt")
        self.repo.hg_commit("adding head", user="test")

        heads = self.repo.hg_heads()
        self.assertEquals(len(heads), 2)
        self.assertTrue(node in heads)
        self.assertTrue(self.repo.hg_node() in heads)

        #merge the changes
        self.repo.hg_merge(node)
        self.repo.hg_commit("merge")
        
        #Check that there's only one head remaining
        heads = self.repo.hg_heads()
        self.assertEquals(len(heads), 1)

def test_doc():
    #Prepare for doctest
    os.mkdir("./test_hgapi")
    with open("test_hgapi/file.txt", "w") as target:
        w = target.write("stuff")
    try:
        #Run doctest
        res = doctest.testfile("../README.rst")
    finally:
        #Cleanup
        shutil.rmtree("test_hgapi")

if __name__ == "__main__":
    import sys
    try:
        test_doc()
    finally:
        unittest.main()
    
