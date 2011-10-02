import unittest
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
        self.assertTrue(self.repo.hg_init())
        self.assertTrue(os.path.exists("test/.hg"))

    def test_010_Identity(self):
        rev = self.repo.hg_rev()
        hgid = self.repo.hg_id()
        self.assertEquals(-1, rev)
        self.assertEquals("000000000000", hgid)

    def test_020_Add(self):
        with open("test/file.txt", "w") as out:
            out.write("stuff")
        self.assertTrue(self.repo.hg_add("file.txt"))
        
    def test_030_Commit(self):
        self.repo.hg_commit("adding", user="test")
        rev  = self.repo.hg_rev()
        hgid = self.repo.hg_id()
        self.assertEquals(rev, 0)
        self.assertNotEquals(hgid, "000000000000")

    def test_040_Log(self):
        rev = self.repo[0]
        self.assertEquals(rev.desc, "adding")
        self.assertEquals(rev.author, "test")
        self.assertEquals(rev.branch, "default")
        self.assertEquals(rev.parents, [-1])


if __name__ == "__main__":
    unittest.main()
