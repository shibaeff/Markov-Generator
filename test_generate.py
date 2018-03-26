import unittest as ut
import generate as gen
import subprocess


class TestGenerate(ut.TestCase):
    def test_load_model(self):
        # broken path
        generator = gen.SentenceGenerator(".test_src/models/mmm.bin", 7, None, None)
        with self.assertRaises(RuntimeError):
            generator.load_model()

        # broken bin
        generator = gen.SentenceGenerator(".test_src/models/broken.bin", 7, None, None)
        with self.assertRaises(RuntimeError):
            generator.load_model()

    def test_gen_sent(self):
        # length was incorrectly specified
        generator = gen.SentenceGenerator("./test_src/model/m.bin", "seven", None, None)
        generator.load_model()
        with self.assertRaises(RuntimeError):
            generator.gen_sent()

        generator.length = -1
        with self.assertRaises(RuntimeError):
            generator.gen_sent()

        # seed is incorrectly specified
        # this case is succesfully handled
        generator = gen.SentenceGenerator("./test_src/model/m.bin", 7, 134, None)
        generator.load_model()
        generator.gen_sent()

    def test_save_sent(self):
        # output file does not exist -- handles it
        generator = gen.SentenceGenerator("./test_src/model/m.bin", 7, None, "./test_src/output/out11.txt")
        generator.load_model()
        generator.gen_sent()
        generator.save_sentence()
        # output file is not txt -- print warning
        generator.output = "./test_src/output/out11.text"
        with self.assertRaises(RuntimeWarning):
            generator.save_sentence()

    def test_console(self):
        # emulating the console output
        sample_output = open("./test_src/output/out.txt", "w+")
        assert subprocess.check_call("python generate.py '--model'"
                                     " './test_src/models/m.bin' '--seed' 'God' '--length' '7'",
                                     shell=True, stdout=sample_output) == 0
        # saving to file
        assert subprocess.check_call("python generate.py '--model' './test_src/models/m.bin' '--seed' 'God' '--length' "
                                     "'7' '--output' './test_src/output/sent.txt'",
                                     shell=True, stdout=sample_output) == 0


if __name__ == "__name__":
    ut.main()
