from __future__ import with_statement
import unittest, doctest
import os, shutil, os.path
import gitapi 

class TestGitAPI(unittest.TestCase):
    """Tests for gitapi.py
    Uses and wipes subfolder named 'test'
    Tests are dependant on each other; named test_<number>_name for sorting
    """
    repo = gitapi.Repo("./test", user="Testuser <test@example.com>")
    
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

    def test_005_Init(self):
        self.repo.git_init()
        self.assertTrue(os.path.exists("test/.git"))

    #def test_040_Identity(self):

#        gitid = self.repo.git_id()

#       self.assertEquals("000000000000", gitid)

    def test_020_Add(self):
        with open("test/file.txt", "w") as out:
            out.write("stuff")
        self.repo.git_add("file.txt")
        
    def test_030_Commit(self):
        #Commit and check that we're on a real revision
        self.repo.git_commit("adding", user="test <test@example.com>")
        gitid = self.repo.git_id()
        self.assertNotEquals(gitid, "000000000000")

        #write some more to file
        with open("test/file.txt", "w+") as out:
            out.write("more stuff")

        #Commit and check that changes have been made
        self.repo.git_commit("modifying", user="test <test@example.com>")

        gitid2 = self.repo.git_id()

        self.assertNotEquals(gitid, gitid2)


    def test_040_Log(self):
        rev = self.repo[self.repo.git_id()]
        self.assertEquals(rev.desc, "modifying")
        self.assertEquals(rev.author, "test")
        self.assertEquals(len(rev.parents), 1)

    def test_050_Checkout(self):
        node = self.repo.git_id()
        
        self.repo.git_checkout('HEAD~1')
        self.assertNotEquals(self.repo.git_id(), node)
        self.repo.git_checkout(node)
        self.assertEquals(self.repo.git_id(), node)


    def test_070_Config(self):

        for key, value in (("test.stuff.otherstuff", "tsosvalue"),
                  ("test.stuff.debug", "true"),
                  ("test.stuff.verbose", "false"),
                  ("test.stuff.list", "one two three")):
            self.repo.git_command("config", key, value)
        #re-read config
        self.repo.read_config()     
        self.assertEquals(self.repo.config('test', 'stuff.otherstuff'),
                          "tsosvalue")

    def test_071_ConfigBool(self):
        self.assertTrue(self.repo.configbool('test', 'stuff.debug'))
        self.assertFalse(self.repo.configbool('test', 'stuff.verbose'))
        
    def test_072_ConfigList(self):
        self.assertTrue(self.repo.configlist('test', 'stuff.list'),
                        ["one", "two", "three"])
  

    def test_090_ModifiedStatus(self):
        #write some more to file
        with open("test/file.txt", "a") as out:
            out.write("stuff stuff stuff")
        status = self.repo.git_status()
        self.assertEquals(status, 
                          {'M': ['file.txt']})
        
    def test_100_CleanStatus(self):
        #commit file created in 090
        self.repo.git_commit("Comitting changes", user="Test <test@example.com>")
        #Assert status is empty
        self.assertEquals(self.repo.git_status(), 
                          {})

    def test_110_UntrackedStatus(self):
        #Create a new file
        with open("test/file2.txt", "w") as out:
            out.write("stuff stuff stuff")
        status = self.repo.git_status()
        self.assertEquals(status, 
                          {'??': ['file2.txt']})

    def test_120_AddedStatus(self):
        #Add file created in 110
        self.repo.git_add("file2.txt")
        status = self.repo.git_status()
        self.assertEquals(status, 
                          {'A': ['file2.txt']})

    def test_130_MissingStatus(self):
        #Commit file created in 120
        self.repo.git_commit("Added file")
        import os
        os.unlink("test/file2.txt")
        status = self.repo.git_status()
        self.assertEquals(status, 
                          {'D': ['file2.txt']})

    def test_140_RemovedStatus(self):
        #Remove file from repo
        self.repo.git_remove("file2.txt")
        status = self.repo.git_status()
        self.assertEquals(status, 
                          {'D': ['file2.txt']})

    def test_140_EmptyStatus(self):
        self.repo.git_reset()
        status = self.repo.git_status()
        self.assertEquals(status, {})

    def test_150_ForkAndMerge(self):
        #Store this version
        node = self.repo.git_id()
        
        #creates new branch
        self.repo.git_branch("test", "HEAD~2")
        self.repo.git_checkout("test")
        with open("test/file3.txt", "w") as out:
            out.write("this is more stuff")
        self.repo.git_add("file3.txt")
        self.repo.git_commit("adding head")
        branches = self.repo.git_branches()
        self.assertTrue("test" in branches)

        #merge the changes
        self.repo.git_checkout("master")
        self.repo.git_merge("test")

        with open("test/file3.txt", "r") as src:
            self.assertEqual(src.read(), "this is more stuff")

        

def test_doc():
    #Prepare for doctest
    os.mkdir("./test_gitapi")
    with open("test_gitapi/file.txt", "w") as target:
        w = target.write("stuff")
    try:
        #Run doctest
        res = doctest.testfile("../README.rst")
    finally:
        #Cleanup
        shutil.rmtree("test_gitapi")

if __name__ == "__main__":
    import sys
    try:
        test_doc()
    finally:
        unittest.main()
    
