import unittest
import os
from changelly import Changelly

class TestChangelly(unittest.TestCase):
    """ TestAoption

    Notes
    Not available until version 2.7
    def setUpClass(cls):
    def tearDownClass(cls):
    """

    def setUp(self):
        """
        Builtin method to instantiate a class
        :param cls: class handler
        :return:
        """
        self.cls = Changelly()

    def tearDown(self):
        #self.cls == True
        pass



    def test_rate(self):
        """

        :return:
        """
        # "gopher" MUST be an existing group the user already belongs to
        rrr = self.cls.getRate('xmr', 'eth');

        self.assertEqual(rrr, '-W group_list=Wrong_group')


if __name__ == '__main__':
    # Simple way
    #unittest.main()
    # Verbose way
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChangelly)
    unittest.TextTestRunner(verbosity=2).run(suite)