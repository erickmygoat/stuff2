from transformers import pipeline

class MasteryVerificationProtocol:
    """
    A module for the agent to test its own knowledge and skills.
    """
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        """
        Initializes the MasteryVerificationProtocol.

        Args:
            model_name (str): The name of the pre-trained summarization model to use.
        """
        try:
            self.summarizer = pipeline("summarization", model=model_name)
        except Exception as e:
            print(f"Error initializing summarization pipeline: {e}")
            self.summarizer = None

    def summarize_text(self, text, max_length=150, min_length=30):
        """
        Generates a concise summary of the given text.

        Args:
            text (str): The text to be summarized.
            max_length (int): The maximum length of the summary.
            min_length (int): The minimum length of the summary.

        Returns:
            str: The generated summary, or an error message if summarization fails.
        """
        if not self.summarizer:
            return "Summarization model is not available."

        try:
            # The model works best with text between 512 and 1024 tokens.
            # We'll truncate the text to ensure it fits.
            summary = self.summarizer(text[:1024], max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            return f"An error occurred during summarization: {e}"

# Example Usage:
if __name__ == '__main__':
    # This example requires a model download on first run, which may take time.
    protocol = MasteryVerificationProtocol()

    # A sample text about a complex topic
    sample_text = """
    The Fourier Transform is a mathematical transform that decomposes a function
    (often a function of time, or a signal) into its constituent frequencies,
    such as the expression of a musical chord in terms of the volumes and
    frequencies of its constituent notes. The term Fourier transform refers to
    both the frequency domain representation and the mathematical operation that
    associates the frequency domain representation to a function of time.
    The Fourier transform of a function of time is itself a complex-valued
    function of frequency, whose absolute value represents the amount of that
    frequency present in the original function, and whose complex argument is
    the phase offset of the basic sinusoid in that frequency.
    """

    summary = protocol.summarize_text(sample_text)

    print("--- Mastery Verification (Summarization) ---")
    print("\\nOriginal Text:")
    print(sample_text.strip())
    print("\\nGenerated Summary:")
    print(summary)
