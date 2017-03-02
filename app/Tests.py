import unittest
from game import Game

class TestHangman(unittest.TestCase):

    def test_winning(self):
        g = Game('fake_user', 'tarantula', '_________', False, 10, '')
        
        g.tryLetter('t')
        g.tryLetter('a')
        g.tryLetter('r')
        g.tryLetter('n')
        g.tryLetter('u')
        g.tryLetter('l')
        
        self.assertEqual(g.lives, 10)
        self.assertTrue(all([x != None for x in g.letters]))
        self.assertEqual(g.letters_guessed, 'tarnul')
        
        self.assertTrue(g.game_over)
        self.assertTrue(g.win)
        
    def test_losing(self):
        g = Game('fake_user', 'tarantula', '_________', False, 10, '')
        g.tryLetter('q')
        g.tryLetter('z')
        g.tryLetter('y')
        g.tryLetter('x')
        g.tryLetter('w')
        g.tryLetter('v')
        g.tryLetter('p')
        g.tryLetter('c')
        g.tryLetter('b')
        g.tryLetter('k')
        
        self.assertTrue(g.game_over)
        self.assertFalse(g.win)
    
    def test_good_letter(self):
        g = Game('fake_user', 'tarantula', '_________', False, 10, '')
        
        g.tryLetter('q')
        g.tryLetter('a')
        
        self.assertEqual(g.lives, 9)
        self.assertEqual(g.letters_guessed, 'qa')
        
        for i, x in enumerate(g.letters):
            if i in [1,3,8]:
                self.assertEqual(x, 'a')
            else:
                self.assertEqual(x, None)
                
        self.assertFalse(g.game_over)
    
    def test_bad_letter(self):
        g = Game('fake_user', 'tarantula', '_________', False, 10, '')
        g.tryLetter('q')
        
        self.assertEqual(g.lives, 9)
        self.assertTrue(all([x == None for x in g.letters]))
        self.assertEqual(g.letters_guessed, 'q')
        
        self.assertFalse(g.game_over)

if __name__ == '__main__':
    unittest.main()