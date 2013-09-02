from __future__ import with_statement
import unittest, doctest
import os, shutil, os.path
import gitapi
import stat

def onfserror(delegate, path, exec_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        delegate(path)
    else:
        raise

class TestGitAPI(unittest.TestCase):
    """Tests for gitapi.py
    Uses and wipes subfolder named 'test' and 'test-clone'
    Tests are dependant on each other; named test_<number>_name for sorting
    """
    repo = gitapi.Repo("./test", user="Testuser <test@example.com>")
    clone = gitapi.Repo("./test-clone", user="Testuser <test@example.com>")
    bareclone = gitapi.Repo("./test-clone-bare", user="Testuser <test@example.com>")


    @classmethod
    def _delete_and_create(cls, path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        assert os.path.exists(path)

    @classmethod
    def setUpClass(cls):
        # patch for Python 3
        if hasattr(cls, "assertEqual"):
            setattr(cls, "assertEquals", cls.assertEqual)
            setattr(cls, "assertNotEquals", cls.assertNotEqual)
        TestGitAPI._delete_and_create("./test")
        TestGitAPI._delete_and_create("./test-clone")
        TestGitAPI._delete_and_create("./test-clone-bare")


    @classmethod
    def tearDownClass(self):
        shutil.rmtree("test", ignore_errors=True)
        shutil.rmtree("test-clone", ignore_errors=True)
        shutil.rmtree("test-clone-bare", ignore_errors=True)

    def test_005_Init(self):
        self.repo.git_init()
        self.assertTrue(os.path.exists("test/.git"))


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

    def test_300_clone(self):
        # clone test to test clone
        self.clone = gitapi.Repo.git_clone("./test", "./test-clone")
        self.assertTrue(isinstance(self.clone, gitapi.Repo))
        self.assertEquals(self.clone.path, self.repo.path + "-clone")

    def test_310_pull(self):
        # add a new directory with some files in test repo first
        os.mkdir("./test/cities")
        with open("./test/cities/brussels.txt", "w") as out:
            out.write("brussel")
        with open("./test/cities/antwerp.txt", "w") as out:
            out.write("antwerpen")
        self.repo.git_add("cities")
        message = "[TEST] Added two cities."
        self.repo.git_commit(message)
        self.clone.git_pull("../test")

        self.assertEquals(self.clone.git_id(), self.repo.git_id())
        # check summary of pulled tip
        self.assertTrue(message in self.clone.git_log(identifier="HEAD"))

    def test_320_push(self):
        #Make a bare clone of test
        gitapi.Repo.git_clone('test', 'test-clone-bare', '--bare')
        # add another file in test-clone first
        with open("./test-clone/cities/ghent.txt", "w") as out:
            out.write("gent")
        self.clone.git_add('cities')
        message = "[CLONE] Added one file."
        self.clone.git_commit(message)
        self.clone.git_push("../test-clone-bare")

        self.assertEquals(self.clone.git_id(), self.bareclone.git_id())
        # check summary of pushed tip
        self.assertTrue(message in self.bareclone.git_log(identifier="HEAD"))
      

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
    
