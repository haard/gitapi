import unittest, doctest
import os, shutil, os.path
import hgapi 

class TestHgAPI(unittest.TestCase):
    """Tests for hgapi.py
    Uses and wipes subfolder named 'test'
    Tests are dependant on each other; named test_<number>_name for sorting
    """
    repo = hgapi.Repo("./test")
    
    @classmethod
    def setUpClass(self):
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


if __name__ == "__main__":
    res = doctest.testfile("README.rst")
    unittest.main()
    
