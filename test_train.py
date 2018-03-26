import unittest as ut
import subprocess
import train as tr
import os


class TrainTest(ut.TestCase):
    def test_process_sources(self):
        # directory that doesn't exist
        trainer = tr.ModelTrainer(model_dir="./test_src/model/m.bin", input_dir="./test_src/src_fake")
        with self.assertRaises(FileNotFoundError):
            trainer.process_sources()

        # directory is empty
        trainer.input_dir = "./test_src/empty_dir"
        with self.assertRaises(RuntimeError):
            trainer.process_sources()

    def test_save_model(self):
        trainer = tr.ModelTrainer(model_dir="./test_src/model/save_test.bin", input_dir="./test_src/samples")
        trainer.process_sources()
        trainer.build_model()
        trainer.save_model()
        assert os.path.exists("./test_src/model/save_test.bin")

    def test_build_model(self):
        common_src_path = "./test_src/samples/"
        case_dirs = ["simple", "middle"]  # contain tests of different complexity.
                                          # simple is a poem;
                                          # middle is the United States Constitution;
        word_counts = {"simple": 149, "middle": 6241}
        for case_dir in case_dirs:
            trainer = tr.ModelTrainer(model_dir=None, input_dir=None)
            trainer.input_dir = common_src_path + case_dir
            trainer.model_dir = "./test_src/model/" + case_dir + ".bin"
            trainer.process_sources()
            trainer.build_model()
            m = trainer.model
            control_sum = 0

            # the simplest way to test the model is to calculate the sum of frequencies mapped after entries consisting of
            # a single word. This sum must be equal to an overall number of words.
            for key in m:
                if len(key) == 1:
                    control_sum += sum(list(m[key].values()))
            self.assertEquals(control_sum, word_counts[case_dir])

if __name__ == "__main__":
    ut.main()
