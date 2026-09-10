import unittest

from solver import extract_prediction_payload


class ExtractPredictionPayloadTests(unittest.TestCase):
    def test_extracts_json_from_noisy_response(self):
        noisy = '''
        I will verify the pattern once more.
        {
          "summary": "The rule is to rotate the pattern by 90 degrees.",
          "prediction": [[1, 0], [0, 1]]
        }
        This is the final answer.
        '''
        result = extract_prediction_payload(noisy)
        self.assertEqual(result["summary"], "The rule is to rotate the pattern by 90 degrees.")
        self.assertEqual(result["prediction"], [[1, 0], [0, 1]])

    def test_extracts_tagged_response_with_extra_text(self):
        noisy = '''
        I think the answer is this.
        <summary>
        Flip the colors and mirror the pattern.
        </summary>
        <prediction>
        1 0
        0 1
        </prediction>
        I confirm it.
        '''
        result = extract_prediction_payload(noisy)
        self.assertEqual(result["summary"], "Flip the colors and mirror the pattern.")
        self.assertEqual(result["prediction"], [[1, 0], [0, 1]])


if __name__ == "__main__":
    unittest.main()
